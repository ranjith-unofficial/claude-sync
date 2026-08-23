#!/usr/bin/env node
/* inc42 event auditor — drive the UI, capture the wire, verify ingestion, diff the spec.
 *
 *   node audit.mjs                          full audit (browser + warehouse)
 *   node audit.mjs --only=warehouse         PostHog-only, no browser
 *   node audit.mjs --only=browser           browser-only, no API key needed
 *   node audit.mjs --journeys=search,freewall --headed=false --days=30
 */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { decodeRequest } from './lib/vendors.mjs';
import { state as actionState } from './lib/actions.mjs';
import * as ph from './lib/posthog.mjs';
import { runRules } from './lib/rules.mjs';
import { renderReport } from './lib/report.mjs';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const arg = (k, d) => {
  const hit = process.argv.find((a) => a.startsWith(`--${k}=`));
  return hit ? hit.split('=').slice(1).join('=') : d;
};
const ONLY = arg('only', 'all');
const HEADED = arg('headed', 'true') !== 'false';
const DAYS = Number(arg('days', 30));
const PICK = arg('journeys', '').split(',').map((s) => s.trim()).filter(Boolean);
const WAIT_INGEST = Number(arg('ingest-wait', 120)); // seconds before verifying

/* inc42.com serves HTTP 201 + application/octet-stream to any UA containing
   "HeadlessChrome" — a bot-mitigation rule. Without this override every headless
   run silently gets a non-HTML body. Anything you point at this site (synthetic
   monitors included) needs a real Chrome UA. */
const REAL_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36';

const log = (...a) => console.log(...a);
const readJSON = (p) => JSON.parse(fs.readFileSync(path.join(ROOT, p), 'utf8'));

/* ── load spec ─────────────────────────────────────────────────────────── */
const target = readJSON('spec/target.json');
const aliases = readJSON('spec/aliases.json');
const liveSheet = readJSON('spec/live.json');
const spec = { ...target, byName: Object.fromEntries(target.events.map((e) => [e.event, e])) };

/* ── browser phase ─────────────────────────────────────────────────────── */
async function runBrowser() {
  const dir = path.join(ROOT, 'journeys');
  const files = fs.readdirSync(dir).filter((f) => f.endsWith('.mjs')).sort();
  const journeys = [];
  for (const f of files) {
    const mod = (await import(path.join(dir, f))).default;
    if (!PICK.length || PICK.includes(mod.id)) journeys.push(mod);
  }
  log(`\n▶ browser phase — ${journeys.length} journey(s), ${HEADED ? 'headed' : 'headless'}`);

  const browser = await chromium.launch({
    headless: !HEADED,
    channel: 'chrome',
    args: ['--disable-blink-features=AutomationControlled'],
  }).catch(() => chromium.launch({ headless: !HEADED }));

  const events = [];
  const identity = [];
  const expectations = [];
  const journeyResults = [];
  const distinctIds = new Set();
  const startedAt = new Date().toISOString();

  for (const j of journeys) {
    log(`\n  ── ${j.name}`);
    const ctx = await browser.newContext({
      viewport: { width: 1440, height: 900 },
      userAgent: REAL_UA,
      locale: 'en-IN',
      timezoneId: 'Asia/Kolkata',
      extraHTTPHeaders: { 'accept-language': 'en-IN,en;q=0.9' },
    });
    // Streamed from the probe. Bound before addInitScript so it exists on first document.
    await ctx.exposeBinding('__AUDIT_EMIT__', (src, r) => {
      try {
        if (!r || typeof r !== 'object') return;
        if (r.channel === 'identity') {
          // addInitScript runs in every frame; ad/GTM iframes produce empty about:blank snapshots.
          const empty = r.posthog_distinct_id == null && r.cio_user_id == null && r.event_properties_bundle == null;
          if (r.url === 'blank' && empty) return;
          identity.push({ ...r, journey: j.id });
          return;
        }
        if (r.vendor === '_marker') return;
        events.push({
          vendor: r.vendor, name: r.name, props: r.props ?? {}, t: r.t,
          journey: j.id, marker: actionState.marker, source: 'sdk', kind: r.kind,
          stack: r.stack, pageUrl: r.url, replayed: r.replayed === true,
        });
      } catch {}
    });
    await ctx.addInitScript({ path: path.join(ROOT, 'lib/probe.js') });

    const page = await ctx.newPage();
    actionState.marker = `${j.id}:start`;

    page.on('request', (req) => {
      for (const e of decodeRequest(req)) {
        if (e.distinct_id) distinctIds.add(e.distinct_id);
        events.push({ ...e, journey: j.id, marker: actionState.marker, wallMs: Date.now(), source: 'wire' });
      }
    });
    page.on('pageerror', (e) => events.push({ vendor: '_page', name: '__PAGE_ERROR__', props: { message: String(e) }, journey: j.id, marker: actionState.marker, source: 'page' }));

    let result = null, error = null;
    try {
      result = await j.run(page, { log: (m) => log(`     ${m}`) });
    } catch (e) {
      error = String(e);
      log(`     ✗ journey error: ${error.split('\n')[0]}`);
    }

    // drain the probe + any late beacons
    await page.waitForTimeout(3000).catch(() => {});
    // The binding already streamed everything; this only surfaces probe self-diagnostics.
    const probe = await page.evaluate(() => (window.__AUDIT__ ? { notes: window.__AUDIT__.notes } : null)).catch(() => null);
    if (probe?.notes?.length) log(`     probe notes: ${probe.notes.slice(0, 3).join(' | ')}`);

    for (const e of j.expect || []) {
      expectations.push({ ...e, journey: j.id, critical: spec.byName[e.event]?.critical ?? false });
    }
    journeyResults.push({ id: j.id, name: j.name, result, error });
    await ctx.close().catch(() => {});
  }
  await browser.close().catch(() => {});

  const wire = events.filter((e) => e.source === 'wire');
  log(`\n  captured ${wire.length} wire events, ${events.length - wire.length} SDK calls, ${identity.length} identity snapshots`);
  const byVendor = {};
  for (const e of wire) byVendor[e.vendor] = (byVendor[e.vendor] || 0) + 1;
  log(`  by vendor: ${Object.entries(byVendor).map(([k, v]) => `${k}=${v}`).join(' · ') || '(none)'}`);

  return { events, identity, expectations, journeys: journeyResults, distinctIds: [...distinctIds], startedAt };
}

/* ── warehouse phase ───────────────────────────────────────────────────── */
async function runWarehouse(browserRun) {
  if (!ph.configured()) {
    log('\n▶ warehouse phase — SKIPPED (POSTHOG_API_KEY not set)');
    return null;
  }
  const range = ph.dateRange(DAYS);
  log(`\n▶ warehouse phase — PostHog project ${process.env.POSTHOG_PROJECT_ID || 53557}, ${range.start} → ${range.end}`);

  const volumes = await ph.hogql(ph.qEventVolumes(range));
  log(`  ${volumes.length} distinct events in ${DAYS}d`);

  const allKeys = await ph.hogql(ph.qAllKeys(range));
  log(`  ${allKeys.length} distinct property keys`);

  // coverage for the events the spec actually maps to
  const mapped = [...new Set(Object.values(aliases.map).map((a) => a.posthog).filter(Boolean))];
  const topMapped = volumes.filter((v) => mapped.includes(v.event) && Number(v.volume) > 100).slice(0, 12);
  const coverage = [];
  for (const v of topMapped) {
    const rows = await ph.hogql(ph.qPropertyCoverage(v.event, range)).catch(() => []);
    for (const r of rows) {
      const total = Number(r.total) || 0, present = Number(r.present) || 0;
      if (!total) continue;
      coverage.push({ event: v.event, key: r.key, present, total, share: Math.round((present / total) * 1000) / 10 });
    }
  }
  log(`  coverage sampled for ${topMapped.length} events (${coverage.length} key/event pairs)`);

  // enum conformance for the properties the dictionary constrains
  const enumProps = spec.dictionary.filter((d) => d.allowed.length >= 2).map((d) => d.property);
  const liveEnumNames = ['Page Type', 'Categories', 'Story Type', 'Development Type', 'Company Type', 'User Type', 'User State', 'Result Type', 'Share Platform', 'Modal Type'];
  const enums = [];
  for (const p of liveEnumNames) {
    const rows = await ph.hogql(ph.qPropertyValues(p, range)).catch(() => []);
    if (rows.length) enums.push({ property: p, values: rows.slice(0, 60) });
  }
  log(`  enum values pulled for ${enums.length} properties`);

  // close the loop on this run
  let runVerification = null;
  if (browserRun?.distinctIds?.length) {
    log(`  waiting ${WAIT_INGEST}s for ingestion before verifying ${browserRun.distinctIds.length} distinct_id(s)…`);
    await new Promise((r) => setTimeout(r, WAIT_INGEST * 1000));
    runVerification = await ph.hogql(ph.qVerifyRun(browserRun.distinctIds, browserRun.startedAt)).catch((e) => {
      log(`  verification query failed: ${e.message}`);
      return null;
    });
    if (runVerification) log(`  ${runVerification.length} event type(s) from this run landed in PostHog`);
  }

  const personProps = await ph.hogql(ph.qPersonProps()).catch(() => []);
  return { range, volumes, allKeys, coverage, enums, runVerification, personProps };
}

/* ── main ──────────────────────────────────────────────────────────────── */
(async () => {
  const stamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const outDir = path.join(ROOT, 'runs', stamp);
  fs.mkdirSync(outDir, { recursive: true });

  const browser = ONLY === 'warehouse' ? { events: [], identity: [], expectations: [], journeys: [], distinctIds: [] } : await runBrowser();
  const warehouse = ONLY === 'browser' ? null : await runWarehouse(browser);

  const findings = runRules({ spec, aliases, liveSheet, browser, warehouse });

  fs.writeFileSync(path.join(outDir, 'raw.json'), JSON.stringify({ browser, warehouse }, null, 2));
  fs.writeFileSync(path.join(outDir, 'findings.json'), JSON.stringify(findings, null, 2));
  const html = renderReport({ spec, aliases, liveSheet, browser, warehouse, findings, stamp, days: DAYS });
  const htmlPath = path.join(outDir, 'report.html');
  fs.writeFileSync(htmlPath, html);

  const counts = findings.reduce((a, f) => ((a[f.severity] = (a[f.severity] || 0) + 1), a), {});
  log(`\n▶ ${findings.length} findings — P0:${counts.P0 || 0}  P1:${counts.P1 || 0}  P2:${counts.P2 || 0}`);
  for (const f of findings.filter((x) => x.severity === 'P0').slice(0, 10)) log(`   P0 · ${f.title}`);
  log(`\n  report  ${htmlPath}`);
  log(`  raw     ${path.join(outDir, 'raw.json')}\n`);
})();
