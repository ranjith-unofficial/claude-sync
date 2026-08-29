---
name: project-inc42-app-analytics-audit
description: "29 Aug 2026 live PostHog+Customer.io audit of the Inc42 app event sheet — push_delivered/push_opened/decode status, 9 admitted-broken properties re-verified, new dead/duplicate events found"
metadata: 
  node_type: memory
  type: project
  originSessionId: 49bc3f2f-101a-442b-9f68-02964d9ae4cd
  modified: 2026-08-29T10:34:15.198Z
---

29 Aug 2026: ran the App Analytics Audit end-to-end — live HogQL queries against PostHog project 146258 ("Inc42 App") plus a Customer.io Data Index pull, cross-checked against the "App - Events" tab in the "One Inc42 - Analytics | Master Sheet" Google Sheet. Output lives in two tabs on that same sheet: **"App Audit - 2026-08-29"** (55 rows, full re-verification) and **"App - New Events Found"** (12 rows).

**Why:** Ranjith wanted to know whether the sheet's documented event/property bugs still hold, and whether PostHog/Customer.io are receiving what the sheet claims — not a re-read of the sheet, a live re-check.

**How to apply:** Treat this as a dated snapshot (2026-08-29), not a standing truth — event volumes and bug status will drift. Before citing any status below as current, re-run the underlying PostHog query if the conversation is more than a few days old.

## Headline findings
- **push_delivered**: confirmed dead — zero PostHog volume ever (event doesn't exist in the taxonomy at all), absent from Customer.io too.
- **push_opened**: only 2 lifetime PostHog events, both 10 Jul 2026, zero since — essentially non-firing despite 67% push opt-in.
- **decode** (AI explainer): zero PostHog telemetry, event absent from taxonomy entirely.
- Of the sheet's 9 admitted-broken properties: **4 confirmed fixed** (`brief_page_opened` source, `story_shared` channel, `search_result_tapped` entity-id, `summary_expanded`→now `story_id`), **1 partially fixed** (`watchlist_entity_added`: entity_name-for-sector fixed ~8 Aug, but `watchlist_size_after` and setPersonProperties still broken), the rest still broken (`deep_link_opened`, `card_rated`/`brief_story_rated` channel, `streak_milestone_viewed`, the push_permission/notification_settings_changed/preferences_updated setPersonProperties family), and **1 contradicts the sheet** (`sign_in_prompt_shown` is now firing with real volume since 1 Aug 2026 — sheet still says "not working").
- `card_rated` is confirmed **renamed to `brief_story_rated`** in production (verified live in PostHog, not just inferred from Customer.io).
- `interest_captured` and `profile_name_updated` are absent from **both** PostHog and Customer.io — worse than the sheet's CIO-only gap assumption.
- **New: the "Application ___" SDK duplicate-tracking finding.** `Application Backgrounded` / `Application Became Active` / `Application Opened` all carry `$lib=posthog-react-native, $lib_version=4.53.3` — the *same* SDK instance that fires the app's manual `app_opened` event. This is PostHog React Native SDK's own built-in `captureApplicationLifecycleEvents` autocapture running in parallel with the manual call, not a third-party or forgotten SDK. `app_opened` (3,710/90d) and `Application Opened` (3,763/90d) are within 1.4% of each other — strong signal they fire on the same trigger. `Application Foregrounded` exists only in Customer.io with zero PostHog counterpart (unconfirmed whether it maps to `Application Became Active`). Needs a product+engineering call on whether to disable the SDK autocapture now that the app has its own instrumentation.

## Operational gotchas hit during this audit
- The PostHog MCP connection's active project **silently reverts to "Inc42 | Live" (53557)** after every token re-auth/expiry — this happened repeatedly mid-session. Always re-confirm active project = 146258 before trusting any query result; see [[reference-inc42-posthog-projects]].
- A background/forked agent hit a permanent "MCP tool access unavailable" blocker and could only complete the Customer.io side + sheet scaffolding — all PostHog verification had to be redone directly in the main session, including a full re-audit to confirm no stale/placeholder rows survived the handoff.

Related: [[project-inc42-tracking-master-review]] (27 Aug review this audit follows up on), [[project-inc42-event-auditor]] (earlier 5/63-implemented finding), [[project-inc42-app-behaviour]] (post-launch funnel data), [[reference-inc42-posthog-projects]].
