---
name: project-inc42-event-auditor
description: "The automated analytics event auditor built for inc42.com — what it is, where it lives, and the verified findings"
metadata:
  node_type: memory
  type: project
---

Automated end-to-end analytics event auditor for inc42.com, built 23 Aug 2026.
Lives at `~/ClaudeDocs/inc42/event-auditor/`. Run: `node audit.mjs` (add `--only=browser` to skip PostHog).

**What it does:** Playwright drives real Chrome through 6 scripted journeys; Node intercepts and decodes every
outbound payload (PostHog gzip/base64 batches, GA4 Measurement Protocol, Meta Pixel, Customer.io); an injected
probe wraps the SDKs at the call site; HogQL then verifies the run's own `distinct_id`s actually landed.
Findings classified P0/P1/P2. Output → `runs/<ts>/report.html` + `findings.json`.

**The consolidated sheet** it generates: `~/ClaudeDocs/inc42/Inc42 Web Analytics — Event Register.xlsx`
(5 tabs — Read Me / Event Register / Property Dictionary / Findings / Scroll Depth). Built by
`python3 tools/build-sheet.py`. It replaces the 47-tab `Inc42 Analytics | Master.xlsx` and the separate
`Inc42 Website - Events & Properties.xlsx`.

**Verified findings (browser half, 23 Aug):**
- Only **5 of 63** planned events are properly implemented; 24 partial, 32 missing.
- **GA4 receives more distinct event types than PostHog** across the same journeys. `autocapture` and
  `capture_pageview` are both OFF, so nothing fills the gap automatically.
- **`Plus Lock` fires ~22×/run to GA4 and 0× to PostHog** — the Jun-2026 audit's "4/30d, likely superseded"
  was wrong; it fires constantly into the wrong tool.
- **Customer.io receives only `type: page` calls, zero `track()`** — confirms the 12-Aug finding.
- **scroll_depth: three parallel implementations** (GTM built-in trigger at 25/50/75/**90**/100, a
  `Custom Scroll Depth` tag, a `ScrollDepth-Value-Calculator` tag), two differently-named GA4 events
  (`scroll` at 90 only, `Scroll Depth` at 25/50), three property formats, and **zero to PostHog**.
- `summary_viewed` is in the Website spec (tab `Website | Events`, row 10) but has **zero hits in the Master
  sheet** — planned, never implemented.

**Gotchas:**
- inc42.com serves **HTTP 201 + `application/octet-stream` to any `HeadlessChrome` UA**. The runner overrides
  the UA. Any synthetic monitor pointed at the site needs the same or it silently gets a non-HTML body.
- `spec/aliases.json` is the hand-maintained join — the plan is snake_case, production is Title Case, and only
  2 of 63 names match automatically. Without it the tool reports all 63 as missing.
- **Probe lesson:** `window.dataLayer` is reassigned more than once, so a naive replay of the array on each
  setter trap double-counts every entry and fabricates "double-fire" findings. Replayed records are now
  flagged and excluded from the duplicate rule. Always check a finding's stack trace before reporting it.

Related: [[reference-inc42-vendor-stack]], [[reference-inc42-posthog-projects]], [[nexloid-product]]
(this is Nexloid's diagnose step, proven on a site we control).
