# Fixing Events — PRD / ticket pack: App PostHog → Customer.io destination parity

**Owner:** Ranjith (PM) · **Drafted:** 2026-09-12 (IST) · **Status:** all figures below independently re-verified against live PostHog + live Customer.io
**Systems:** PostHog `Inc42 App` 146258 · Customer.io `Inc42 App` 224949 · Taxonomy `App` tab, `ashish-events-media-datalabs-app-v3.xlsx` (66 events)
**Method:** HogQL via authenticated browser (`POST /api/environments/146258/query/`) + Customer.io `eu.fly.customer.io` REST (`/customers`, `/logs`, `/event_names`). Read-only.
**NOT this:** Singular → PostHog install/open attribution. Separate epic.

---

## 1. Headline — the defect is Android-specific

The prior pass measured parity as a binary "does the user have the event on CIO". Measuring **event counts**
per user, per platform, changes the picture entirely:

| Event | iOS loss | Android loss | Ratio |
|---|---|---|---|
| `brief_completed` | **2.9%** (3 of 105) | **32.1%** (27 of 84) | **11×** |
| `sign_in_completed` | **0%** (0 of 63) | **8.0%** (4 of 50) | — |

Android drops roughly **one in three** brief completions on the way to Customer.io. iOS is essentially healthy.
Both of the prior pass's "profile exists but no event" users (`lalitarorac9`, `nehalk482`) are Android — consistent.

Extrapolated: PostHog recorded 631 Android `brief_completed` in 30d. At 32% loss that is **~200 brief completions
per month that never reach Customer.io** from Android alone.

**This makes the fix a scoped Android client bug, not a distributed-systems investigation.** Repro needs one Android device.

---

## 2. Proof: attribute writes succeed while the event is dead

Live CIO profile `kavicharlaraviteja@gmail.com` (cio_id `b5dd0d00a609a709`, id `206935`, Android):

| Signal | Value |
|---|---|
| PostHog `brief_completed`, 30d | **24** (daily, through 2026-09-12 02:03:28) |
| CIO `brief_completed` events | **7** — last one **2026-09-04 02:32:22**, then nothing for 8 days |
| CIO attribute `last_brief_completed_at` | **2026-09-12T02:03:27.354Z** — matches the PostHog event to the second |
| CIO attribute `briefs_completed_total` | **8** — frozen |
| Other CIO events on the same profile | `card_viewed` (28), `brief_page_opened`, `sign_in_completed`, `streak_opened` — all live through **2026-09-12 02:04** |

So at 02:03:27 on 12 Sep the app wrote the person attribute to Customer.io and **did not send the event**, then 52
seconds later successfully sent `card_viewed` on the same profile. Identity was correct, transport was open, the
property write landed. **The `brief_completed` track call itself is not being made.**

Three different numbers for one fact on one user: PostHog 24, CIO events 7, CIO counter 8.

> Note this **inverts** the 29 Aug taxonomy note for `brief_completed` ("no setPersonProperties call"). Live data
> shows setPersonProperties working and the **track** missing. The sheet records the opposite of the real defect.

---

## 3. Hypotheses tested and eliminated

Each was ruled out by evidence, not opinion — record this so no one re-litigates them:

| Hypothesis | Verdict | Killed by |
|---|---|---|
| CIO log retention shorter than 30d, so counts aren't comparable | **ELIMINATED** | `utkarsh` 14/14 spanning 26 days, `shatayubhatnagar98` 16/16 spanning 25 days, `animesh` 48/49 spanning 30 days — CIO logs clearly retain ~30d |
| CIO SDK fails to flush when app is backgrounded | **ELIMINATED** | kavicharla 2026-09-07: brief completed, app stayed foreground **24 hours** (`bgIn=87,437s`), event still never reached CIO. Meanwhile 09-02 with `bgIn=2.9s` delivered fine |
| Race between `$set`/identify and the adjacent `track` | **ELIMINATED** | Delivery succeeded and failed at identical `$set` adjacency on both sides of the cut-off date |
| Event-name mismatch (`signin_completed` vs `sign_in_completed`) | **ELIMINATED** | Both spellings absent for Exhibit A |
| Identify ordering / anon-id orphaning explains the terminal drops | **NOT for these users** | Exhibit A: `$identify` → `209480` at 06:22:30.153, `brief_completed` 71s later, CIO accepted 9 writes on that id in between. Real as a *separate* defect (§5) |
| Wrong workspace / wrong project | **ELIMINATED** | PH 146258 and CIO 224949 both confirmed, profiles match on shared id |

**Surviving hypothesis:** the Android client's brief-completion code path calls the CIO person-property update but
not the CIO `track`, or calls a track that fails silently. Start at the diff between `brief_opened` (Android, works)
and `brief_completed` (Android, fails).

Supporting detail: for Exhibit A, `brief_completed` and `streak_milestone_viewed` fired 45ms apart in PostHog and
**both** are absent from CIO; for kavicharla, both stopped at the **same instant** (2026-09-04 02:32:22). They are
emitted from the same block. Whatever breaks, breaks that block's CIO emission.

---

## 4. Exhibit A — verified independently

`lalitarorac9@gmail.com` · PH person `41d2a88e-7ca5-55a4-b505-c6a632d44ff1` · shared id `209480` · CIO `b5dd0d00d812d912` · Android

PostHog, 2026-09-12 (millisecond-accurate):

| Time (UTC) | Event | On CIO? |
|---|---|---|
| 06:22:30.153 | `$identify` → 209480 | — |
| 06:22:30.156 | `sign_in_completed` | **NO** |
| 06:22:30.157 | `register` | **NO** |
| 06:22:32.096 | `onboarding_completed` | YES |
| 06:22:49–06:23:06 | `walkthrough` ×4, `explore_viewed` ×2, `watchlist_viewed` | YES |
| 06:23:25.647 | `brief_opened` | YES |
| 06:23:26–06:23:40 | `card_viewed` ×8 | YES (all 8) |
| 06:23:41.430 | `brief_completed` | **NO** |
| 06:23:41.475 | `streak_milestone_viewed` | **NO** |

CIO profile holds exactly 19 events: `card_viewed` 8, `walkthrough` 4, `brief_page_opened` 2, `explore_viewed` 2,
`brief_opened` 1, `watchlist_viewed` 1, `onboarding_completed` 1. Attributes `is_registered=true`,
`registration_date=2026-09-12T06:22:29.916Z` present; `last_brief_completed_at` and `briefs_completed_total` absent.

Also confirmed: PostHog merged two pre-identify anon ids (`76f6e0dc-…`, `01a09445-…`) into this person, and the app
fired a **`$identify` on an anon UUID at 06:19:10 — three minutes before any user identity existed.** That is the
mechanism that manufactures the anon CIO profiles in §5.

---

## 5. Anonymous-profile pollution — quantified

Full census of the CIO App workspace (all 2,410 profiles paged):

| Profile type | Count | Share |
|---|---|---|
| Keyed by real email | 954 | 39.6% |
| **Anonymous UUID, `email: null`** | **1,417** | **58.8%** |
| Other | 39 | 1.6% |

**Three in five Customer.io profiles are anonymous shells** that can never be reached by an email campaign and never
merge to the identified profile. Driven by the install-time `$identify` on a generated UUID (§4). This inflates CIO
profile counts (and therefore billing) and silently splits journeys.

---

## 6. Over-fan-out — quantified

| Measure | Count |
|---|---|
| Events the taxonomy routes to Customer.io | **23** |
| Event names actually present in the CIO App catalog | **56** |
| **Unauthorised names arriving at CIO** | **36** |
| Authorised names absent from CIO entirely | **3** |

The 3 absent are `interest_captured`, `push_delivered`, `profile_name_updated` — **exactly** the three CIO-bound rows
whose `audit_status` was left blank on 29 Aug. They were never checked, and they have never worked.

Unauthorised arrivals include `card_viewed`, `brief_page_opened`, `explore_viewed`, `watchlist_viewed`, `scroll_depth`,
`search_performed`, `article_opened`, `profile_section_viewed`, `onboarding`, `error_shown`. Also present:
`application backgrounded` / `application foregrounded` / `application installed` / `application opened` — **lower-cased**
in CIO where PostHog has them title-cased, and two of those four are dead in PostHog.

Caveat: the CIO catalog is lifetime, so presence proves it fanned out at some point, not that it fires today.

---

## 7. Why the 29 Aug audit did not catch this

| # | Failure | Evidence |
|---|---|---|
| 1 | **Wrong unit of analysis.** It asked "does event X reach CIO / on what % of profiles" — a question that cannot express per-user or per-platform loss. | `brief_completed` recorded as "CIO Y, 16% of profiles" |
| 2 | **Binary, not quantitative.** Even the 12 Sep pass scored a user with 24 PostHog events and 7 CIO events as parity "Y". Event-count loss (32% Android) is 2.7× the user-level gap (12%). | kavicharla, ashishu001, pranav |
| 3 | **Never segmented by platform.** The single most important variable was never crossed. | §1 |
| 4 | **Rows never audited.** 5 of 66 rows have a blank `audit_status`; 3 are CIO-bound and all 3 are confirmed dead. | `interest_captured`, `profile_name_updated`, `article_published` |
| 5 | **A note recording the defect backwards.** `brief_completed` was filed as "no setPersonProperties call"; live data shows setPersonProperties works and the track is missing. | §2 |
| 6 | **False "Working".** `sign_in_completed` and `register` marked Working. | §4 |

---

## 8. Statistical honesty

The live population of users who fired `brief_completed` in the last 30d with an email on the PostHog person is
**298 users / 1,008 events** (total event volume 1,128, so ~120 events belong to persons with no email at all and can
never match a CIO profile by email). The verified cohort is **24 profiles** — 8% of that population. The Android/iOS
split is large and consistent enough to act on, but the exact percentages carry a wide interval. **Ticket F7 replaces
sampling with a standing census.**

---

## 9. Acceptance tests

Let **U** = any user, **T** = 5 minutes.

- **AT-1 — post-identify parity.** U fires `brief_completed` in PH at t with a resolved id → U's CIO profile shows a `brief_completed` **event** by t+T. **Must pass on Android and iOS separately.**
- **AT-2 — auth parity.** Same for `sign_in_completed` and `register`.
- **AT-3 — count parity, not presence.** For any U over any 7-day window, `count(PH event) == count(CIO event)` per event name. Presence is not the test.
- **AT-4 — no attr-only completion.** A profile must never hold `last_brief_completed_at` / `briefs_completed_total` without the matching event. Property write and track are one transaction, or both retried. `briefs_completed_total` must equal the CIO event count.
- **AT-5 — pre-identify merge.** An event fired anonymously then identified in-session must land on the identified profile. No anon profile may be a terminal event's only home.
- **AT-6 — no install-time identify.** The client must not call `identify` before a real user identity exists. New anon UUID profiles per install → 0.
- **AT-7 — fan-out matches taxonomy.** Every name CIO receives is on the authorised list, or the list is updated. No silent third state. Casing identical across destinations.
- **AT-8 — no silent drops.** Every client→CIO call logs its HTTP outcome; non-2xx retried with backoff and surfaced.

**Release gate:** AT-1, AT-2, AT-3 pass at 100% on a 50-user live sample **split evenly Android/iOS**, verified after the fix ships.

### QA matrix

| Case | Path | Expected |
|---|---|---|
| Q1 | Android: sign in → complete brief | both events on CIO ≤T |
| Q2 | iOS: same | both events on CIO ≤T |
| Q3 | Complete brief 3× across 3 days on Android | CIO event count == 3, counter == 3 |
| Q4 | Complete brief anonymously → sign in after | event on identified profile post-merge |
| Q5 | Fresh install, no sign-in | **no** CIO profile created |
| Q6 | CIO API forced to 500 | retried, lands, logged |
| Q7 | Airplane mode during completion → reconnect | queued, delivered |
| Q8 | Attribute-only write | **forbidden** — fails CI |

---

## 10. Ticket pack

| ID | P | Ticket | Owner | Done when |
|---|---|---|---|---|
| F1 | **P0** | **Android `brief_completed` → CIO track call.** Diff the Android `brief_opened` path (works) against `brief_completed` (32% loss). The property write already works — the track is missing or silently failing. | Ritvik / Android | AT-1 + AT-3 at 100%, n=25 Android |
| F2 | **P0** | Android `sign_in_completed` + `register` track (8% loss; `register` confirmed lost for Exhibit A) | Ritvik / Android | AT-2, n=25 Android |
| F3 | **P0** | Make property-write and track atomic for the brief-completion block; `briefs_completed_total` must reconcile to event count | Ritvik | AT-4; Q8 fails CI |
| F4 | **P0** | Backfill CIO events for Android users with PH events missing on CIO since the defect window (kavicharla: 17 events) | Animesh + Ritvik | Re-census shows 0 gap on backfilled set |
| F5 | **P1** | **Stop the install-time `identify` on a generated UUID.** Root cause of 1,417 orphan profiles. Decide the fate of the existing 1,417 (merge or delete) with Animesh. | Ritvik + Animesh | AT-6; orphan share falls |
| F6 | **P1** | Add `$app_version` / `$app_build` to every event. **Currently absent — we could not correlate this defect to a release.** | Ritvik | Both properties on 100% of events |
| F7 | **P1** | Replace sampling with a standing census: nightly, all 298+ users, per-event **count** comparison PH vs CIO, **split by OS**, alert on any delta | Data / PM | Runs unattended, one alert channel |
| F8 | **P1** | Log + retry every client→CIO call outcome; alert on non-2xx rate | Ritvik | AT-8, dashboard live |
| F9 | **P1** | Implement or delete the 3 confirmed-dead: `interest_captured`, `push_delivered`, `profile_name_updated`. `push_delivered` blocks all push-delivery reporting. | Ranjith + Ritvik | Each has volume or is removed |
| F10 | **P2** | Close the 36-name over-fan-out: authorise or stop each. Fix the title-case/lower-case divergence. Identify `article_published`'s real producer (PH 0 / CIO live; `source` wrongly recorded as `ios \| android`). | Animesh | Every CIO name mapped to a producer |
| F11 | **P2** | Fill the 5 blank `audit_status` rows; add `last_verified_at` per row; correct the inverted `brief_completed` note | Ashish / taxonomy | 0 blank rows |
| F12 | **P2** | `pabandeepswain@zohomail.in` has 12 PH `brief_completed` and **no CIO profile at all** — find why identified users fail to create profiles | Animesh | Root cause documented |

---

## 11. Provenance

**Verified live in this pass (2026-09-12, ~17:30–18:00 IST):** the 30d event census (55 names); Exhibit A's full
PostHog timeline and complete CIO profile; per-user PH and CIO counts for all 24 resolvable cohort profiles
(**my CIO counts matched the prior pass exactly on all 24** — that data is sound); the Android/iOS split; the
2,410-profile CIO census; the 56-name CIO catalog; the absence of `$app_version`; taxonomy destinations, identify
flags and audit-status blanks from the workbook.

**Corrected during verification:** Customer.io's `?search=` parameter is silently ignored and returns the unfiltered
customer list — an email lookup built on it resolves every address to the same profile. Profiles must be resolved by
paging `/customers` and indexing `identifiers.email`. Any earlier result built on `?search=` is invalid.

**Not claimed:** no CIO 30-day aggregate volumes (the API exposes `daily_count` for today and per-profile logs only).
Per-user depth covers `brief_completed`, `sign_in_completed` and `register`; the other ~20 CIO-bound events have
catalog presence only. `register` gaps for users who signed up before the log window are indeterminate. Root cause
in §3 is the surviving hypothesis — no one has read the Android client yet. F1 starts there.
