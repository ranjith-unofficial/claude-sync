---
name: project-inc42-datalabs-event-validation
description: "DataLabs six-point event validation (30 Aug 2026) — found a silent 18 May lock-tracking regression that broke a live A/B test, and a structurally invalid UserGuiding completion event"
metadata: 
  node_type: memory
  type: project
  originSessionId: 89944606-7a76-4026-a114-806b40d5dc68
  modified: 2026-08-30T07:51:29.466Z
---

Six-point validation (marketing/analytics skill criteria) of the four DataLabs events flagged by the 29–30 Aug raw census. Run live against PostHog project 66351 on 2026-08-30. Scoped to new findings only, not the ~150 already-confirmed sheet events.

**P0 — `Register Lock Interaction` silently regressed on 18 May 2026.** Three of its four value variants stopped dead within ~2 minutes of each other (a deploy). Monthly `onLoad` volume: May 212,554 → June 0 → July 0 → Aug 0. `Long Lock` as a lock type went to zero entirely. Only `Short Lock`/`Click` survives (~4,000/mo, and actually growing, so the product is fine — only tracking broke). Lifetime 421,773 events; 96% of that volume is the now-dead onLoad impression tracking.
- Consequence: 8 live insights reference this event, and 6 filter on `Lock Interaction = onLoad`, so they have been returning zero for 3.5 months. The **Freewall Lock A/B test is unreadable** (insights 3531380, 3495747, 3343388, 3342458, 3333793, 3332289). Lock impression → register conversion can no longer be computed at all.
- Second defect on the same event: `User State` mislabels identified users as "Guest" — 127 of 129 events whose `distinct_id` is an email still say Guest. The A/B funnels filter on `User State = Guest` / `is_not Logged-in`, so the test population is contaminated on top of being empty. Insight 3343388 also uses `semver_eq` as the operator on a plain string value.

**`guide completed (userguiding)` is structurally invalid as a completion metric.** Across 6,143 (user, guide) pairs over 400 days: median start→complete gap **26 milliseconds**, 80.2% complete within 1 second, and **36.4% "complete" BEFORE they start** (negative gap). It fires on guide render, not completion. The 8,587 lifetime "completions" and any completion rate derived from them are meaningless. It feeds insight 1004711 "DL Key Events" as a DAU series.
- Whole UserGuiding cluster is dead: 31,247 lifetime events, **zero in the last 30 days**, last activity 2026-06-11 (guides), 2025-07-08 (surveys), 2025-02-01 (checklist, 2 events ever).
- Naming correction: the real event names carry a `(userguiding)` suffix, e.g. `guide started (userguiding)`. Checklist/sheet names without the suffix do not exist.

**`Customise` → `Customize Columns Applied` migration is clean at event level, incomplete at property level.** Old British spelling: 2,843 lifetime, last fired 2025-03-22, zero since. New spelling: first 2025-07-16, 523/90d. No overlap, so no duplicate-event problem. But there is a **~4-month tracking blackout (Mar–Jul 2025)** with no column-customisation tracking at all, and the payload property is *still* named `Customise Column Properties` (British). 0 of 500 live insights reference either spelling — nothing consumes it.

**`master_agent_query` quality properties are genuinely populating — not placeholder.** `evidence_density` present on 2,032/2,345 (86.7%), avg 84.1, full 0–100 range, only 54 true zeros. `ungrounded_claims` present on 2,229/2,345 (95.1%), 67 events >0, max 3. An earlier-looking "367 zeros" was a ClickHouse artifact — `JSONExtractFloat` returns 0 for missing keys, so absent (313) and true-zero (54) must be separated with `JSONHas`. Gaps: 313 events missing evidence_density, concentrated in `out_of_scope` (legitimate) plus 37 events firing with an empty `query_type` (real bug). `is_fallback` = true on zero events in 90d. 18 live insights consume this event but **none use evidence_density or ungrounded_claims** — the quality signals are captured and unread.

**PII pattern across DataLabs: raw email is the PostHog `distinct_id`/`$user_id`.** Not a stray property leak — it is the identity key itself. Register Lock Interaction 128/4,049 (3.2%), Customize Columns Applied 296/523 (56.6%), UserGuiding 100% of sampled events. `master_agent_query` is clean: zero emails/phones in the raw `query` text, no email/user_email/response_text properties. Relevant to [[project-dpdp-compliance]] and distinct from the GA4/Mixpanel leak in [[project-inc42-mixpanel-gtm-tag-forensics]].

**Tooling note:** the PostHog MCP silently reverts project context roughly every other `execute-sql` call — `switch-project` reports success while the SQL session runs elsewhere, returning zero rows plus bogus "event not found in taxonomy" warnings for events that definitely exist. Workaround: call `switch-project` immediately before *every* query, and include `count() AS rows_matched` as a canary so an empty result is distinguishable from a real zero. Same class of bug as noted in [[project-inc42-datalabs-onboarding-cio-crosscheck]], but worse here.

See also [[reference-inc42-posthog-projects]], [[project-inc42-event-auditor]], [[project-inc42-tracking-master-review]].
