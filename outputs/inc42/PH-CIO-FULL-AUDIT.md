# Complete PostHog → Customer.io audit — Inc42 App

**Run:** 2026-09-12, ~18:00–18:45 IST · **Window:** last 30 days
**PostHog:** `Inc42 App` 146258 · **Customer.io:** `Inc42 App` 224949 · **Taxonomy:** App tab, `ashish-events-media-datalabs-app-v3.xlsx`
**Method:** full census, not a sample. Every event name in both systems; every profile in Customer.io (2,412 paged); every emailed user in PostHog (962). No sampling anywhere.
**Raw data:** `ph-cio-audit/` — `ph_users.txt`, `cio_users.txt` (per-user matrices), `ph_totals.tsv`, `cio_totals.tsv`, `events.txt` (index).

---

## 0. Correction to the earlier 24-user finding

An earlier pass on 24 users reported **Android losing 32% of `brief_completed` vs 3% on iOS (11×)**.
On the full population that is **wrong** — it was driven by one outlier user (`kavicharlaraviteja`, −17 events).

**Full-population truth:** `brief_completed` loses **17.7% on Android vs 8.3% on iOS — a 2.1× skew.**
The Android skew is real and consistent, but it is 2–4×, not 11×. Everything below is the full census.

---

## 1. Headline

| Measure | Value |
|---|---|
| Authorised events in PostHog for emailed users (30d) | **11,621** |
| Never delivered to Customer.io | **1,256 (10.8%)** |
| — because the user has **no CIO profile at all** | 374 |
| — lost despite a profile existing | 882 |
| Users with at least one lost event | **276 of 931 (29.6%)** |
| Users at perfect parity | 655 (70.4%) |

**By platform (users present in both systems):**

| OS | Users | Users with a gap | Authorised events (PH) | Event loss |
|---|---|---|---|---|
| Android | 528 | **176 (33.3%)** | 6,179 | **8.1%** |
| iOS | 387 | 97 (25.1%) | 4,892 | 6.5% |
| iPadOS | 16 | 3 (18.8%) | 176 | — |

---

## 2. Per-event loss — all 23 authorised events

PostHog 30d vs Customer.io 30d, all events including those on anonymous profiles.

| Event | PH | CIO | Lost | Loss % | Verdict |
|---|---|---|---|---|---|
| `story_unsaved` | 23 | 12 | −11 | **47.8%** | worst rate |
| `notification_settings_changed` | 61 | 34 | −27 | **44.3%** | |
| `account_deleted` | 6 | 4 | −2 | **33.3%** | low volume |
| `app_updated` | 43 | 31 | −12 | **27.9%** | |
| `signed_out` | 52 | 39 | −13 | **25.0%** | |
| `preferences_updated` | 117 | 100 | −17 | 14.5% | |
| `brief_completed` | 1,126 | 984 | −142 | **12.6%** | highest-value loss |
| `brief_opened` | 3,133 | 2,780 | −353 | 11.3% | largest absolute loss |
| `watchlist_entity_added` | 275 | 249 | −26 | 9.5% | |
| `story_saved` | 195 | 177 | −18 | 9.2% | |
| `app_installed` | 1,272 | 1,186 | −86 | 6.8% | mostly pre-identify |
| `onboarding_completed` | 1,109 | 1,038 | −71 | 6.4% | |
| `walkthrough` | 3,718 | 3,483 | −235 | 6.3% | |
| `watchlist_entity_removed` | 33 | 31 | −2 | 6.1% | |
| `sign_in_completed` | 2,438 | 2,303 | −135 | 5.5% | |
| `push_permission_granted` | 702 | 668 | −34 | 4.8% | |
| `register` | 480 | 460 | −20 | 4.2% | |
| `push_permission_denied` | 617 | 599 | −18 | 2.9% | |
| **`interest_captured`** | 0 | 0 | — | — | **NOT IN CIO CATALOG — never existed** |
| **`push_delivered`** | 0 | 0 | — | — | **NOT IN CIO CATALOG — never existed** |
| **`profile_name_updated`** | 0 | 0 | — | — | **NOT IN CIO CATALOG — never existed** |
| `push_opened` | 0 | 0 | — | — | dead in both |
| **`article_published`** | **0** | **409** | +409 | — | **reverse gap — see §5** |
| **TOTAL** | **15,400** | **14,587** | **−813** | **5.3%** | |

### Per-event × platform (users in both systems)

| Event | iOS loss | Android loss | Android skew |
|---|---|---|---|
| `sign_in_completed` | 2.1% | **9.6%** | **4.5×** |
| `brief_completed` | 8.3% | **17.7%** | **2.1×** |
| `push_permission_granted` | 12.5% | 25.0% | 2.0× |
| `walkthrough` | 2.5% | 3.2% | 1.3× |
| `onboarding_completed` | 1.8% | 2.5% | 1.4× |
| `brief_opened` | 12.4% | 14.9% | 1.2× |
| `watchlist_entity_added` | 2.4% | 3.0% | 1.2× |
| `register` | 0.0% | 5.2% | Android-only |
| `watchlist_entity_removed` | 0.0% | 3.8% | Android-only |
| `notification_settings_changed` | 0.0% | 5.3% | Android-only |
| `story_saved` | 17.7% | 4.5% | iOS worse |
| `signed_out` | 41.9% | 9.5% | iOS worse |
| `story_unsaved` | 76.9% | 10.0% | iOS worse (1 user) |
| `app_updated` | 95.7% | 100% | both broken |

`app_installed` cannot be measured this way — it fires before identify for 1,266 of 1,272 events, so the emailed subset is unrepresentative.

---

## 3. Users with NO Customer.io profile — unreachable by any campaign

**31 users, 374 authorised events, and 30 of the 31 are Android.** These people signed in, completed onboarding, read briefs — and no CIO profile was ever created.

| Email | OS | Events lost |
|---|---|---|
| adityabhupal17@gmail.com | Android | 44 |
| pabandeepswain@zohomail.in | Android | 37 |
| vaibhavagarwal1772002@gmail.com | Android | 36 |
| vishaldas0018@gmail.com | Android | 26 |
| subhanjan.biki@gmail.com | Android | 19 |
| yashwanthkashamaina121@gmail.com | Android | 17 |
| drakemoney008@gmail.com | Android | 15 |
| aman.chopra@medscred.com / kkarthik973@gmail.com | Android | 13 each |
| houseofdravon@gmail.com / siddeshmudaliar@gmail.com | Android | 12 each |
| manohvee@gmail.com / reachribu2@gmail.com / sundaram.t2809@gmail.com | Android | 10 each |
| sanketchandak2002, us4031712, vighnesh.s020506 | Android | 9 each |
| chocoboswift, sgo.dream, tanujj969 | Android | 8 each |
| adibajaj6313, naguljithnj, shishir.parasher@inc42.com | Android | 7 each |
| meet.shah2822, nandedrds | Android | 6 each |
| anwaydixit@rediffmail.com | Android | 4 |
| arjansinghbhambra1, vivekraman.2747 | Android | 3 each |
| kaushal9999, prashanth.prosys | Android | 2 each |
| **nyjain4@gmail.com** | **iOS** | 2 |

That 30:1 Android:iOS split is the single strongest platform signal in the audit.

---

## 4. Complete misses — profile exists, event never arrived

| Event | Users with total miss | Events lost | % of that event |
|---|---|---|---|
| `app_updated` | 22 | 23 of 24 | **95.8%** |
| `brief_completed` | 17 | 20 of 980 | 2.0% |
| `brief_opened` | 15 | 40 of 2,561 | 1.6% |
| `sign_in_completed` | 13 | 13 of 2,358 | 0.6% |
| `register` | 13 | 13 of 461 | 2.8% |
| `walkthrough` | 11 | 32 of 3,213 | 1.0% |
| `onboarding_completed` | 7 | 7 of 925 | 0.8% |
| `signed_out` | 4 | 5 of 52 | 9.6% |
| `app_installed` | 4 | 4 of 6 | 66.7% |
| `push_permission_granted` | 3 | 3 of 16 | 18.8% |
| `account_deleted` | 3 | 3 of 6 | 50.0% |
| `story_saved`, `story_unsaved`, `watchlist_entity_added`, `watchlist_entity_removed`, `push_permission_denied` | 1 each | 1–10 | — |

**Key reading:** for `brief_completed`, only 2.0% of events are complete misses — so the 17.7% Android loss is mostly **partial** loss (users who get some completions but not all), not users cut off entirely. That points at intermittent drops, not a per-user switch.

`register` complete misses are **13 of 13 on Android**. `sign_in_completed` complete misses are 12 of 13 on Android.

---

## 5. Reverse gap — `article_published`

- **409 events in Customer.io, 0 in PostHog.** 354 of them on a single profile: `editorial@inc42.com`.
- Taxonomy records its `source` as `ios | android` — impossible; nothing app-side produces it.
- This is a backend/editorial pipeline writing to Customer.io that product analytics cannot see at all.

---

## 6. Over-fan-out — 76% of Customer.io volume is unauthorised

The taxonomy authorises **23** events to Customer.io. Customer.io's catalog holds **56 names** and received **46,130 unauthorised events in 30 days** (a floor — 10 names hit the 3,000-page cap) against 14,587 authorised.

Top unauthorised by volume:

| Event | CIO 30d | PH 30d |
|---|---|---|
| `app_opened` | ≥3,000 | 5,731 |
| `application backgrounded` | ≥3,000 | **0** |
| `application foregrounded` | ≥3,000 | **0** |
| `application opened` | ≥3,000 | **0** |
| `brief_page_opened` | ≥3,000 | 10,404 |
| `card_viewed` | ≥3,000 | 16,235 |
| `profile_section_viewed` | ≥3,000 | 4,351 |
| `scroll_depth` | ≥3,000 | 3,972 |
| `explore_viewed` | ≥2,999 | 9,099 |
| `onboarding` | ≥2,999 | 5,170 |
| `article_opened` | 2,779 | 3,095 |
| `summary_expanded` | 2,052 | 2,289 |
| `search_performed` | 1,781 | 1,893 |
| `watchlist_viewed` | 1,778 | 2,055 |
| `sign_in_started` | 1,391 | 1,513 |
| `push_permission_prompted` | 1,267 | 1,317 |
| `deep_link_opened` | 1,095 | 1,199 |
| `application installed` | 76 | **0** |
| …plus 17 more | | |

**Four lower-cased `application *` events reach Customer.io but do not exist in PostHog at all.** PostHog has them title-cased (`Application Backgrounded`). That is a second, undocumented delivery path — almost certainly a CDP/Segment-style auto-track writing straight to Customer.io.

Five taxonomy names never arrive anywhere: `brief_open_today`, `company_untracked`, `industry_untracked`, `push_priming_dismissed`, `share_initiated`.

---

## 7. Profile-level state

| Measure | Value |
|---|---|
| Customer.io App profiles (all) | **2,412** |
| With a real email identifier | 955 (39.6%) |
| **Anonymous UUID, `email: null`** | **1,457 (60.4%)** |
| PostHog emailed users active in 30d | 962 |
| Matched in both | 931 |
| PostHog-active with no CIO profile | 31 |
| CIO email profiles with no PostHog 30d activity | 24 (includes test addresses: `gwshare.com`, `testinginc42`) |

**Three in five Customer.io profiles are anonymous shells** no campaign can reach. Cause confirmed earlier: the app fires `$identify` on a generated UUID at install, minutes before any user identity exists.

---

## 8. What to do — ordered

| # | Action | Why |
|---|---|---|
| 1 | **Fix Android profile creation.** 30 of 31 users with no CIO profile are Android. | Highest-certainty platform defect; 374 events and 31 people invisible |
| 2 | **Fix Android `register` + `sign_in_completed` delivery.** All 13 `register` complete misses and 12 of 13 `sign_in_completed` misses are Android. | Breaks every welcome/onboarding journey |
| 3 | **Fix `brief_completed` on Android** (17.7% vs 8.3% iOS). Mostly partial loss → look for intermittent drops, not a kill switch. | Highest-value engagement signal |
| 4 | **`app_updated` is 95.8% broken** — 23 of 24 events never arrive, both platforms. | Effectively unusable today |
| 5 | **Delete or implement** `interest_captured`, `push_delivered`, `profile_name_updated` — never existed in CIO. `push_delivered` blocks all push-delivery reporting. | Taxonomy claims capability that has never worked |
| 6 | **Find `article_published`'s producer.** 409 CIO events, 0 in PostHog, 354 on `editorial@inc42.com`, wrong `source` in the sheet. | Unknown pipeline writing to a production destination |
| 7 | **Stop the install-time `identify`.** 1,457 orphan profiles (60.4%). Decide merge-or-delete for the existing ones. | Inflates CIO profile count and billing; splits journeys |
| 8 | **Close the 36-name over-fan-out**, including the 4 lower-cased `application *` events absent from PostHog. Authorise or stop each. | 76% of CIO volume is undocumented |
| 9 | **Nightly per-user count assert**, PH vs CIO, split by OS, alert on any delta. | Every method used before today measured presence, not counts — that is why this was invisible |

---

## 9. Method notes and limits

- Customer.io per-event volume was obtained by paging `/v1/environments/224949/logs?type=event&name=<event>` with the `continuation` cursor and tallying `customer_id`, filtered to a 30-day cutoff. Authorised events were paged to completion (400-page cap, never hit); unauthorised events were capped at 60 pages (3,000 events) — those are floors, marked `≥`.
- Customer.io log retention covers the full 30-day window (confirmed: multiple profiles match PostHog exactly across 25–30 day spans).
- Profiles were resolved by paging all 2,412 customers and indexing `identifiers.email`. Customer.io's `?search=` parameter is **silently ignored** and returns the unfiltered list — any lookup built on it is invalid.
- PostHog counts come from HogQL over `events` with `person.properties.email`, 30-day window.
- Emails matched case-insensitively (PostHog holds at least one mixed-case address).
- Events that fire before identify (`app_installed`, `push_permission_*`, `sign_in_started`) cannot be attributed to an email profile; their per-user numbers are unrepresentative and flagged where used.
- Both sides were pulled within ~45 minutes; users active in that gap can shift a count by ±1.
