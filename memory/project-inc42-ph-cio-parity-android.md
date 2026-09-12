---
name: project-inc42-ph-cio-parity-android
description: "Full-census App PostHog→Customer.io audit (12 Sep 2026) — 10.8% of authorised events never delivered; Android skew 2-4x; 60% of CIO profiles are anon shells"
metadata:
  type: project
---

Animesh reported (12 Sep 2026) that some App users have `brief_completed` / `sign_in_completed` in
PostHog but not on their Customer.io profile. Audited as a **full census** the same day — every event
name in both systems, all 2,412 CIO profiles, all 962 emailed PostHog users. PH `146258` / CIO `224949`.

**Headline:** of 11,621 authorised events in PostHog for emailed users in 30d, **1,256 (10.8%) never
reach Customer.io**. 276 of 931 matched users (29.6%) lose at least one event.

**⚠ Corrects an earlier 24-user pass** that claimed Android loses 32% of `brief_completed` vs 3% iOS
(11x). That was one outlier user. **Full population: Android 17.7% vs iOS 8.3% — 2.1x.**
`sign_in_completed` is 9.6% Android vs 2.1% iOS (4.5x). The Android skew is real but 2-4x, not 11x.

**Strongest platform signal:** 31 PostHog-active users have **no CIO profile at all** — **30 of 31 are
Android**. All 13 `register` complete misses and 12 of 13 `sign_in_completed` complete misses are Android.

**Worst per-event loss:** `app_updated` 95.8% (23 of 24 never arrive, both platforms); `story_unsaved`
47.8%; `notification_settings_changed` 44.3%; `brief_completed` 12.6%; `brief_opened` 11.3% (largest
absolute, -353). For `brief_completed` only 2.0% are complete misses — the rest is *partial* loss, so
it is intermittent drops, not a per-user cutoff.

**Never existed in CIO at all:** `interest_captured`, `push_delivered`, `profile_name_updated`.
**Reverse gap:** `article_published` — 409 events in CIO, 0 in PostHog, 354 on `editorial@inc42.com`;
sheet wrongly records `source` as `ios | android`.

**Over-fan-out:** taxonomy authorises 23 events; CIO catalog has 56 and took **46,130 unauthorised
events in 30d (floor)** vs 14,587 authorised — **76% of CIO volume is undocumented**. Includes four
lower-cased `application backgrounded/foregrounded/opened/installed` events that **do not exist in
PostHog** — a second undocumented delivery path (CDP/Segment-style auto-track).

**Profiles:** 2,412 total, 955 with email, **1,457 (60.4%) anonymous UUID shells** — caused by the app
firing `$identify` on a generated UUID at install before any identity exists.

Report + raw per-user matrices: `~/ClaudeDocs/inc42/PH-CIO-FULL-AUDIT.md` and `ph-cio-audit/`.
Earlier ticket pack: `~/ClaudeDocs/inc42/FIXING-EVENTS-PRD-ph-cio-parity.md`.
Separate epic, do not merge: Singular→PostHog install/open attribution.

See [[project-inc42-app-event-validation]], [[project-inc42-event-audit-4sep]], [[feedback-analytics-depth]],
[[reference-inc42-vendor-api-browser-access]].
