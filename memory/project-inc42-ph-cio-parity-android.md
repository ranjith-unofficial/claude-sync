---
name: project-inc42-ph-cio-parity-android
description: "App PostHog→Customer.io event parity defect is Android-specific — brief_completed loses 32% on Android vs 3% iOS; verified live 12 Sep 2026"
metadata:
  type: project
---

Animesh reported (12 Sep 2026) that some App users have `brief_completed` / `sign_in_completed` in PostHog but
not on their Customer.io profile. Verified live the same day against PH `146258` + CIO `224949`.

**The defect is Android-specific, and it is a count problem, not a presence problem.**

| Event | iOS loss | Android loss |
|---|---|---|
| `brief_completed` | 2.9% (3/105) | **32.1% (27/84)** |
| `sign_in_completed` | 0% (0/63) | 8.0% (4/50) |

~200 Android brief completions/month never reach CIO. The prior audit's binary "does the user have the event"
check scored a user with **24 PH events and 7 CIO events** as passing — which is why it reported 12% instead of 32%.

**Smoking gun — `kavicharlaraviteja@gmail.com` (Android, cio_id `b5dd0d00a609a709`):** CIO `brief_completed`
stopped 2026-09-04; attribute `last_brief_completed_at` still updating live (2026-09-12T02:03:27, matching the PH
event to the second); `card_viewed` delivered 52s later on the same profile. So identity, transport and the
property write all work — **only the track call is missing.** This *inverts* the 29 Aug sheet note
("no setPersonProperties call"): setPersonProperties works, the track does not.

**Ruled out by test, do not re-litigate:** CIO log retention (3 users match exactly across 25-30 days);
CIO SDK flush-on-background (kavicharla 09-07 stayed foreground 24h, still lost); race with adjacent `$set`;
event-name spelling; wrong workspace; identify-ordering for these specific users.

**Also found:** 1,417 of 2,410 CIO App profiles (58.8%) are anonymous UUID shells with `email: null`, caused by the
app calling `$identify` on a generated UUID at install, ~3 min before any user identity exists. CIO receives **56**
event names against **23** authorised — 36 unauthorised. The 3 authorised-but-absent (`interest_captured`,
`push_delivered`, `profile_name_updated`) are exactly the 3 CIO rows left blank in the 29 Aug audit. Events carry
**no `$app_version`**, so defects cannot be correlated to releases.

Ticket pack + acceptance tests: `~/ClaudeDocs/inc42/FIXING-EVENTS-PRD-ph-cio-parity.md` (F1-F12).
Separate epic, do not merge: Singular→PostHog install/open attribution.

See [[project-inc42-app-event-validation]], [[project-inc42-event-audit-4sep]],
[[reference-inc42-vendor-api-browser-access]], [[feedback-analytics-depth]].
