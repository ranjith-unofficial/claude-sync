const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const md = (s) => esc(s).replace(/`([^`]+)`/g, '<code>$1</code>');
const n = (x) => (Number(x) || 0).toLocaleString('en-IN');

const SEV_NOTE = { P0: 'Blocks decisions', P1: 'Distorts numbers', P2: 'Hygiene / unresolved' };
const CLS = {
  NOT_INSTRUMENTED: 'Not instrumented', NEVER_FIRES: 'Never fires', NOT_REPRODUCED: 'Not reproduced',
  UNVERIFIED: 'Unverified', FIRES_NOT_LANDED: 'Fires, never lands', COVERAGE_GAP: 'Coverage gap',
  VENDOR_BALANCE: 'Vendor balance', VENDOR_ASYMMETRY: 'Vendor asymmetry', GTM_ONLY: 'Ads-only',
  DOUBLE_FIRE: 'Double-fire', PROP_MISSING: 'Missing properties', PROP_COVERAGE: 'Thin coverage',
  NAME_DRIFT: 'Name drift', IDENTITY: 'Identity', PII_LEAK: 'PII', ZOMBIE: 'Zombie event',
  NOISE: 'Noise', UNSPECIFIED: 'Unplanned event', PAGE_ERROR: 'Page error', RULE_ERROR: 'Rule error',
};
const STATUS_TONE = { implemented: 'ok', partial: 'warn', gtm_only: 'warn', missing: 'bad', server_side: 'na' };

export function reportStyles() {
  return `
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;450;500;600&display=swap">
<style>
:root{
  --paper:#fbfcfd; --surface:#f2f5f7; --raised:#ffffff; --line:#dde4e9; --line-soft:#e9eef1;
  --ink:#0d1418; --ink-2:#3c4a52; --ink-3:#68787f;
  --accent:#0e6f78; --accent-soft:#e2f1f2;
  --p0:#c0362c; --p1:#a56a09; --p2:#5b6b73; --ok:#14804a;
  --p0-bg:#fbeceb; --p1-bg:#fbf2e2; --p2-bg:#eef1f3; --ok-bg:#e6f4ec;
  --shadow:0 1px 2px rgba(13,20,24,.05),0 1px 12px rgba(13,20,24,.04);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#0d1418; --surface:#141d22; --raised:#161f25; --line:#26333a; --line-soft:#1e2a30;
  --ink:#e6edf1; --ink-2:#a9bac3; --ink-3:#748891;
  --accent:#4fc9d1; --accent-soft:#12333a;
  --p0:#f08a80; --p1:#e0ad4e; --p2:#8fa3ac; --ok:#5cc98d;
  --p0-bg:#2b1917; --p1-bg:#2a2214; --p2-bg:#1b252a; --ok-bg:#14291f;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 1px 14px rgba(0,0,0,.25);
}}
:root[data-theme="dark"]{
  --paper:#0d1418; --surface:#141d22; --raised:#161f25; --line:#26333a; --line-soft:#1e2a30;
  --ink:#e6edf1; --ink-2:#a9bac3; --ink-3:#748891;
  --accent:#4fc9d1; --accent-soft:#12333a;
  --p0:#f08a80; --p1:#e0ad4e; --p2:#8fa3ac; --ok:#5cc98d;
  --p0-bg:#2b1917; --p1-bg:#2a2214; --p2-bg:#1b252a; --ok-bg:#14291f;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 1px 14px rgba(0,0,0,.25);
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font:400 15px/1.6 "IBM Plex Sans","Helvetica Neue",Arial,sans-serif;
  -webkit-font-smoothing:antialiased;font-variant-numeric:tabular-nums}
.wrap{max-width:1140px;margin:0 auto;padding:56px 28px 96px;display:flex;flex-direction:column;gap:0}
code,.mono{font-family:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace}
code{font-size:.86em;background:var(--surface);padding:.1em .38em;border-radius:3px;color:var(--ink-2)}

.eyebrow{font-family:"IBM Plex Mono",monospace;font-size:11px;font-weight:500;letter-spacing:.14em;
  text-transform:uppercase;color:var(--accent);margin:0 0 14px}
h1{font-family:"IBM Plex Sans Condensed",sans-serif;font-weight:700;font-size:clamp(30px,4.4vw,46px);
  line-height:1.06;letter-spacing:-.015em;margin:0 0 16px;text-wrap:balance}
h2{font-family:"IBM Plex Sans Condensed",sans-serif;font-weight:600;font-size:22px;letter-spacing:-.005em;
  margin:0 0 4px;text-wrap:balance}
.h2wrap{display:flex;flex-direction:column;gap:4px;margin:60px 0 18px;padding-bottom:12px;border-bottom:2px solid var(--ink)}
.h2sub{color:var(--ink-3);font-size:13.5px;max-width:68ch}
.lede{font-size:17px;line-height:1.65;color:var(--ink-2);max-width:66ch;margin:0 0 8px}
.meta{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--ink-3);
  display:flex;flex-wrap:wrap;gap:6px 16px;margin-top:22px;padding-top:18px;border-top:1px solid var(--line)}

/* thesis */
.thesis{background:var(--raised);border:1px solid var(--line);border-radius:12px;padding:26px 28px;
  margin:38px 0 0;box-shadow:var(--shadow);display:flex;flex-direction:column;gap:20px}
.thesis .t{font-family:"IBM Plex Sans Condensed",sans-serif;font-weight:600;font-size:19px}
.bars{display:flex;flex-direction:column;gap:11px}
.bar{display:grid;grid-template-columns:110px 1fr 74px;align-items:center;gap:14px}
.bar .lbl{font-family:"IBM Plex Mono",monospace;font-size:12.5px;color:var(--ink-2)}
.bar .track{height:22px;background:var(--surface);border-radius:3px;overflow:hidden}
.bar .fill{height:100%;background:var(--accent);border-radius:3px}
.bar .fill.mute{background:var(--ink-3);opacity:.45}
.bar .val{font-family:"IBM Plex Mono",monospace;font-size:12.5px;color:var(--ink-3);text-align:right}
.thesis .note{font-size:13.5px;color:var(--ink-2);border-left:2px solid var(--accent);padding-left:14px;max-width:70ch}

/* tiles */
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(146px,1fr));gap:1px;
  background:var(--line);border:1px solid var(--line);border-radius:10px;overflow:hidden;margin:28px 0 0}
.tile{background:var(--raised);padding:16px 18px;display:flex;flex-direction:column;gap:3px}
.tile .v{font-family:"IBM Plex Sans Condensed",sans-serif;font-weight:700;font-size:30px;line-height:1;letter-spacing:-.02em}
.tile .l{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3)}
.tile .s{font-size:12px;color:var(--ink-3);line-height:1.4}
.tile.p0 .v{color:var(--p0)} .tile.p1 .v{color:var(--p1)} .tile.ok .v{color:var(--ok)} .tile.acc .v{color:var(--accent)}

/* findings */
.findings{display:flex;flex-direction:column;gap:10px}
.f{background:var(--raised);border:1px solid var(--line);border-radius:10px;padding:16px 20px 16px 22px;
  position:relative;overflow:hidden;box-shadow:var(--shadow)}
.f::before{content:"";position:absolute;inset:0 auto 0 0;width:3px;background:var(--sev)}
.f.s-P0{--sev:var(--p0)} .f.s-P1{--sev:var(--p1)} .f.s-P2{--sev:var(--p2)}
.f .top{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin-bottom:7px}
.chip{font-family:"IBM Plex Mono",monospace;font-size:10.5px;font-weight:600;letter-spacing:.06em;
  padding:2px 7px;border-radius:3px;background:var(--sev-bg,var(--surface));color:var(--sev,var(--ink-2))}
.f.s-P0 .chip{--sev-bg:var(--p0-bg)} .f.s-P1 .chip{--sev-bg:var(--p1-bg)} .f.s-P2 .chip{--sev-bg:var(--p2-bg)}
.chip.cls{background:transparent;border:1px solid var(--line);color:var(--ink-3);font-weight:500}
.f .ttl{font-family:"IBM Plex Sans Condensed",sans-serif;font-weight:600;font-size:16.5px;line-height:1.3;margin-bottom:6px}
.f .ev{font-size:13.5px;color:var(--ink-2);line-height:1.55;margin-bottom:10px;max-width:78ch}
.f .row{display:grid;grid-template-columns:64px 1fr;gap:10px;font-size:13px;line-height:1.5;
  color:var(--ink-2);padding-top:8px;border-top:1px solid var(--line-soft);max-width:82ch}
.f .row + .row{border-top:none;padding-top:4px}
.f .row b{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.09em;text-transform:uppercase;
  color:var(--ink-3);font-weight:500;padding-top:2px}

/* tables */
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--raised)}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.09em;
  text-transform:uppercase;color:var(--ink-3);font-weight:500;padding:11px 14px;
  border-bottom:1px solid var(--line);background:var(--surface);white-space:nowrap;position:sticky;top:0}
td{padding:9px 14px;border-bottom:1px solid var(--line-soft);vertical-align:top}
tbody tr:last-child td{border-bottom:none}
.num{text-align:right;white-space:nowrap;font-family:"IBM Plex Mono",monospace}
.dim{color:var(--ink-3)}
.tag{display:inline-block;font-family:"IBM Plex Mono",monospace;font-size:10.5px;font-weight:500;
  padding:2px 7px;border-radius:3px;white-space:nowrap}
.tag.ok{background:var(--ok-bg);color:var(--ok)}
.tag.warn{background:var(--p1-bg);color:var(--p1)}
.tag.bad{background:var(--p0-bg);color:var(--p0)}
.tag.na{background:var(--surface);color:var(--ink-3)}
tr.r-bad td:first-child{box-shadow:inset 3px 0 var(--p0)}
tr.r-warn td:first-child{box-shadow:inset 3px 0 var(--p1)}
tr.r-ok td:first-child{box-shadow:inset 3px 0 var(--ok)}
.note-cell{color:var(--ink-3);font-size:12px;line-height:1.45;max-width:330px}
.star{color:var(--p1)}

.callout{background:var(--accent-soft);border:1px solid color-mix(in srgb,var(--accent) 30%,transparent);
  border-radius:10px;padding:16px 20px;font-size:14px;line-height:1.6;color:var(--ink-2);max-width:78ch}
.callout b{color:var(--ink)}
.steps{display:flex;flex-direction:column;gap:12px;counter-reset:s}
.step{display:grid;grid-template-columns:26px 1fr;gap:14px;align-items:start}
.step .i{font-family:"IBM Plex Mono",monospace;font-size:11px;font-weight:600;color:var(--accent);
  background:var(--accent-soft);border-radius:4px;height:22px;display:grid;place-items:center;margin-top:2px}
.step .b{font-size:14px;line-height:1.6;color:var(--ink-2)}
.step .b b{color:var(--ink);font-weight:600}
@media (max-width:640px){
  .wrap{padding:36px 18px 70px}
  .bar{grid-template-columns:88px 1fr 56px;gap:9px}
  .f .row{grid-template-columns:1fr;gap:2px}
}
</style>`;
}

export function reportBody({ spec, aliases, browser, warehouse, findings, stamp, days }) {
  const statuses = Object.values(aliases.map).reduce((a, v) => ((a[v.status] = (a[v.status] || 0) + 1), a), {});
  const totalSpec = Object.keys(aliases.map).length;
  const bySev = (s) => findings.filter((f) => f.severity === s);
  const wire = browser.events.filter((e) => e.source === 'wire');
  const types = {};
  for (const e of wire) (types[e.vendor] ||= new Set()).add(e.name);
  const maxTypes = Math.max(1, ...Object.values(types).map((s) => s.size));
  const when = stamp.replace('T', ' ').replace(/-(\d\d)-(\d\d)$/, ':$1:$2');

  const bars = ['posthog', 'ga4', 'meta', 'customerio']
    .filter((v) => types[v])
    .map((v) => {
      const c = types[v].size;
      const label = { posthog: 'PostHog', ga4: 'GA4', meta: 'Meta Pixel', customerio: 'Customer.io' }[v];
      return `<div class="bar"><span class="lbl">${label}</span>
        <span class="track"><span class="fill${v === 'posthog' ? '' : ' mute'}" style="width:${Math.round((c / maxTypes) * 100)}%"></span></span>
        <span class="val">${c} event${c === 1 ? '' : 's'}</span></div>`;
    }).join('');

  const findingCards = findings.map((f) => `
    <article class="f s-${f.severity}">
      <div class="top">
        <span class="chip">${f.severity}</span>
        <span class="chip cls">${esc(CLS[f.cls] ?? f.cls)}</span>
      </div>
      <div class="ttl">${md(f.title)}</div>
      <div class="ev">${md(f.evidence)}</div>
      <div class="row"><b>Impact</b><span>${md(f.impact)}</span></div>
      <div class="row"><b>Fix</b><span>${md(f.fix)}</span></div>
    </article>`).join('');

  const specRows = spec.events.map((e) => {
    const a = aliases.map[e.event] || {};
    const vol = warehouse?.volumes?.find((v) => v.event === a.posthog);
    const tone = STATUS_TONE[a.status] ?? 'na';
    return `<tr class="r-${tone}">
      <td><code>${esc(e.event)}</code>${e.critical ? ' <span class="star" title="north-star">★</span>' : ''}${e.upsell ? ' <span class="star" title="commercial intent">↑</span>' : ''}</td>
      <td class="dim">${esc(e.group)}</td>
      <td>${a.posthog ? `<code>${esc(a.posthog)}</code>` : a.gtm ? `<span class="dim">GTM: <code>${esc(a.gtm)}</code></span>` : '<span class="dim">—</span>'}</td>
      <td class="num">${vol ? n(vol.volume) : '<span class="dim">—</span>'}</td>
      <td><span class="tag ${tone}">${esc(a.status ?? 'unmapped')}</span></td>
      <td class="note-cell">${md(a.note ?? '')}</td>
    </tr>`;
  }).join('');

  const capturedRows = Object.entries(types).flatMap(([v, set]) =>
    [...set].map((name) => {
      const count = wire.filter((e) => e.vendor === v && e.name === name).length;
      return { v, name, count };
    })).sort((a, b) => b.count - a.count).map((r) => `
      <tr><td><code>${esc(r.name)}</code></td><td class="dim">${esc(r.v)}</td><td class="num">${r.count}</td></tr>`).join('');

  const journeyRows = browser.journeys.map((j) => `
    <tr><td>${esc(j.name)}</td>
      <td>${j.error ? '<span class="tag bad">error</span>'
        : j.result?.skipped ? `<span class="tag warn">skipped</span> <span class="dim">${esc(j.result.skipped)}</span>`
        : '<span class="tag ok">ran</span>'}</td>
      <td class="num">${n(wire.filter((e) => e.journey === j.id).length)}</td></tr>`).join('');

  return `
<div class="wrap">
  <p class="eyebrow">Instrumentation audit · inc42.com</p>
  <h1>What the website actually reports</h1>
  <p class="lede">Six user journeys driven through real Chrome, every outbound analytics payload decoded on the
  wire, and the result diffed against the ${totalSpec}-event tracking plan. Not what the code intends to send —
  what left the browser.</p>
  <div class="meta">
    <span>${esc(when)}</span>
    <span>${warehouse ? `PostHog ${esc(String(process.env.POSTHOG_PROJECT_ID || 53557))} · ${esc(warehouse.range.start)} → ${esc(warehouse.range.end)}` : 'browser-only run'}</span>
    <span>spec ${esc(spec.version)}</span>
    <span>${n(wire.length)} payloads captured</span>
  </div>

  <div class="thesis">
    <div class="t">Distinct event types received, per vendor, across the same six journeys</div>
    <div class="bars">${bars}</div>
    <p class="note">The marketing stack sees more of what users do than the product-analytics stack does.
    Every product decision made from PostHog is made on the thinner dataset — and
    <code>autocapture</code> and <code>capture_pageview</code> are both off, so nothing fills the gap automatically.</p>
  </div>

  <div class="tiles">
    <div class="tile"><span class="v">${totalSpec}</span><span class="l">Planned</span><span class="s">events in the spec</span></div>
    <div class="tile ok"><span class="v">${statuses.implemented ?? 0}</span><span class="l">Implemented</span><span class="s">fire as specified</span></div>
    <div class="tile p1"><span class="v">${statuses.partial ?? 0}</span><span class="l">Partial</span><span class="s">fire, wrong or thin</span></div>
    <div class="tile p0"><span class="v">${statuses.missing ?? 0}</span><span class="l">Missing</span><span class="s">nothing fires</span></div>
    <div class="tile p0"><span class="v">${bySev('P0').length}</span><span class="l">P0</span><span class="s">${SEV_NOTE.P0}</span></div>
    <div class="tile p1"><span class="v">${bySev('P1').length}</span><span class="l">P1</span><span class="s">${SEV_NOTE.P1}</span></div>
    <div class="tile"><span class="v">${bySev('P2').length}</span><span class="l">P2</span><span class="s">${SEV_NOTE.P2}</span></div>
    <div class="tile acc"><span class="v">${Object.keys(types).length}</span><span class="l">Vendors</span><span class="s">seen on the wire</span></div>
  </div>

  <div class="h2wrap"><h2>Findings</h2>
    <p class="h2sub">Ranked by whether the defect blocks a decision, distorts a number, or is hygiene.</p></div>
  <div class="findings">${findingCards || '<p class="dim">No findings.</p>'}</div>

  ${!warehouse ? `<div class="h2wrap"><h2>What a PostHog key would resolve</h2>
    <p class="h2sub">This run captured the browser half only.</p></div>
    <div class="callout"><b>${bySev('P2').filter((f) => f.cls === 'UNVERIFIED').length} findings are unresolved because no warehouse query ran.</b>
    Without it, an event absent from a journey is ambiguous: it may be broken, or the journey may simply
    never have reached its trigger. More importantly, a browser-only run cannot detect the most expensive
    failure mode of all — an event that fires perfectly, looks correct in devtools, and never arrives.
    Set <code>POSTHOG_API_KEY</code> and re-run to close both.</div>` : ''}

  <div class="h2wrap"><h2>Spec coverage</h2>
    <p class="h2sub">All ${totalSpec} planned events against what production actually sends.
    ★ north-star · ↑ commercial intent.</p></div>
  <div class="scroll"><table>
    <thead><tr><th>Spec event</th><th>Group</th><th>Live name</th><th class="num">30d vol</th><th>Status</th><th>Note</th></tr></thead>
    <tbody>${specRows}</tbody></table></div>

  <div class="h2wrap"><h2>What was captured</h2>
    <p class="h2sub">Every distinct event decoded off the wire during this run.</p></div>
  <div class="scroll"><table>
    <thead><tr><th>Event</th><th>Vendor</th><th class="num">Captures</th></tr></thead>
    <tbody>${capturedRows}</tbody></table></div>

  <div class="h2wrap"><h2>Journeys</h2></div>
  <div class="scroll"><table>
    <thead><tr><th>Journey</th><th>Outcome</th><th class="num">Payloads</th></tr></thead>
    <tbody>${journeyRows}</tbody></table></div>

  ${warehouse ? `<div class="h2wrap"><h2>Top live events</h2>
    <p class="h2sub">Highest-volume events in PostHog over ${days} days, and whether the plan knows about them.</p></div>
  <div class="scroll"><table>
    <thead><tr><th>Event</th><th class="num">Volume</th><th class="num">Persons</th><th class="num">Per day</th><th>In plan?</th></tr></thead>
    <tbody>${warehouse.volumes.slice(0, 40).map((v) => {
      const mapped = Object.values(aliases.map).some((a) => a.posthog === v.event);
      return `<tr><td><code>${esc(v.event)}</code></td><td class="num">${n(v.volume)}</td><td class="num">${n(v.persons)}</td><td class="num">${(Number(v.per_day) || 0).toFixed(1)}</td><td>${mapped ? '<span class="tag ok">yes</span>' : '<span class="tag warn">no</span>'}</td></tr>`;
    }).join('')}</tbody></table></div>` : ''}

  <div class="h2wrap"><h2>Method</h2>
    <p class="h2sub">Why this catches things a devtools sweep does not.</p></div>
  <div class="steps">
    <div class="step"><span class="i">1</span><span class="b"><b>Drive.</b> Playwright runs real Chrome through scripted journeys. The site serves HTTP&nbsp;201 and <code>application/octet-stream</code> to any <code>HeadlessChrome</code> user-agent, so the runner overrides it — worth knowing before you point any synthetic monitor at inc42.com.</span></div>
    <div class="step"><span class="i">2</span><span class="b"><b>Decode.</b> Every outbound request is intercepted in Node and parsed per vendor: PostHog's gzip/base64 batches, GA4 Measurement Protocol, Meta Pixel query params, Customer.io's Segment-shaped body. The wire is ground truth; the console only shows what the site chose to log.</span></div>
    <div class="step"><span class="i">3</span><span class="b"><b>Observe.</b> A probe injected before any page script wraps <code>posthog.capture</code>, <code>analytics.track</code>, <code>fbq</code> and <code>dataLayer.push</code> at the call site, so arguments dropped before the network are still visible. It streams to Node, because in-page buffers die on every navigation.</span></div>
    <div class="step"><span class="i">4</span><span class="b"><b>Verify.</b> HogQL queries this run's own <code>distinct_id</code>s to prove the events landed, plus 30-day volumes, property coverage and enum values.</span></div>
    <div class="step"><span class="i">5</span><span class="b"><b>Diff.</b> Results are classified against the spec. The alias layer is what makes this possible: the plan is snake_case, production is Title Case, and only 2 of ${totalSpec} names match on their own.</span></div>
  </div>
</div>`;
}

export function renderReport(data) {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Inc42 Event Audit</title>
${reportStyles()}</head><body>${reportBody(data)}</body></html>`;
}
