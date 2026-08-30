---
name: project-inc42-media-event-validation
description: "Media six-point event validation (30 Aug 2026) — corrects 3 of the 29-30 Aug full-redo's own findings (lifetime vs. live), finds a live 11-day-old modal-tracking regression, and confirms Inc42 Onboarding is both the top PII-leaking event and a dead-end funnel"
metadata:
  node_type: memory
  type: project
  originSessionId: 89944606-7a76-4026-a114-806b40d5dc68
  modified: 2026-08-30T08:01:46.406Z
---

Six-point validation (marketing/analytics skill criteria) of the Media events flagged by the 29–30 Aug full-redo census. Run live against PostHog project 53557 on 2026-08-30 (bypassed the MCP's project-switch bug entirely by querying PostHog's API with the project pinned in the URL).

**Corrects 3 of the full-redo's own findings — lifetime totals were mistaken for current activity:**
- **"Loaded a Page" (22.7M events) is not live tracking at all** — 100% carries `$import`, is a bulk-imported historical Mixpanel dataset from the 2024 platform migration, date range Aug 2024–Mar 2025 only. There is no code to retire; the action is a data-hygiene decision on whether to purge it (it inflates PostHog volume/billing and pollutes any all-time analysis). Ties to the open Mixpanel incident as the same migration-era artifact class.
- **"User Segment" (2.66M events) — the original "dead, MoEngage-only" finding was correct; the full-redo's "firing 3 days ago" was a misread of a single straggler event.** Peaked 871,577/mo in May 2025, died in exact lockstep with MoEngage's removal (Aug 2025), single-digit strays since. Historical PII note: while live, GTM tag 439 called `Moengage.add_email` + `mixpanel.track` with a raw `Email` property.
- **"Plus Lock" (1,044,508 events) — both the full-redo and the earlier "0× to PostHog" report were correct, for different windows.** Code is intact and still gated correctly (`main.min.js` v21.94, 5 refs), but the condition it depends on stopped being met in March 2026 — Freewall Lock replaced it. Not a measurement bug. Separate minor finding: GTM contains `_cio.track("Plus Lock")` but Customer.io never received it — a silent delivery gap on an already-dead event.

**New, live, 11-day-old regression — the most actionable finding.** The homepage app-promo modal's inline script was changed around 19 Aug 2026 to push renamed events (`Inc42 App Modal Viewed/Clicked/Closed`) via `dataLayer.push`, but the GTM container (re-fetched live, confirmed) was never updated to match — it still listens for the old bare names (`Modal Viewed`, `Modal Clicked`, `Modal Closed`). Result: **all app-promo modal tracking has been completely dark since 19 Aug.** `Modal Clicked`/`Modal Closed` daily volume: steady through 18 Aug → 2 and 4 events on 19 Aug → 0 from 20 Aug onward. Fix is a one-line GTM trigger update per tag, not a code rollback — cheapest, highest-value fix from this whole validation pass.

**`Inc42 Onboarding` — confirmed the highest-volume PII-leaking Media event still firing today, and separately a dead-end funnel.** 13,733 events/60 days, still live. Two independent property defects:
- `distinct_id` is a raw email in 11,456/13,733 events (83%); GTM tag 427 fires `mixpanel.identify` + `mixpanel.people.set` + `posthog.identify` + 3× `_cio.identify` with email/phone/first/last/full name — confirms and quantifies the existing [[project-inc42-mixpanel-gtm-tag-forensics]] finding rather than adding a new one.
- Only two funnel states ever fire: `"Onboarding Started "` (12,121, note the trailing space — breaks any exact-match filter) and `"Onboarding Step 1 Completed"` (1,611, 13%). **No completion state exists at all** — the funnel is unmeasurable past step 1.

**This last point is directly relevant to the open Utkarsh onboarding-unification discussion (29 Aug, unresolved — see chat, not yet filed as a decision pending his clarification).** Ranjith relayed that Utkarsh wants DataLabs' final/canonical onboarding event unified into Media too. Media's current onboarding event can't even measure completion today — worth surfacing as a concrete blocker/data point when that discussion resumes, not treating as a separate issue.

**Modal Clicked/Closed also carry a naming collision independent of the regression**: "Modal Close" (legacy) and "Modal Closed" (current) are largely mutually exclusive (1,095 sessions have both out of 65,748/10,329 respectively) but are redundant names for one concept — needs a product decision, not more data.

**Gaps that couldn't be closed:** GA4 key-event marking is unverifiable without GTM/GA4 UI access (neither Google identity available has it); the compiled GTM container's rule→tag-index mapping is unreliable for asserting exact trigger wiring (nested `{"function"` structures inflate indices) — trigger evidence in this validation came from site code and observed firing patterns instead, not container parsing.

**Priority action order (as given by the validating agent):** 1) fix the 11-day-dark modal tracking (GTM trigger update), 2) fix Inc42 Onboarding's trailing-space value + missing completion state, 3) decide on purging the 8.3M imported "Loaded a Page" rows, 4) formally retire Plus Lock + User Segment in the master sheet.

Related: [[project-inc42-mixpanel-gtm-tag-forensics]], [[project-inc42-mixpanel-legacy-finding]], [[project-inc42-app-event-validation]], [[project-inc42-datalabs-event-validation]], [[project-inc42-analytics-team-briefs]].
