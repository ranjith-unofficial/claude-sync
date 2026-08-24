const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const md = (s) => esc(s).replace(/`([^`]+)`/g, '<code>$1</code>');
const n = (x) => (Number(x) || 0).toLocaleString('en-IN');

const CLS = {
  NOT_INSTRUMENTED: 'Not instrumented', NEVER_FIRES: 'Never fires', NOT_REPRODUCED: 'Not reproduced',
  UNVERIFIED: 'Unverified', FIRES_NOT_LANDED: 'Fires, never lands', COVERAGE_GAP: 'Coverage gap',
  VENDOR_BALANCE: 'Vendor balance', VENDOR_ASYMMETRY: 'Vendor asymmetry', GTM_ONLY: 'Ads-only',
  DOUBLE_FIRE: 'Double-fire', PROP_MISSING: 'Missing properties', PROP_COVERAGE: 'Thin coverage',
  NAME_DRIFT: 'Name drift', IDENTITY: 'Identity', NEVER_IDENTIFIED: 'Not identified', PII_LEAK: 'PII',
  ZOMBIE: 'Zombie event', NOISE: 'Noise', UNSPECIFIED: 'Unplanned event', PAGE_ERROR: 'Page error',
  RULE_ERROR: 'Rule error',
};
const STATUS_LABEL = { implemented: 'OK', partial: 'Partial', gtm_only: 'Ads only', missing: 'Missing', server_side: 'Server' };

export function reportStyles() {
  return `
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{
  --bg:#ffffff; --panel:#fafafa; --line:#e2e2e2;
  --ink:#1a1a1a; --ink-2:#555555; --ink-3:#8a8a8a;
  --p0:#b42318; --p1:#b54708; --p2:#667085; --ok:#12762d;
  --p0-bg:#fef3f2; --p1-bg:#fffaeb; --p2-bg:#f2f4f7; --ok-bg:#ecfdf3;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#111214; --panel:#17181b; --line:#2b2d31;
  --ink:#eaeaea; --ink-2:#a8a8a8; --ink-3:#77797d;
  --p0:#f97066; --p1:#f79009; --p2:#84878c; --ok:#32d583;
  --p0-bg:#2a1615; --p1-bg:#2a1f0e; --p2-bg:#1e1f22; --ok-bg:#0f2419;
}}
:root[data-theme="dark"]{
  --bg:#111214; --panel:#17181b; --line:#2b2d31;
  --ink:#eaeaea; --ink-2:#a8a8a8; --ink-3:#77797d;
  --p0:#f97066; --p1:#f79009; --p2:#84878c; --ok:#32d583;
  --p0-bg:#2a1615; --p1-bg:#2a1f0e; --p2-bg:#1e1f22; --ok-bg:#0f2419;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:400 14px/1.55 Inter,-apple-system,sans-serif;font-variant-numeric:tabular-nums}
.wrap{max-width:980px;margin:0 auto;padding:40px 24px 90px}
code{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:.88em;background:var(--panel);border:1px solid var(--line);padding:0 .35em;border-radius:3px;color:var(--ink-2)}

h1{font-size:22px;font-weight:700;margin:0 0 6px;letter-spacing:-.01em}
.sub{color:var(--ink-2);font-size:13.5px;max-width:70ch;margin:0 0 14px}
.meta{font-size:12px;color:var(--ink-3);border-top:1px solid var(--line);border-bottom:1px solid var(--line);
  padding:8px 0;margin:16px 0 30px;display:flex;flex-wrap:wrap;gap:4px 20px}
.meta b{color:var(--ink-2);font-weight:500}

h2{font-size:15px;font-weight:700;margin:38px 0 4px;padding-bottom:8px;border-bottom:1px solid var(--ink);letter-spacing:-.005em}
.h2sub{color:var(--ink-3);font-size:12.5px;margin:0 0 12px}

/* summary strip - plain, no color blocks */
.summary{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:0;
  border:1px solid var(--line);border-radius:6px;overflow:hidden;margin:18px 0 0}
.summary div{padding:12px 14px;border-right:1px solid var(--line)}
.summary div:last-child{border-right:none}
.summary .n{font-size:20px;font-weight:700;line-height:1.1}
.summary .l{font-size:11px;color:var(--ink-3);margin-top:3px}
.summary .p0 .n{color:var(--p0)}.summary .p1 .n{color:var(--p1)}.summary .ok .n{color:var(--ok)}

table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;font-size:11px;font-weight:600;color:var(--ink-3);text-transform:uppercase;letter-spacing:.03em;
  padding:8px 10px;border-bottom:1px solid var(--ink);white-space:nowrap}
td{padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}
tbody tr:last-child td{border-bottom:none}
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:6px}
.num{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
.dim{color:var(--ink-3)}

/* severity: text label, not a colored block */
.sev{font-weight:700;font-size:11.5px;white-space:nowrap}
.sev.P0{color:var(--p0)}.sev.P1{color:var(--p1)}.sev.P2{color:var(--ink-3)}

.badge{display:inline-block;font-size:11px;font-weight:600;padding:1px 6px;border-radius:3px;white-space:nowrap;border:1px solid var(--line)}
.badge.ok{color:var(--ok);border-color:var(--ok)}
.badge.warn{color:var(--p1);border-color:var(--p1)}
.badge.bad{color:var(--p0);border-color:var(--p0)}
.badge.na{color:var(--ink-3)}

.note{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--p1);border-radius:4px;
  padding:10px 14px;font-size:13px;color:var(--ink-2);margin:14px 0;max-width:78ch}
.note b{color:var(--ink)}

ul.plain{margin:6px 0 0;padding-left:20px}
ul.plain li{margin:3px 0;color:var(--ink-2);font-size:13px}
ul.plain li b{color:var(--ink);font-weight:600}

@media (max-width:640px){.wrap{padding:24px 14px 60px}}
</style>`;
}

export function reportBody({ spec, aliases, browser, warehouse, findings, drift = [], stamp, days }) {
  const statuses = Object.values(aliases.map).reduce((a, v) => ((a[v.status] = (a[v.status] || 0) + 1), a), {});
  const totalSpec = Object.keys(aliases.map).length;
  const bySev = (s) => findings.filter((f) => f.severity === s);
  const wire = browser.events.filter((e) => e.source === 'wire' && !e.replayed);
  const types = {};
  for (const e of wire) (types[e.vendor] ||= new Set()).add(e.name);
  const when = stamp.replace('T', ' ').replace(/-(\d\d)-(\d\d)$/, ':$1:$2');

  const findingRows = findings.map((f) => `
    <tr>
      <td><span class="sev ${f.severity}">${f.severity}</span></td>
      <td class="dim">${esc(CLS[f.cls] ?? f.cls)}</td>
      <td>
        <div><b>${md(f.title)}</b></div>
        <div class="dim" style="margin-top:3px">${md(f.evidence)}</div>
        <div style="margin-top:5px"><span class="dim">Impact:</span> ${md(f.impact)}</div>
        <div style="margin-top:2px"><span class="dim">Fix:</span> ${md(f.fix)}</div>
      </td>
    </tr>`).join('');

  const driftRows = drift.map((d) => {
    const badge = { misrouted: 'bad', 'regressed since June': 'bad', unchanged: 'warn',
                    new: 'warn', 'improved since June': 'ok' }[d.verdict] ?? 'na';
    const obs = wire.filter((e) => e.name === d.event);
    const byV = obs.reduce((a, e) => ((a[e.vendor] = (a[e.vendor] || 0) + 1), a), {});
    const seenTxt = Object.keys(byV).length
      ? Object.entries(byV).map(([v, c]) => `${v} ×${c}`).join(', ') : '<span class="dim">nothing</span>';
    return `<tr>
      <td><code>${esc(d.event)}</code></td>
      <td class="dim">${esc(String(d.junStatus ?? ''))}</td>
      <td class="num">${d.junVol ? n(d.junVol) : '<span class="dim">—</span>'}</td>
      <td>${seenTxt}</td>
      <td><span class="badge ${badge}">${esc(d.verdict)}</span></td>
      <td class="dim">${md(d.title)}</td>
    </tr>`;
  }).join('');

  const specRows = spec.events.map((e) => {
    const a = aliases.map[e.event] || {};
    const vol = warehouse?.volumes?.find((v) => v.event === a.posthog);
    const badge = { implemented: 'ok', partial: 'warn', gtm_only: 'warn', missing: 'bad', server_side: 'na' }[a.status] ?? 'na';
    return `<tr>
      <td><code>${esc(e.event)}</code>${e.critical ? ' ★' : e.upsell ? ' ↑' : ''}</td>
      <td class="dim">${esc(e.group)}</td>
      <td>${a.posthog ? `<code>${esc(a.posthog)}</code>` : a.gtm ? `<span class="dim">GTM: <code>${esc(a.gtm)}</code></span>` : '<span class="dim">—</span>'}</td>
      <td class="num">${vol ? n(vol.volume) : '<span class="dim">—</span>'}</td>
      <td><span class="badge ${badge}">${STATUS_LABEL[a.status] ?? a.status ?? '—'}</span></td>
      <td class="dim" style="max-width:300px">${md(a.note ?? '')}</td>
    </tr>`;
  }).join('');

  const journeyRows = browser.journeys.map((j) => `
    <tr><td>${esc(j.name)}</td>
      <td>${j.error ? '<span class="badge bad">error</span>'
        : j.result?.skipped ? `<span class="badge warn">skipped</span> <span class="dim">${esc(j.result.skipped)}</span>`
        : '<span class="badge ok">ran</span>'}</td>
      <td class="num">${n(wire.filter((e) => e.journey === j.id).length)}</td></tr>`).join('');

  return `
<div class="wrap">
  <h1>Inc42 web — analytics event audit</h1>
  <div class="sub">${wire.length.toLocaleString()} payloads decoded across ${browser.journeys.length} journeys, checked against the June 2026 warehouse audit and the ${totalSpec}-event spec.</div>
  <div class="meta">
    <span><b>Run</b> ${esc(when)}</span>
    <span><b>Source</b> ${warehouse ? `PostHog ${esc(String(process.env.POSTHOG_PROJECT_ID || 53557))}, ${esc(warehouse.range.start)}–${esc(warehouse.range.end)}` : 'browser-only'}</span>
    <span><b>Spec</b> ${esc(spec.version)}</span>
  </div>

  <div class="summary">
    <div><div class="n">${totalSpec}</div><div class="l">Spec events</div></div>
    <div class="ok"><div class="n">${statuses.implemented ?? 0}</div><div class="l">Implemented</div></div>
    <div class="p1"><div class="n">${statuses.partial ?? 0}</div><div class="l">Partial</div></div>
    <div class="p0"><div class="n">${statuses.missing ?? 0}</div><div class="l">Missing</div></div>
    <div class="p0"><div class="n">${bySev('P0').length}</div><div class="l">P0 findings</div></div>
    <div class="p1"><div class="n">${bySev('P1').length}</div><div class="l">P1 findings</div></div>
    <div><div class="n">${Object.keys(types).length}</div><div class="l">Vendors seen</div></div>
  </div>

  <div class="note"><b>Headline:</b> across the same journeys, GA4 receives more distinct event types than PostHog receives, and an authenticated session never called <code>identify()</code> — signed in on the site, anonymous in analytics. Details below.</div>

  ${drift.length ? `<h2>Re-audit vs June 2026</h2>
  <p class="h2sub">Every event from the Master sheet's latest tab ("Audit | Jun 2026"), re-tested live. "Unchanged / new" rows are real findings; anything not listed here was either confirmed still working or could not be reached by any journey.</p>
  <div class="scroll"><table>
    <thead><tr><th>Event</th><th>June status</th><th class="num">June 30d</th><th>Seen this run</th><th>Verdict</th><th>Meaning</th></tr></thead>
    <tbody>${driftRows}</tbody></table></div>` : ''}

  <h2>Findings</h2>
  <p class="h2sub">Ranked P0 (blocks decisions) → P1 (distorts numbers) → P2 (hygiene / unresolved).</p>
  <div class="scroll"><table>
    <thead><tr><th>Sev</th><th>Class</th><th>Finding</th></tr></thead>
    <tbody>${findingRows || '<tr><td colspan="3" class="dim">No findings.</td></tr>'}</tbody>
  </table></div>

  <h2>Spec coverage</h2>
  <p class="h2sub">All ${totalSpec} planned events. ★ north-star, ↑ commercial intent.</p>
  <div class="scroll"><table>
    <thead><tr><th>Spec event</th><th>Group</th><th>Live name</th><th class="num">30d vol</th><th>Status</th><th>Note</th></tr></thead>
    <tbody>${specRows}</tbody></table></div>

  <h2>Journeys run</h2>
  <div class="scroll"><table>
    <thead><tr><th>Journey</th><th>Outcome</th><th class="num">Payloads</th></tr></thead>
    <tbody>${journeyRows}</tbody></table></div>

  ${warehouse ? `<h2>Top live events (${days}d)</h2>
  <div class="scroll"><table>
    <thead><tr><th>Event</th><th class="num">Volume</th><th class="num">Persons</th><th class="num">Per day</th><th>In plan?</th></tr></thead>
    <tbody>${warehouse.volumes.slice(0, 40).map((v) => {
      const mapped = Object.values(aliases.map).some((a) => a.posthog === v.event);
      return `<tr><td><code>${esc(v.event)}</code></td><td class="num">${n(v.volume)}</td><td class="num">${n(v.persons)}</td><td class="num">${(Number(v.per_day) || 0).toFixed(1)}</td><td>${mapped ? '<span class="badge ok">yes</span>' : '<span class="badge warn">no</span>'}</td></tr>`;
    }).join('')}</tbody></table></div>` : ''}

  <h2>Method</h2>
  <ul class="plain">
    <li><b>Drive.</b> Playwright runs real Chrome through scripted journeys. inc42.com serves HTTP 201 + <code>application/octet-stream</code> to a <code>HeadlessChrome</code> UA, so the runner overrides it.</li>
    <li><b>Decode.</b> Every outbound request is intercepted in Node and parsed per vendor — PostHog's gzip/base64 batches, GA4 Measurement Protocol, Meta Pixel, Customer.io. The wire is ground truth, not the console.</li>
    <li><b>Observe.</b> A probe wraps <code>posthog.capture</code>, <code>analytics.track</code>, <code>fbq</code>, <code>dataLayer.push</code> at the call site and streams to Node, since in-page buffers die on navigation.</li>
    <li><b>Verify.</b> HogQL queries this run's own <code>distinct_id</code>s to prove events landed, plus 30-day volumes and property coverage.</li>
    <li><b>Diff.</b> Classified against the spec and against the June 2026 audit. The alias layer (plan is snake_case, production is Title Case) makes the join possible — only 2 of ${totalSpec} names matched automatically.</li>
  </ul>
</div>`;
}

export function renderReport(data) {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Inc42 Event Audit</title>
${reportStyles()}</head><body>${reportBody(data)}</body></html>`;
}
