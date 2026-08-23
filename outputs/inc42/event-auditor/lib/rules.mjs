/* Failure classification. Every rule returns findings; nothing here talks to the network. */

const P0 = 'P0', P1 = 'P1', P2 = 'P2';
let seq = 0;
const F = (o) => ({ id: `F${String(++seq).padStart(3, '0')}`, ...o });
export const resetIds = () => { seq = 0; };

function lev(a, b) {
  const m = a.length, n = b.length;
  if (Math.abs(m - n) > 3) return 99;
  const d = Array.from({ length: m + 1 }, (_, i) => [i, ...Array(n).fill(0)]);
  for (let jj = 0; jj <= n; jj++) d[0][jj] = jj;
  for (let i = 1; i <= m; i++) for (let jj = 1; jj <= n; jj++)
    d[i][jj] = Math.min(d[i - 1][jj] + 1, d[i][jj - 1] + 1, d[i - 1][jj - 1] + (a[i - 1] === b[jj - 1] ? 0 : 1));
  return d[m][n];
}
const normKey = (k) => k.toLowerCase().replace(/[^a-z0-9]/g, '');
const pct = (a, b) => (b ? Math.round((a / b) * 1000) / 10 : 0);

/* ── 1 · NEVER_FIRES — spec'd, expected in a journey, absent everywhere ───── */
export function ruleNeverFires({ spec, aliases, browser, warehouse }) {
  const out = [];
  const fired = new Set(browser.events.map((e) => e.name));
  const vol = new Map((warehouse?.volumes || []).map((v) => [v.event, Number(v.volume) || 0]));
  for (const exp of browser.expectations) {
    const a = aliases.map[exp.event] || {};
    const live = a.posthog;
    const sawBrowser = live ? fired.has(live) : false;
    const sawWarehouse = live ? (vol.get(live) || 0) > 0 : false;
    if (sawBrowser || sawWarehouse) continue;
    out.push(F({
      cls: 'NEVER_FIRES',
      severity: exp.critical ? P0 : P1,
      event: exp.event,
      title: `\`${exp.event}\` never fires`,
      evidence: live
        ? `Mapped to live event \`${live}\`, but the journey "${exp.journey}" produced 0 and the 30d warehouse volume is 0.`
        : `No production event is mapped to this spec event at all (status: ${a.status ?? 'unmapped'}).`,
      impact: exp.note || spec.byName[exp.event]?.metric || 'Metric in the spec has no data behind it.',
      fix: live ? `Check the handler for \`${live}\`.` : `Instrument \`${exp.event}\` per the spec (${spec.byName[exp.event]?.fires_when ?? '—'}).`,
      journey: exp.journey,
    }));
  }
  return out;
}

/* ── 2 · FIRES_NOT_LANDED — the loop-closing rule; only this proves ingestion ── */
export function ruleFiresNotLanded({ browser, warehouse }) {
  if (!warehouse?.runVerification) return [];
  const landed = new Set(warehouse.runVerification.map((r) => r.event));
  const byName = new Map();
  for (const e of browser.events) {
    if (e.vendor !== 'posthog') continue;
    byName.set(e.name, (byName.get(e.name) || 0) + 1);
  }
  return [...byName].filter(([n]) => !landed.has(n)).map(([n, c]) => F({
    cls: 'FIRES_NOT_LANDED',
    severity: P0,
    event: n,
    title: `\`${n}\` leaves the browser but never lands in PostHog`,
    evidence: `Captured ${c}× on the wire to the PostHog endpoint during this run, but a HogQL query on this run's distinct_id returns 0 rows.`,
    impact: 'Silent data loss — the event looks correct in devtools and is invisible in analysis.',
    fix: 'Check ingestion: project API key, CSP, the posthog.inc42.com reverse proxy, and any consent gate that drops the batch.',
  }));
}

/* ── 3 · GTM_ONLY — fires to ads tools, never to product analytics ────────── */
export function ruleGtmOnly({ browser, aliases }) {
  const byVendor = {};
  for (const e of browser.events) (byVendor[e.vendor] ||= new Set()).add(e.name);
  const out = [];
  for (const [specName, a] of Object.entries(aliases.map)) {
    if (a.status !== 'gtm_only' || !a.gtm) continue;
    const sawGtm = ['gtm', 'meta', 'ga4'].some((v) => byVendor[v]?.has(a.gtm));
    out.push(F({
      cls: 'GTM_ONLY',
      severity: P1,
      event: specName,
      title: `\`${specName}\` reaches GTM/Meta but never PostHog`,
      evidence: `${sawGtm ? 'Confirmed live this run: ' : 'Per the 12-Aug audit: '}fires as \`${a.gtm}\` on the GTM/Meta path with 0 PostHog captures.`,
      impact: 'The ad platform can optimise on this signal; product analytics cannot see it. ' + (a.note || ''),
      fix: `Emit \`${specName}\` to PostHog with its spec'd property groups.`,
    }));
  }
  return out;
}

/* ── 4 · DOUBLE_FIRE — two names for one action, or one name twice ────────── */
export function ruleDoubleFire({ browser, warehouse }) {
  const out = [];
  // (a) same event, same marker window, fired more than expected
  const perMark = {};
  for (const e of browser.events) {
    const k = `${e.marker || '—'}|${e.vendor}|${e.name}`;
    (perMark[k] ||= []).push(e);
  }
  for (const [k, list] of Object.entries(perMark)) {
    if (list.length < 2) continue;
    const [marker, vendor, name] = k.split('|');
    // identical payloads within 2s = a genuine duplicate, not a legitimate repeat
    const sig = (e) => JSON.stringify(e.props ?? {});
    const groups = {};
    for (const e of list) (groups[sig(e)] ||= []).push(e);
    for (const g of Object.values(groups)) {
      if (g.length < 2) continue;
      const span = Math.max(...g.map((x) => x.t || 0)) - Math.min(...g.map((x) => x.t || 0));
      if (span > 2000) continue;
      out.push(F({
        cls: 'DOUBLE_FIRE',
        severity: P1,
        event: name,
        title: `\`${name}\` double-fires (${vendor})`,
        evidence: `${g.length} identical payloads within ${span}ms at step "${marker}".`,
        impact: 'Inflated volume; every rate computed against it is wrong.',
        fix: 'Find the duplicate listener — usually an SPA re-render or a handler bound twice.',
      }));
    }
  }
  // (b) warehouse: near-identical event NAMES (Modal Close vs Modal Closed)
  const vols = (warehouse?.volumes || []).filter((v) => Number(v.volume) > 50);
  for (let i = 0; i < vols.length; i++) for (let jj = i + 1; jj < vols.length; jj++) {
    const a = vols[i].event, b = vols[jj].event;
    if (normKey(a) === normKey(b) || lev(a.toLowerCase(), b.toLowerCase()) <= 2) {
      out.push(F({
        cls: 'DOUBLE_FIRE',
        severity: P1,
        event: `${a} / ${b}`,
        title: `Two events for one action: \`${a}\` and \`${b}\``,
        evidence: `${a}: ${Number(vols[i].volume).toLocaleString()}/30d · ${b}: ${Number(vols[jj].volume).toLocaleString()}/30d.`,
        impact: 'Double-count risk; anyone filtering on one name silently loses the other.',
        fix: 'Consolidate to one canonical name; alias the other during migration.',
      }));
    }
  }
  return out;
}

/* ── 5 · PROP_MISSING — spec'd property absent or thinly covered ──────────── */
export function ruleMissingProps({ spec, aliases, browser, warehouse }) {
  const out = [];
  const seen = {};
  for (const e of browser.events) {
    if (e.vendor !== 'posthog') continue;
    (seen[e.name] ||= []).push(e.props || {});
  }
  for (const exp of browser.expectations) {
    const live = aliases.map[exp.event]?.posthog;
    if (!live || !seen[live]) continue;
    const want = exp.props || (spec.byName[exp.event]?.properties || []).map((p) => p.name);
    const present = new Set(seen[live].flatMap((p) => Object.keys(p)));
    const presentNorm = new Set([...present].map(normKey));
    const missing = want.filter((w) => !presentNorm.has(normKey(w)));
    if (!missing.length) continue;
    out.push(F({
      cls: 'PROP_MISSING',
      severity: exp.critical ? P0 : P1,
      event: exp.event,
      title: `\`${live}\` is missing ${missing.length} spec'd propert${missing.length > 1 ? 'ies' : 'y'}`,
      evidence: `Missing: ${missing.map((m) => `\`${m}\``).join(', ')}. Captured keys: ${[...present].slice(0, 14).join(', ')}${present.size > 14 ? '…' : ''}`,
      impact: exp.note || 'The dimension the event exists to slice by is unavailable.',
      fix: `Attach ${missing.join(', ')} at the call site.`,
      journey: exp.journey,
    }));
  }
  // warehouse coverage: a prop present on <90% of rows is drifting
  for (const c of warehouse?.coverage || []) {
    if (c.share >= 90 || c.total < 500) continue;
    out.push(F({
      cls: 'PROP_COVERAGE',
      severity: c.share < 20 ? P1 : P2,
      event: c.event,
      title: `\`${c.key}\` only covers ${c.share}% of \`${c.event}\``,
      evidence: `${Number(c.present).toLocaleString()} of ${Number(c.total).toLocaleString()} rows in the last 30d.`,
      impact: 'Any breakdown on this property silently drops the uncovered majority.',
      fix: 'Set the property unconditionally, or document the conditional and exclude it from the spec.',
    }));
  }
  return out;
}

/* ── 6 · NAME_DRIFT — same concept, several keys ──────────────────────────── */
export function ruleNameDrift({ warehouse }) {
  const keys = (warehouse?.allKeys || []).filter((k) => Number(k.volume) > 20);
  const buckets = {};
  for (const k of keys) (buckets[normKey(k.key)] ||= []).push(k);
  const out = [];
  for (const group of Object.values(buckets)) {
    if (group.length < 2) continue;
    out.push(F({
      cls: 'NAME_DRIFT',
      severity: P1,
      event: group[0].key,
      title: `${group.length} casing variants of one property`,
      evidence: group.map((g) => `\`${g.key}\` (${Number(g.volume).toLocaleString()})`).join(' · '),
      impact: 'Cross-tool joins and any filter on one spelling silently drop the rest.',
      fix: 'Pick one key; alias the others through a single transform layer.',
    }));
  }
  // typo-distance pairs across different normalised keys (Modal Type vs Model Type)
  const uniq = Object.values(buckets).map((g) => g[0]);
  for (let i = 0; i < uniq.length; i++) for (let jj = i + 1; jj < uniq.length; jj++) {
    const a = uniq[i], b = uniq[jj];
    if (lev(normKey(a.key), normKey(b.key)) !== 1) continue;
    if (Math.min(Number(a.volume), Number(b.volume)) < 100) continue;
    out.push(F({
      cls: 'NAME_DRIFT',
      severity: P0,
      event: `${a.key} / ${b.key}`,
      title: `Likely production typo: \`${a.key}\` vs \`${b.key}\``,
      evidence: `One character apart, both live: \`${a.key}\` ${Number(a.volume).toLocaleString()} · \`${b.key}\` ${Number(b.volume).toLocaleString()}.`,
      impact: 'Consumers must match the typo forever, or lose that share of rows.',
      fix: 'Rename with a migration; alias the misspelling during transition, then drop it.',
    }));
  }
  return out;
}

/* ── 7 · IDENTITY — the rule that poisons every other number ──────────────── */
export function ruleIdentity({ browser }) {
  const out = [];
  const snaps = browser.identity || [];
  const emailish = /@/;
  for (const s of snaps) {
    if (s.posthog_distinct_id && emailish.test(String(s.posthog_distinct_id))) {
      out.push(F({
        cls: 'IDENTITY',
        severity: P0,
        event: '(identity)',
        title: 'PostHog distinct_id is an email address',
        evidence: `\`posthog.get_distinct_id()\` = "${String(s.posthog_distinct_id).replace(/(.{3}).*(@.*)/, '$1…$2')}" at ${s.url}.`,
        impact: 'PII is the primary key. An email change or re-login fractures the person; the anon→known merge is fragile.',
        fix: 'identify() with the immutable Auth0 uid as distinct_id; keep email as a $set property only.',
      }));
      break;
    }
  }
  const signedOut = snaps.find((s) => /reset|logout|signed_out/i.test(s.reason || ''));
  if (signedOut && signedOut.posthog_distinct_id && emailish.test(String(signedOut.posthog_distinct_id))) {
    out.push(F({
      cls: 'IDENTITY', severity: P0, event: '(identity)',
      title: 'posthog.reset() is not called on logout',
      evidence: 'distinct_id still resolves to the previous user after sign-out.',
      impact: 'The next anonymous visitor on this device is merged into the previous person.',
      fix: 'Call posthog.reset() in the logout handler.',
    }));
  }
  const cioNull = snaps.filter((s) => s.cio_user_id === null && s.posthog_distinct_id && emailish.test(String(s.posthog_distinct_id)));
  if (cioNull.length) {
    out.push(F({
      cls: 'IDENTITY', severity: P0, event: '(identity)',
      title: 'Customer.io is not identified client-side',
      evidence: `\`analytics.user().id()\` = null while PostHog reports a logged-in user (${cioNull.length} snapshot${cioNull.length > 1 ? 's' : ''}).`,
      impact: 'Browser-side CIO events are anonymous. All lifecycle messaging depends on server/reverse-ETL — a single point of failure.',
      fix: 'Call Customer.io identify() on auth; document client vs server event ownership explicitly.',
    }));
  }
  return out;
}

/* ── 8 · PII_LEAK ─────────────────────────────────────────────────────────── */
export function rulePII({ browser }) {
  const out = [];
  const hits = (browser.identity || []).flatMap((s) => (s.pii || []).map((p) => ({ ...p, url: s.url })));
  const byPath = {};
  for (const h of hits) (byPath[`${h.path}:${h.kind}`] ||= h);
  for (const h of Object.values(byPath)) {
    out.push(F({
      cls: 'PII_LEAK', severity: P0, event: '(privacy)',
      title: `Raw ${h.kind} in \`${h.path.split('.')[0]}\``,
      evidence: `Found at \`${h.path}\` (sample "${h.sample}") on ${h.url}.`,
      impact: 'Exposed to every GTM tag and shipped to third parties. Direct DPDP exposure (May-2027).',
      fix: 'Send hashed identifiers only client-side; strip raw email/phone from the dataLayer and the shared analytics bundle.',
    }));
  }
  // raw PII on the wire
  const wire = browser.events.filter((e) =>
    /(^|_)(em|ph|fn|ln)$|ud\[/.test(Object.keys(e.props || {}).join(',')) ||
    /@/.test(JSON.stringify(e.props || {}).slice(0, 4000)));
  const vendors = [...new Set(wire.map((e) => e.vendor))].filter((v) => v !== 'posthog');
  if (vendors.length) {
    out.push(F({
      cls: 'PII_LEAK', severity: P0, event: '(privacy)',
      title: `Identifiers sent to ${vendors.join(', ')}`,
      evidence: `${wire.length} outbound payload(s) carried email-shaped or ud[]/em/ph/fn/ln fields.`,
      impact: 'Third-party sharing of personal data; needs a consent basis under DPDP.',
      fix: 'Confirm the consent basis, or disable advanced matching / CAPI PII.',
    }));
  }
  return out;
}

/* ── 9 · VENDOR_ASYMMETRY — the ads tool gets everything, product gets nothing ── */
export function ruleVendorAsymmetry({ browser }) {
  const byName = {};
  for (const e of browser.events) {
    const k = normKey(e.name || '');
    (byName[k] ||= {})[e.vendor] = Math.max((byName[k][e.vendor] ?? 0), Object.keys(e.props || {}).length);
    (byName[k].__name ||= e.name);
  }
  const out = [];
  for (const [, v] of Object.entries(byName)) {
    const ph = v.posthog ?? null;
    const rich = Math.max(v.meta ?? 0, v.ga4 ?? 0, v.gtm ?? 0);
    if (ph == null || rich === 0) continue;
    if (rich >= 10 && ph <= rich / 3) {
      out.push(F({
        cls: 'VENDOR_ASYMMETRY', severity: P1, event: v.__name,
        title: `\`${v.__name}\`: PostHog gets ${ph} properties, ads tools get ${rich}`,
        evidence: `Same user action, same moment — the ad platform receives the full bundle while product analytics receives ${ph}.`,
        impact: 'The tool you make product decisions in is the one starved of context.',
        fix: 'Attach the shared Super + Story bundle to the PostHog call through the same transform layer.',
      }));
    }
  }
  return out;
}

/* ── 10 · ZOMBIE + NOISE — warehouse hygiene ──────────────────────────────── */
export function ruleZombieAndNoise({ spec, aliases, warehouse }) {
  const out = [];
  const mapped = new Set(Object.values(aliases.map).map((a) => a.posthog).filter(Boolean));
  const NOISE = /^(gtm\.|dl_event|test_event|test$|\$?session_start$|first_visit$|user_signed_up|payment_completed|subscription_created)/i;
  for (const v of warehouse?.volumes || []) {
    const vol = Number(v.volume) || 0;
    const perDay = Number(v.per_day) || 0;
    if (NOISE.test(v.event) && vol > 0) {
      out.push(F({
        cls: 'NOISE', severity: P1, event: v.event,
        title: `\`${v.event}\` is leaking into the Live project`,
        evidence: `${vol.toLocaleString()} events / 30d. GTM dataLayer or test traffic, not deliberate instrumentation.`,
        impact: 'Pollutes the Live project; inflates event-definition lists and confuses anyone browsing the taxonomy.',
        fix: 'Route to the Stage project (57482) or drop at the GTM tag.',
      }));
      continue;
    }
    if (mapped.has(v.event) && vol > 0 && perDay < 1) {
      out.push(F({
        cls: 'ZOMBIE', severity: P0, event: v.event,
        title: `\`${v.event}\` is effectively dead (${vol} events / 30d)`,
        evidence: `${perDay.toFixed(2)}/day across ${Number(v.persons).toLocaleString()} persons. Last seen ${v.last_seen}.`,
        impact: 'The event exists, so dashboards built on it look healthy while reporting nothing.',
        fix: 'Either fix the handler or deprecate the event and remove it from the plan.',
      }));
    }
  }
  return out;
}

/* ── 11 · UNSPECIFIED — live events nobody planned ────────────────────────── */
export function ruleUnspecified({ aliases, warehouse }) {
  const mapped = new Set(Object.values(aliases.map).map((a) => a.posthog).filter(Boolean));
  const known = new Set(Object.keys(aliases.unspecified_live_events || {}));
  return (warehouse?.volumes || [])
    .filter((v) => Number(v.volume) > 1000 && !mapped.has(v.event) && !v.event.startsWith('$'))
    .slice(0, 20)
    .map((v) => F({
      cls: 'UNSPECIFIED', severity: known.has(v.event) ? P2 : P1, event: v.event,
      title: `\`${v.event}\` is live but not in the tracking plan`,
      evidence: `${Number(v.volume).toLocaleString()}/30d. ${aliases.unspecified_live_events?.[v.event] ?? 'Undocumented.'}`,
      impact: 'Ungoverned surface area — nobody owns its schema, so it drifts.',
      fix: 'Fold into the plan with an owner and a property contract, or deprecate.',
    }));
}

export const ALL_RULES = [
  ruleNeverFires, ruleFiresNotLanded, ruleGtmOnly, ruleDoubleFire, ruleMissingProps,
  ruleNameDrift, ruleIdentity, rulePII, ruleVendorAsymmetry, ruleZombieAndNoise, ruleUnspecified,
];

export function runRules(ctx) {
  resetIds();
  const findings = [];
  for (const r of ALL_RULES) {
    try { findings.push(...(r(ctx) || [])); }
    catch (e) { findings.push(F({ cls: 'RULE_ERROR', severity: P2, event: r.name, title: `Rule ${r.name} failed`, evidence: String(e), impact: '—', fix: '—' })); }
  }
  const order = { P0: 0, P1: 1, P2: 2 };
  return findings.sort((a, b) => order[a.severity] - order[b.severity] || a.cls.localeCompare(b.cls));
}
