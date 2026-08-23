/* Re-audit rules referenced against 'Audit | Jun 2026' — the latest tab of the Master sheet.
   The question these answer is not "does the spec match production" but
   "is the June audit still true two months on, and what moved?" */

const P0 = 'P0', P1 = 'P1', P2 = 'P2';
let seq = 0;
const F = (o) => ({ id: `M${String(++seq).padStart(3, '0')}`, ...o });
const norm = (k) => String(k).toLowerCase().replace(/[^a-z0-9]/g, '');

/** Build: live event name -> what the browser saw, split by vendor. */
function observed(browser) {
  const out = {};
  for (const e of browser.events) {
    if (e.replayed || e.source !== 'wire') continue;
    const k = norm(e.name);
    (out[k] ||= { name: e.name, vendors: {}, count: 0, props: new Set() });
    out[k].vendors[e.vendor] = (out[k].vendors[e.vendor] || 0) + 1;
    out[k].count++;
    for (const p of Object.keys(e.props || {})) out[k].props.add(p);
  }
  return out;
}

export function runMasterRules({ live, coverage, browser, warehouse }) {
  seq = 0;
  const obs = observed(browser);
  const cov = coverage.map;
  const ranJourneys = new Set(
    browser.journeys.filter((j) => !j.error && !j.result?.skipped).map((j) => j.id));
  const results = Object.fromEntries(browser.journeys.map((j) => [j.id, j.result || {}]));

  /* A journey can run start to finish without ever reaching the condition it exists to test —
     eight articles read and the freewall never rendered, for instance. Calling that a regression
     would be a fabricated finding, so the precondition gates the verdict. */
  const triggerReached = (c) => {
    if (!c.requires) return true;
    const v = results[c.requires.journey]?.[c.requires.field];
    return Boolean(v);
  };
  const out = [];

  for (const ev of live.events) {
    const name = ev.live_name;
    if (!name || ev.noise) continue;
    const c = cov[name] || {};
    const seen = obs[norm(name)];
    const junVol = Number(ev.volume_30d) || 0;

    // ── not reachable by any journey: report as coverage, never as a defect
    if (!c.journey) {
      if (ev.missing || ev.dead) {
        out.push(F({
          cls: 'STILL_BROKEN_UNVERIFIED', severity: P2, event: name,
          junStatus: ev.status, junVol, verdict: 'unchanged, unverified',
          title: `${name} — June flagged it, no journey can reach it`,
          evidence: `June 2026: ${ev.status} (${junVol.toLocaleString()}/30d). ${c.why || 'No journey drives this trigger.'}`,
          impact: ev.findings || 'Cannot confirm or clear without driving the trigger.',
          fix: ev.fix || 'Needs a session or an action this audit deliberately does not perform.',
        }));
      }
      continue;
    }

    // ── journey exists but did not run (skipped/errored, e.g. no credentials)
    if (!ranJourneys.has(c.journey)) {
      out.push(F({
        cls: 'NOT_RUN', severity: P2, event: name,
        junStatus: ev.status, junVol, verdict: 'not tested',
        title: `${name} — its journey did not run`,
        evidence: `Covered by the "${c.journey}" journey, which was skipped or errored this run.`,
        impact: 'June status carries forward untested.',
        fix: c.journey === 'logged-in' ? 'Set INC42_EMAIL / INC42_PASSWORD in .env and re-run.' : `Repair the "${c.journey}" journey.`,
      }));
      continue;
    }

    if (!triggerReached(c)) {
      out.push(F({
        cls: 'NOT_TRIGGERED', severity: P2, event: name,
        junStatus: ev.status, junVol, verdict: 'not tested',
        title: `${name} — the trigger never occurred`,
        evidence: `The "${c.journey}" journey ran but \`${c.requires.field}\` was falsy, so ${c.trigger} never happened. `
          + `June 2026: ${ev.status} (${junVol.toLocaleString()}/30d).`,
        impact: 'No evidence either way. Not a defect.',
        fix: `Make the "${c.journey}" journey reach ${c.trigger}, then re-run.`,
      }));
      continue;
    }

    const toPostHog = seen?.vendors?.posthog ?? 0;
    const toOthers = seen ? Object.entries(seen.vendors).filter(([v]) => v !== 'posthog') : [];

    // ── fires, but to the wrong stack
    if (!toPostHog && toOthers.length) {
      out.push(F({
        cls: 'WRONG_DESTINATION', severity: P0, event: name,
        junStatus: ev.status, junVol, verdict: 'misrouted',
        title: `${name} fires to ${toOthers.map(([v]) => v).join('/')}, not to PostHog`,
        evidence: `Observed ${toOthers.map(([v, n]) => `${n}× to ${v}`).join(', ')} in the "${c.journey}" journey; 0× to PostHog. `
          + `June recorded ${junVol.toLocaleString()}/30d in PostHog and called it "${ev.status}".`,
        impact: `The June audit read its own low volume as a firing problem. It is a routing problem: the event fires reliably, into the wrong tool.`,
        fix: 'Mirror to PostHog through the shared transform layer.',
      }));
      continue;
    }

    // ── observed reaching PostHog
    if (toPostHog) {
      if (ev.dead || ev.missing) {
        out.push(F({
          cls: 'RECOVERED', severity: P2, event: name,
          junStatus: ev.status, junVol, verdict: 'improved since June',
          title: `${name} is firing again`,
          evidence: `June 2026: ${ev.status} (${junVol.toLocaleString()}/30d). Observed ${toPostHog}× to PostHog in the "${c.journey}" journey.`,
          impact: 'The June finding is stale — re-check before acting on it.',
          fix: 'Confirm volume in PostHog, then close the June item.',
        }));
      }
      continue;
    }

    // ── nothing at all, though the journey ran and should have triggered it
    const wasHealthy = ev.healthy && junVol > 1000;
    out.push(F({
      cls: wasHealthy ? 'REGRESSED' : 'STILL_BROKEN', severity: wasHealthy ? P0 : P1, event: name,
      junStatus: ev.status, junVol, verdict: wasHealthy ? 'regressed since June' : 'unchanged',
      title: wasHealthy
        ? `${name} was healthy in June and did not fire at all`
        : `${name} is still not firing`,
      evidence: `June 2026: ${ev.status} (${junVol.toLocaleString()}/30d). The "${c.journey}" journey ran and drove ${c.trigger}, and produced 0 captures on any vendor.`,
      impact: (wasHealthy
        ? 'Either a regression since June, or the June volume comes from a trigger path this journey does not represent. Both need answering.'
        : (ev.findings || 'The metric this event serves still has no data.'))
        + (c.navigates ? ' NOTE: this click navigates away, so an unflushed batch is a plausible alternative explanation — check for sendBeacon on pagehide before assuming a missing handler.' : ''),
      fix: ev.fix || `Check the handler for ${name}.`,
    }));
  }

  // ── live now, absent from the June tab entirely
  const known = new Set(live.events.map((e) => norm(e.live_name || '')));
  for (const [k, v] of Object.entries(obs)) {
    if (known.has(k) || v.name.startsWith('$') || v.count < 2) continue;
    out.push(F({
      cls: 'NEW_SINCE_JUNE', severity: P1, event: v.name,
      junStatus: 'absent', junVol: 0, verdict: 'new',
      title: `${v.name} is live but absent from the June audit`,
      evidence: `${v.count} captures this run (${Object.entries(v.vendors).map(([a, b]) => `${a} ${b}`).join(', ')}). Not listed anywhere in 'Audit | Jun 2026'.`,
      impact: 'Shipped after June, or missed by it. Either way nobody owns its schema.',
      fix: 'Add to the register with an owner and a property contract, or deprecate.',
    }));
  }

  const order = { P0: 0, P1: 1, P2: 2 };
  const seenKey = new Set();
  return out
    .filter((f) => !seenKey.has(f.cls + f.event) && seenKey.add(f.cls + f.event))
    .sort((a, b) => order[a.severity] - order[b.severity] || a.event.localeCompare(b.event));
}
