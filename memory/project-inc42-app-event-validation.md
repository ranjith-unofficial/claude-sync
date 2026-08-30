---
name: project-inc42-app-event-validation
description: "App six-point event validation (30 Aug 2026) — watchlist free-tier cap not enforced in prod, card_viewed missing edition_date on all events, Application_ SDK-duplicate confirmed zero-risk to disable, 4th PII pattern found"
metadata:
  node_type: memory
  type: project
  originSessionId: 89944606-7a76-4026-a114-806b40d5dc68
  modified: 2026-08-30T07:57:46.131Z
---

Six-point validation (marketing/analytics skill criteria) of the App events flagged by the 29–30 Aug raw census. Run live against PostHog project 146258 (full history = 90d window, app is that new) and Customer.io workspace 224949 on 2026-08-30.

**Biggest finding: the watchlist free-tier cap is not enforced in production at all.** `watchlist_limit_hit` never fires because its trigger condition never occurs — users have reached 166 watchlist items / 161 tracked companies against the sheet's documented ~15 company / 5 sector (~20 total) cap, a 10x overage on 13+ users. This is a missing product gate, not a missing analytics event — the "upsell signal" this event exists to capture has had nothing to capture.

**`rating_prompt_shown` is a decisive instrumentation bug**, not an unmet trigger: the condition fires repeatedly (5× day-7 streak milestones; 83 users with 3+ brief completions, 28 with 7+, max streak 11) but the event never fires either platform.

**`article_published` is a routing gap, not a missing feature**: fires server-side into Customer.io (<1% of profiles, unused) but never reaches PostHog — the sheet's PostHog column is simply wrong for this row.

**`force_update_shown` never fires because the gate has no floor set** — 4 app versions live including a pre-release 0.1.0 still emitting 23,182 events on both platforms with nothing catching it. Consistent with force-update mechanics being PROPOSED v2 scope (see [[project-inc42-app-v2-release]] — don't force-update iOS until build ≥41).

**`locked_feature_tapped` and `brief_fallback_shown` are blocked, not resolved**: no lock/paywall event of any kind exists in the project (partial evidence, needs eng/codebase to confirm gated UI exists at all); `brief_fallback_shown` couldn't be tested because of a separate bug (next paragraph).

**Real bug outside the scoped list: `card_viewed` — the app's single highest-volume event (13,164 samples) — has `edition_date` returning 0 distinct values on every single event.** Per the sheet this property is what powers card drop-off curve, boost effectiveness, and the editorial feedback loop. None of that per-edition analysis is currently possible. This is what blocked the `brief_fallback_shown` test as a side effect, but is a significant finding on its own.

**Application Opened/Became Active/Backgrounded/Installed — CLOSED, confirmed zero-risk to disable.** Exact duplicate of the custom lifecycle events, not a partial overlap: 84.5% of `app_opened` firings have a same-minute, same-person `Application Opened`; totals within 1% (3,930 vs 3,968); raw 10-second buckets show 1:1 pairing. Nothing downstream consumes any of the four (Customer.io: 0 of 55 events "in use"; the one live automation touching lifecycle explicitly has no conversion criteria set). Caveat: the SDK events carry `$os` but `platform` is null on all of them (custom events populate android/ios) — so this is "delete the duplicate," not "swap to the SDK version," since they aren't property-equivalent. Also: `Application Installed` is itself dead within the dead family — 4 lifetime events, stopped 2026-07-10, vs `app_installed`'s 825.

**PII pattern, 4th instance this week.** `app_opened` carried a real email property on 17 events / 8 distinct users between 29 Jul and 8 Aug 2026, forwarding to Customer.io; no occurrences found after 8 Aug. Not confirmed fixed — could simply be sparse/intermittent — needs a follow-up check, not an assumption it resolved itself. Joins [[project-inc42-mixpanel-gtm-tag-forensics]] (Mixpanel GTM tags + GA4 page_view) and [[project-inc42-datalabs-event-validation]] (raw email as PostHog distinct_id) as the fourth distinct PII pattern found across the analytics stack this week — this is now a systemic pattern worth flagging to whoever owns [[project-dpdp-compliance]] as such, not four separate one-offs.

**Separate operational flag, unresolved:** Customer.io's Segments list shows 0 active and 0 archived, yet a live running automation ("Segment - 1 | App Install Done | No Onboarding | No Signup") has sent 333 messages since 6 Aug off a segment that doesn't appear in that list at all. Either a UI/permissions artifact, or a segment definition nobody can currently see or audit is driving live sends. Needs a direct check.

**Same recurring PostHog MCP tooling bug, 4th confirmed occurrence** (see [[project-inc42-datalabs-event-validation]] for the first report and the PostHog feedback already filed) — project context silently reverted off 146258 roughly every other call; every figure above is canary-verified.

Related: [[project-inc42-app-analytics-audit]] (the original 29 Aug audit this validates against), [[project-inc42-analytics-team-briefs]].
