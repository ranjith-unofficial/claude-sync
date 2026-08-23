const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const md = (s) => esc(s).replace(/`([^`]+)`/g, '<code>$1</code>');
const n = (x) => (Number(x) || 0).toLocaleString('en-IN');

const SEV = { P0: ['#b3261e', 'Blocks decisions'], P1: ['#a15c00', 'Distorts numbers'], P2: ['#4a5568', 'Hygiene'] };
const CLS_LABEL = {
  NEVER_FIRES: 'Never fires', FIRES_NOT_LANDED: 'Fires, never lands', GTM_ONLY: 'Ads-only',
  DOUBLE_FIRE: 'Double-fire', PROP_MISSING: 'Missing properties', PROP_COVERAGE: 'Thin coverage',
  NAME_DRIFT: 'Name drift', IDENTITY: 'Identity', PII_LEAK: 'PII', VENDOR_ASYMMETRY: 'Vendor asymmetry',
  ZOMBIE: 'Zombie event', NOISE: 'Noise', UNSPECIFIED: 'Unplanned event', RULE_ERROR: 'Rule error',
};

export function renderReport({ spec, aliases, browser, warehouse, findings, stamp, days }) {
  const statuses = Object.values(aliases.map).reduce((a, v) => ((a[v.status] = (a[v.status] || 0) + 1), a), {});
  const total = Object.keys(aliases.map).length;
  const bySev = (s) => findings.filter((f) => f.severity === s);
  const wire = browser.events.filter((e) => e.source === 'wire');
  const vendors = wire.reduce((a, e) => ((a[e.vendor] = (a[e.vendor] || 0) + 1), a), {});

  const tile = (label, value, sub, tone = '') =>
    `<div class="tile ${tone}"><div class="v">${value}</div><div class="l">${esc(label)}</div>${sub ? `<div class="s">${md(sub)}</div>` : ''}</div>`;

  const findingRows = findings.map((f) => `
    <tr class="sev-${f.severity}">
      <td class="sev"><span class="pill" style="--c:${SEV[f.severity][0]}">${f.severity}</span></td>
      <td class="cls">${esc(CLS_LABEL[f.cls] ?? f.cls)}</td>
      <td>
        <div class="t">${md(f.title)}</div>
        <div class="e">${md(f.evidence)}</div>
        <div class="i"><b>Impact</b> ${md(f.impact)}</div>
        <div class="fx"><b>Fix</b> ${md(f.fix)}</div>
      </td>
    </tr>`).join('');

  const specRows = spec.events.map((e) => {
    const a = aliases.map[e.event] || {};
    const vol = warehouse?.volumes?.find((v) => v.event === a.posthog);
    const cls = { implemented: 'ok', partial: 'warn', gtm_only: 'warn', missing: 'bad', server_side: 'na' }[a.status] ?? 'na';
    return `<tr class="${cls}">
      <td><code>${esc(e.event)}</code>${e.critical ? ' <span class="star">★</span>' : ''}</td>
      <td class="g">${esc(e.group)}</td>
      <td>${a.posthog ? `<code>${esc(a.posthog)}</code>` : a.gtm ? `<span class="dim">GTM only: <code>${esc(a.gtm)}</code></span>` : '<span class="dim">—</span>'}</td>
      <td class="num">${vol ? n(vol.volume) : '<span class="dim">—</span>'}</td>
      <td><span class="tag ${cls}">${esc(a.status ?? 'unmapped')}</span></td>
      <td class="note">${md(a.note ?? '')}</td>
    </tr>`;
  }).join('');

  const journeyRows = browser.journeys.map((j) => `
    <tr><td><b>${esc(j.name)}</b></td>
    <td>${j.error ? `<span class="tag bad">error</span> <span class="dim">${esc(j.error.split('\n')[0].slice(0, 120))}</span>`
      : j.result?.skipped ? `<span class="tag warn">skipped</span> <span class="dim">${esc(j.result.skipped)}</span>`
      : '<span class="tag ok">ran</span>'}</td>
    <td class="num">${n(browser.events.filter((e) => e.journey === j.id && e.source === 'wire').length)}</td></tr>`).join('');

  return `<!doctype html><meta charset="utf-8">
<title>Inc42 Event Audit — ${esc(stamp)}</title>
<style>
:root{--bg:#fff;--fg:#16191d;--dim:#6b7280;--line:#e5e7eb;--card:#f9fafb;--ok:#0f7b3f;--warn:#a15c00;--bad:#b3261e}
@media(prefers-color-scheme:dark){:root{--bg:#101215;--fg:#e8eaed;--dim:#9aa2ad;--line:#282c33;--card:#181b1f;--ok:#4ade80;--warn:#fbbf24;--bad:#f87171}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:40px 24px 80px}
h1{font-size:27px;margin:0 0 4px;letter-spacing:-.02em}h2{font-size:19px;margin:44px 0 14px;letter-spacing:-.01em}
.sub{color:var(--dim);font-size:14px;margin-bottom:28px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(158px,1fr));gap:12px;margin:24px 0}
.tile{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.tile .v{font-size:26px;font-weight:640;letter-spacing:-.02em}.tile .l{font-size:12px;color:var(--dim);text-transform:uppercase;letter-spacing:.05em;margin-top:2px}
.tile .s{font-size:12px;color:var(--dim);margin-top:6px}
.tile.bad .v{color:var(--bad)}.tile.warn .v{color:var(--warn)}.tile.ok .v{color:var(--ok)}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--dim);padding:8px 10px;border-bottom:1px solid var(--line);font-weight:600}
td{padding:11px 10px;border-bottom:1px solid var(--line);vertical-align:top}
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:10px}
code{font:12.5px ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--card);padding:1px 5px;border-radius:4px}
.pill{display:inline-block;color:#fff;background:var(--c);border-radius:5px;padding:2px 7px;font-size:11px;font-weight:650}
.tag{display:inline-block;border-radius:5px;padding:2px 7px;font-size:11px;font-weight:600;border:1px solid currentColor}
.tag.ok{color:var(--ok)}.tag.warn{color:var(--warn)}.tag.bad{color:var(--bad)}.tag.na{color:var(--dim)}
.t{font-weight:620;margin-bottom:3px}.e{color:var(--dim);font-size:13px}
.i,.fx{font-size:12.5px;margin-top:5px}.i b,.fx b{font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--dim);margin-right:5px}
.sev{white-space:nowrap;width:1%}.cls{white-space:nowrap;color:var(--dim);font-size:12px;width:1%}
.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.dim{color:var(--dim)}.g{color:var(--dim);font-size:12px}.note{color:var(--dim);font-size:12px;max-width:340px}
.star{color:var(--warn)}
tr.bad td:first-child{box-shadow:inset 3px 0 var(--bad)}tr.warn td:first-child{box-shadow:inset 3px 0 var(--warn)}tr.ok td:first-child{box-shadow:inset 3px 0 var(--ok)}
.note-box{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--warn);border-radius:8px;padding:12px 16px;font-size:13.5px;color:var(--dim);margin:16px 0}
</style>
<div class="wrap">
<h1>Inc42 web — analytics event audit</h1>
<div class="sub">${esc(stamp.replace('T', ' ').replace(/-/g, ':').replace(/^(\d+):(\d+):(\d+)/, '$1-$2-$3'))} ·
${warehouse ? `PostHog project ${esc(process.env.POSTHOG_PROJECT_ID || '53557')} · ${esc(warehouse.range.start)} → ${esc(warehouse.range.end)} (${days}d)` : 'browser-only run (no warehouse verification)'} ·
spec ${esc(spec.version)}</div>

<div class="tiles">
  ${tile('Spec events', total, 'in the tracking plan')}
  ${tile('Implemented', statuses.implemented ?? 0, 'fire correctly', 'ok')}
  ${tile('Partial', statuses.partial ?? 0, 'fire, but wrong or thin', 'warn')}
  ${tile('Missing', statuses.missing ?? 0, 'nothing fires at all', 'bad')}
  ${tile('P0 findings', bySev('P0').length, SEV.P0[1], 'bad')}
  ${tile('P1 findings', bySev('P1').length, SEV.P1[1], 'warn')}
  ${tile('Wire events', n(wire.length), 'captured this run')}
  ${tile('Vendors seen', Object.keys(vendors).length, Object.entries(vendors).map(([k, v]) => `${k} ${v}`).join(' · ') || '—')}
</div>

${!warehouse ? '<div class="note-box"><b>Browser-only run.</b> Nothing here proves ingestion. Set <code>POSTHOG_API_KEY</code> and re-run to close the loop — that is the only way to catch events that fire correctly and never land.</div>' : ''}

<h2>Findings</h2>
<div class="scroll"><table>
<thead><tr><th>Sev</th><th>Class</th><th>Finding</th></tr></thead>
<tbody>${findingRows || '<tr><td colspan="3" class="dim">No findings.</td></tr>'}</tbody>
</table></div>

<h2>Journeys run</h2>
<div class="scroll"><table>
<thead><tr><th>Journey</th><th>Outcome</th><th class="num">Wire events</th></tr></thead>
<tbody>${journeyRows || '<tr><td colspan="3" class="dim">No journeys run.</td></tr>'}</tbody>
</table></div>

<h2>Spec coverage — all ${total} planned events</h2>
<div class="scroll"><table>
<thead><tr><th>Spec event</th><th>Group</th><th>Live name</th><th class="num">30d volume</th><th>Status</th><th>Note</th></tr></thead>
<tbody>${specRows}</tbody>
</table></div>

${warehouse ? `<h2>Top live events (${days}d)</h2><div class="scroll"><table>
<thead><tr><th>Event</th><th class="num">Volume</th><th class="num">Persons</th><th class="num">Per day</th><th>Last seen</th><th>In plan?</th></tr></thead>
<tbody>${warehouse.volumes.slice(0, 40).map((v) => {
    const mapped = Object.values(aliases.map).some((a) => a.posthog === v.event);
    return `<tr><td><code>${esc(v.event)}</code></td><td class="num">${n(v.volume)}</td><td class="num">${n(v.persons)}</td><td class="num">${(Number(v.per_day) || 0).toFixed(1)}</td><td class="dim">${esc(String(v.last_seen).slice(0, 16))}</td><td>${mapped ? '<span class="tag ok">yes</span>' : '<span class="tag warn">no</span>'}</td></tr>`;
  }).join('')}</tbody></table></div>` : ''}

</div>`;
}
