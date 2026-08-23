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
// Denominators: without them the funnel above them cannot be measured at all.
const DENOMINATORS = new Set(['freewall_shown', 'plus_wall_shown', 'sign_in_prompt_shown',
  'newsletter_prompt_shown', 'search_initiated', 'web_push_prompt_shown']);

export function ruleNeverFires({ spec, aliases, browser, warehouse }) {
  const out = [];
  const fired = new Set(browser.events.filter((e) => e.vendor === 'posthog').map((e) => e.name));
  const vol = new Map((warehouse?.volumes || []).map((v) => [v.event, Number(v.volume) || 0]));
  const haveWarehouse = Boolean(warehouse?.volumes?.length);

  for (const exp of browser.expectations) {
    const a = aliases.map[exp.event] || {};
    const live = a.posthog;
    if (live && fired.has(live)) continue;               // observed this run — nothing to report

    const sp = spec.byName[exp.event];
    const isP0 = exp.critical || sp?.critical || sp?.upsell || DENOMINATORS.has(exp.event);
    const wVol = live ? (vol.get(live) ?? 0) : 0;

    // Three genuinely different situations. Collapsing them is how an auditor cries wolf.
    if (live && haveWarehouse && wVol > 0) {
      out.push(F({
        cls: 'NOT_REPRODUCED', severity: P2, event: exp.event,
        title: `\`${exp.event}\` fires in production but not in this journey`,
        evidence: `\`${live}\` has ${wVol.toLocaleString()} events/30d in PostHog, yet the "${exp.journey}" journey produced none.`,
        impact: 'Either the journey does not reach the trigger, or the event is conditional (variant, segment, device). Not a defect on its own.',
        fix: 'Tighten the journey to hit the real trigger, or document the condition.',
        journey: exp.journey,
      }));
      continue;
    }
    if (live && haveWarehouse && wVol === 0) {
      out.push(F({
        cls: 'NEVER_FIRES', severity: isP0 ? P0 : P1, event: exp.event,
        title: `\`${exp.event}\` never fires`,
        evidence: `Mapped to \`${live}\`. Zero captures in the "${exp.journey}" journey AND zero volume in PostHog over the last 30 days.`,
        impact: exp.note || sp?.metric || 'The metric in the plan has no data behind it.',
        fix: `Check the handler for \`${live}\`.`,
        journey: exp.journey,
      }));
      continue;
    }
    if (!live) {
      if (a.status === 'gtm_only') continue;   // ruleGtmOnly already reports these, with better evidence
      out.push(F({
        cls: 'NOT_INSTRUMENTED', severity: isP0 ? P0 : P1, event: exp.event,
        title: `\`${exp.event}\` is not instrumented at all`,
        evidence: a.gtm
          ? `No PostHog event is mapped. It exists only on the GTM/Meta path as \`${a.gtm}\`.`
          : `No production event is mapped to this spec event (status: ${a.status ?? 'unmapped'}).`,
        impact: exp.note || sp?.metric || 'Planned metric with nothing behind it.',
        fix: `Instrument \`${exp.event}\` per the spec — fires when: ${sp?.fires_when ?? '—'}.`,
        journey: exp.journey,
      }));
      continue;
    }
    // mapped, browser saw nothing, and we have no warehouse to arbitrate
    out.push(F({
      cls: 'UNVERIFIED', severity: P2, event: exp.event,
      title: `\`${exp.event}\` not observed — unverified`,
      evidence: `\`${live}\` produced no captures in "${exp.journey}". No PostHog key was supplied, so production volume could not be checked.`,
      impact: 'Cannot distinguish a broken event from a journey that never reached the trigger.',
      fix: 'Set POSTHOG_API_KEY and re-run to resolve this either way.',
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
// GTM's own lifecycle pushes (gtm.js / gtm.dom / gtm.scrollDepth / config pushes with no
// `event` key) are container plumbing, not analytics events. Repeats there are normal.
const GTM_INTERNAL = /^gtm\./;
const isPlumbing = (e) =>
  !e.name ||
  GTM_INTERNAL.test(String(e.name)) ||
  e.name === 'null' ||
  e.replayed === true ||                                     // dataLayer backlog, not an observed firing
  e.vendor === '_page' ||                                    // page errors get their own rule
  (e.vendor === 'meta' && !/^(track|trackCustom)$/.test(e.kind ?? '')) ||  // fbq('init', <pixelId>)
  /^\d{10,}$/.test(String(e.name));                          // bare pixel / measurement IDs

export function ruleDoubleFire({ browser, warehouse }) {
  const out = [];
  // (a) identical payloads inside one journey step = a duplicate listener
  const perStep = {};
  for (const e of browser.events) {
    if (isPlumbing(e)) continue;
    ((perStep[`${e.journey}|${e.marker || '—'}|${e.vendor}|${e.name}`] ||= [])).push(e);
  }
  const agg = {};
  for (const [k, list] of Object.entries(perStep)) {
    if (list.length < 2) continue;
    const [, marker, vendor, name] = k.split('|');
    const groups = {};
    for (const e of list) (groups[JSON.stringify(e.props ?? {})] ||= []).push(e);
    for (const g of Object.values(groups)) {
      if (g.length < 2) continue;
      const ts = g.map((x) => x.t ?? x.wallMs ?? 0);
      const span = Math.max(...ts) - Math.min(...ts);
      if (span > 2000) continue;
      const a = (agg[`${vendor}|${name}`] ||= { vendor, name, steps: [], extra: 0, worst: 0 });
      a.steps.push(marker);
      a.extra += g.length - 1;
      a.worst = Math.max(a.worst, g.length);
    }
  }
  for (const a of Object.values(agg)) {
    out.push(F({
      cls: 'DOUBLE_FIRE',
      severity: P1,
      event: a.name,
      title: `\`${a.name}\` double-fires (${a.vendor})`,
      evidence: `${a.extra} redundant payload(s) across ${a.steps.length} step(s); worst case ${a.worst} identical calls within 2s (e.g. "${a.steps[0]}").`,
      impact: 'Inflated volume; every rate computed against this event is wrong.',
      fix: 'Find the duplicate listener — usually an SPA re-render or a handler bound twice.',
    }));
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
    // The spec sheet mixes real property names with inline footnotes ("*Story bundle only when…").
    const isRealProp = (name) => /^[a-z][a-z0-9_]*$/.test(name) && name.length <= 40;
    const want = (exp.props || (spec.byName[exp.event]?.properties || []).map((p) => p.name)).filter(isRealProp);
    if (!want.length) continue;
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

/* ── 12 · COVERAGE_GAP — fires to GA4/Meta, never to PostHog ──────────────── */
// Generalises the hardcoded GTM_ONLY alias: catches anything the site sends to the
// marketing stack while product analytics stays blind, whether or not it is in the plan.
export function ruleCoverageGap({ browser }) {
  const wire = browser.events.filter((e) => e.source === 'wire');
  const ph = new Set(wire.filter((e) => e.vendor === 'posthog').map((e) => normKey(e.name)));
  const ads = {};
  for (const e of wire) {
    if (!['ga4', 'meta'].includes(e.vendor)) continue;
    if (/^(page_view|PageView|user_engagement|scroll)$/i.test(String(e.name))) {
      // pageview/scroll are handled by their own spec rules; keep this list to custom events
      if (String(e.name).toLowerCase() !== 'scroll') continue;
    }
    const k = normKey(e.name);
    (ads[k] ||= { name: e.name, count: 0, vendors: new Set() });
    ads[k].count++;
    ads[k].vendors.add(e.vendor);
  }
  return Object.entries(ads)
    .filter(([k]) => !ph.has(k))
    .filter(([, v]) => v.count >= 2)
    .sort((a, b) => b[1].count - a[1].count)
    .map(([, v]) => F({
      cls: 'COVERAGE_GAP', severity: P1, event: v.name,
      title: `\`${v.name}\` reaches ${[...v.vendors].join('/')} but never PostHog`,
      evidence: `${v.count} captures to ${[...v.vendors].join(' and ')} during this run; 0 to PostHog.`,
      impact: 'The ad platform can optimise on this behaviour. The tool you make product decisions in cannot see it.',
      fix: 'Mirror the event to PostHog through the shared transform layer, or decide deliberately that it is marketing-only and record that.',
    }));
}

/* ── 13 · VENDOR_BALANCE — how lopsided is the stack overall ──────────────── */
export function ruleVendorBalance({ browser }) {
  const wire = browser.events.filter((e) => e.source === 'wire');
  if (!wire.length) return [];
  const types = {};
  for (const e of wire) (types[e.vendor] ||= new Set()).add(e.name);
  const ph = types.posthog?.size ?? 0;
  const ga = types.ga4?.size ?? 0;
  const cio = types.customerio?.size ?? 0;
  const out = [];
  if (ga > ph) {
    out.push(F({
      cls: 'VENDOR_BALANCE', severity: P0, event: '(stack)',
      title: `GA4 receives ${ga} distinct events; PostHog receives ${ph}`,
      evidence: `Across every journey in this run: ` +
        Object.entries(types).map(([v, s]) => `${v} ${s.size}`).join(' · ') + '.',
      impact: 'Product analytics is the thinner dataset. Every product decision is made on the tool with less information.',
      fix: 'Treat the PostHog payload as the contract and mirror to marketing tools, not the other way round.',
    }));
  }
  const cioTracks = wire.filter((e) => e.vendor === 'customerio' && e.type === 'track').length;
  if (cio > 0 && cioTracks === 0) {
    out.push(F({
      cls: 'VENDOR_BALANCE', severity: P0, event: '(stack)',
      title: 'Customer.io receives page calls but zero track calls',
      evidence: `${wire.filter((e) => e.vendor === 'customerio').length} outbound Customer.io calls this run, all of type "page". No track() at all.`,
      impact: 'All lifecycle messaging depends on server-side/reverse-ETL. No real-time site behaviour reaches the CRM, and the browser path is a silent single point of failure.',
      fix: 'Decide client vs server event ownership explicitly and document it; wire track() for the behaviours campaigns trigger on.',
    }));
  }
  return out;
}

/* ── 14 · PAGE_ERROR — a thrown error can kill every handler after it ──────── */
export function rulePageErrors({ browser }) {
  const errs = browser.events.filter((e) => e.vendor === '_page');
  if (!errs.length) return [];
  const byMsg = {};
  for (const e of errs) {
    const m = String(e.props?.message ?? '').split('\n')[0].slice(0, 160);
    (byMsg[m] ||= { count: 0, markers: new Set() });
    byMsg[m].count++;
    byMsg[m].markers.add(e.marker);
  }
  return Object.entries(byMsg).map(([msg, v]) => F({
    cls: 'PAGE_ERROR', severity: P1, event: '(runtime)',
    title: `Uncaught page error: ${msg.slice(0, 70)}`,
    evidence: `Thrown ${v.count}× during ${v.markers.size} journey step(s): ${[...v.markers].slice(0, 3).join(', ')}.`,
    impact: 'An uncaught error aborts the rest of its call stack — any analytics call queued after it never runs.',
    fix: 'Fix the error, or move analytics calls ahead of the throwing code.',
  }));
}

/* ── 15 · NEVER_IDENTIFIED — authenticated on the site, anonymous in analytics ── */
// PostHog mints a UUIDv7 for anonymous visitors. If an authenticated journey ran and the
// distinct_id still matches that shape on every snapshot, identify() never fired — the
// session is logged in to the site and anonymous to analytics.
const ANON_UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export function ruleNeverIdentified({ browser }) {
  const authJourneys = new Set(browser.journeys
    .filter((j) => ['logged-in', 'logout'].includes(j.id) && !j.error && !j.result?.skipped)
    .map((j) => j.id));
  if (!authJourneys.size) return [];

  const snaps = (browser.identity || [])
    .filter((s) => authJourneys.has(s.journey) && s.posthog_distinct_id);
  if (!snaps.length) return [];

  const out = [];
  const ids = [...new Set(snaps.map((s) => String(s.posthog_distinct_id)))];
  const allAnon = ids.every((id) => ANON_UUID.test(id));
  if (allAnon) {
    out.push(F({
      cls: 'NEVER_IDENTIFIED', severity: P0, event: '(identity)',
      title: 'Logged in to the site, anonymous in PostHog',
      evidence: `Across ${snaps.length} snapshots in an authenticated session, every \`distinct_id\` was an `
        + `anonymous UUID (e.g. ${ids[0]}). Never an email, never an Auth0 id. \`identify()\` did not fire.`,
      impact: 'Logged-in behaviour cannot be attributed to a person. Every funnel that joins anonymous reading '
        + 'to a known user breaks here, and this is the mechanism behind the low web identification rate.',
      fix: 'Call posthog.identify() with the Auth0 uid on every page load for an authenticated user, not only at '
        + 'the moment of login. Keep email as a $set property.',
    }));
  }
  if (ids.length > 1) {
    out.push(F({
      cls: 'NEVER_IDENTIFIED', severity: P1, event: '(identity)',
      title: `The same signed-in user carries ${ids.length} different distinct_ids`,
      evidence: `Observed: ${ids.map((i) => i.slice(0, 13) + '…').join(', ')} — one per browser context, with no identify() to merge them.`,
      impact: 'One person is counted as several. Person-level metrics and any retention or frequency number are inflated.',
      fix: 'Identify on load so contexts converge on the Auth0 uid.',
    }));
  }
  const cioNull = snaps.filter((s) => s.cio_user_id == null).length;
  if (cioNull === snaps.length) {
    out.push(F({
      cls: 'NEVER_IDENTIFIED', severity: P0, event: '(identity)',
      title: 'Customer.io holds a guest token for a signed-in user',
      evidence: `\`analytics.user().id()\` was null in all ${snaps.length} authenticated snapshots. The saved session `
        + 'also carries a `gist.web.usingGuestUserToken` key in localStorage.',
      impact: 'Every browser-side Customer.io event is attributed to a guest. Lifecycle messaging depends entirely on '
        + 'server-side/reverse-ETL, with no real-time site behaviour and no client-side fallback.',
      fix: 'Call the Customer.io identify() on auth, and document client vs server event ownership.',
    }));
  }
  return out;
}

export const ALL_RULES = [
  ruleNeverFires, ruleFiresNotLanded, ruleGtmOnly, ruleDoubleFire, ruleMissingProps,
  ruleNameDrift, ruleIdentity, rulePII, ruleVendorAsymmetry, ruleZombieAndNoise, ruleUnspecified,
  ruleCoverageGap, ruleVendorBalance, rulePageErrors, ruleNeverIdentified,
];

export function runRules(ctx) {
  resetIds();
  const findings = [];
  for (const r of ALL_RULES) {
    try { findings.push(...(r(ctx) || [])); }
    catch (e) { findings.push(F({ cls: 'RULE_ERROR', severity: P2, event: r.name, title: `Rule ${r.name} failed`, evidence: String(e), impact: '—', fix: '—' })); }
  }
  const order = { P0: 0, P1: 1, P2: 2 };
  // The same defect can surface from several journeys; report it once.
  const seen = new Set();
  const unique = findings.filter((f) => {
    const k = `${f.cls}|${f.event}|${f.title}`;
    if (seen.has(k)) return false;
    seen.add(k);
    return true;
  });
  return unique.sort((a, b) => order[a.severity] - order[b.severity] || a.cls.localeCompare(b.cls));
}
