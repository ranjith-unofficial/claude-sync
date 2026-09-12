# Fixing Events — PRD / ticket pack: App PostHog → Customer.io destination parity

**Owner:** Ranjith (PM) · **Drafted:** 2026-09-12 (IST)
**Systems:** PostHog `Inc42 App` 146258 · Customer.io `Inc42 App` 224949 · Taxonomy `App` tab, `ashish-events-media-datalabs-app-v3.xlsx` (66 events)
**Upstream evidence:** `PER-USER-JOURNEY-AUDIT-REPORT.md`, `cohort-parity-brief-signin.md`, `event-level-ph-cio-gaps.md` (all 2026-09-12 17:19 IST)
**NOT this:** Singular → PostHog install/open attribution (`singular-posthog-attribution-plan.md`). Separate epic, separate tickets.

---

## 1. Problem

Customer.io campaigns keyed on brief completion and sign-in silently skip a minority of users who
demonstrably performed those actions. The event exists in CIO in aggregate, so every existing check
says "working". Parity is per-user, and per-user it fails.

| Claim | Value | Source |
|---|---|---|
| `brief_completed` — PH event, no CIO event | **12% (3/25)** | cohort, 30d PH sample |
| `brief_completed` — profile exists, no CIO event | **8.3% (2/24)** | cohort |
| `brief_completed` — CIO attr set, event never fired | **4.2% (1/24)** — `nehalk482` | cohort |
| `sign_in_completed` — PH event, no CIO event | **6.7% (1/15)**, understated | cohort + Exhibit A |
| Exhibit A: `brief_completed`, `sign_in_completed`, `register` absent on CIO after identify | confirmed | `lalitarorac9@gmail.com`, id `209480` |

**Blast radius:** any CIO campaign, segment or automation whose entry condition is one of the 23
CIO-destination events. At 12% that is ~1 in 8 converters never entering the journey.

---

## 2. The decisive piece of evidence

Exhibit A's own timeline rules out most candidate causes. On 2026-09-12:

| Time (UTC) | Event | Identity | Landed on CIO? |
|---|---|---|---|
| 06:22:30 | `sign_in_completed` | **identify → 209480** | **NO** |
| 06:22:30+ | `register`, `onboarding_completed`, `brief_page_opened`, `walkthrough`×4 | 209480 | partial (`register` NO) |
| 06:22–06:23 | `brief_opened`, `card_viewed`×8 | 209480 | **YES** |
| 06:23:41 | `brief_completed` | 209480 | **NO** |

Therefore, in the 71 seconds between identify and `brief_completed`:

- Identity was already resolved to `209480` → **not an identify-ordering failure** for this user.
- CIO accepted 9+ writes on that identity, including `card_viewed`, which the taxonomy does not even
  route to CIO → **transport was open, and over-delivering**.
- Only the *named terminal events* dropped.

→ The defect is **per-event**, in the code path or fan-out config for specific event names — not
timing, not transport, not the wrong profile. Pre-identify anon orphaning is a real *second* failure
mode (workspace logs show many anon-UUID `brief_completed` matches) but it does not explain Exhibit A.

---

## 3. Why the 29 Aug audit did not catch this

Not "we looked and got it wrong" — four distinct coverage failures:

| # | Failure | Evidence |
|---|---|---|
| 1 | **Wrong unit of analysis.** Aug 29 asked "does event X reach CIO / on what % of profiles". It cannot express "user U fired X in PH, U's CIO profile lacks X". A 12% per-user gap is invisible to a coverage %. | `brief_completed` = "CIO Y, 16% of profiles" → read as low-but-present |
| 2 | **Under-escalation of the actual root cause.** 9 of 23 CIO events were marked *"no setPersonProperties call"* / *"setPersonProperties call not working"*. That **is** the broken identity/property path. It was filed as a property nit, not a parity defect. | `brief_completed`, `story_saved`, `story_unsaved`, `watchlist_entity_added`, `watchlist_entity_removed`, `push_permission_granted`, `push_permission_denied`, `notification_settings_changed`, `preferences_updated` |
| 3 | **Rows never audited at all.** 5 of 66 rows carry a blank `audit_status`; 3 are CIO-bound. Their "dead in both systems" status was never discovered on Aug 29 — it was never checked. | `interest_captured`, `profile_name_updated`, `article_published` (+ `watchlist_limit_hit`, `locked_feature_tapped`) |
| 4 | **False "Working".** `sign_in_completed` and `register` are both `Working` with `trigger_identify_call = Yes`. Exhibit A disproves both at user level. | taxonomy vs Exhibit A |

**Fix the method, not just the events** — see ticket F7.

---

## 4. Second, unmeasured defect: over-fan-out

The mirror image, currently unquantified and worth its own line because it hits CIO cost and segment logic:

- Taxonomy routes **23** events to CIO. The CIO App catalog lists **56** event names.
- `app_opened` is `posthog`-only on the sheet but live in CIO at `daily_count` 105.
- `card_viewed` is `posthog`-only on the sheet but present on Exhibit A's CIO profile.
- The Sep 12 audit set `CIO_daily = n/a` for all 43 non-CIO-expected events — i.e. **it did not check them**.
  Up to **33** event names may be fanning out unexpectedly; exactly one is quantified.
- `article_published`: PH 0 / CIO `daily_count` 3, `source` recorded as `ios | android`. It cannot be
  app-client-fired. The `source` value is wrong and the producer is unidentified.

---

## 5. Root-cause hypotheses and the test that discriminates each

| # | Hypothesis | Discriminating test | Ruled out by Exhibit A? |
|---|---|---|---|
| H1 | Per-event fan-out config / code path omits the CIO `track` for specific names | Read the client: is `track`→CIO invoked in the same function for `brief_completed` as for `brief_opened`? | **No — leading candidate** |
| H2 | Two non-transactional paths: `setPersonProperties`/identify succeeds, `track` doesn't (or inverse) | `nehalk482` has `last_brief_completed_at` set, 0 `brief_completed` tracks | **No — confirmed live for ≥1 user** |
| H3 | Pre-identify events land on anon UUID profiles and never merge | CIO workspace logs for `brief_completed` return many anon-UUID `filter_matches` | Not for Exhibit A; **real as a second mode** |
| H4 | CIO API rejection (4xx/429/5xx) with no retry, silently swallowed | Instrument and log CIO HTTP response per track call | Weakened — 9+ writes succeeded in the same 71s |
| H5 | Event-name mismatch (`signin_completed` vs `sign_in_completed`) | Both spellings checked on Exhibit A — **neither** on CIO | **Yes — eliminated** |

---

## 6. Acceptance tests (the contract engineering must pass)

Let **U** = any user, **T** = 5 minutes.

- **AT-1 — post-identify parity.** If U fires `brief_completed` in PH at time t with a resolved
  `distinct_id`, then U's CIO profile for that same id shows a `brief_completed` **event** by t+T.
- **AT-2 — auth parity.** Same for `sign_in_completed` and `register`.
- **AT-3 — no attr-only completion.** A CIO profile must never hold `last_brief_completed_at` /
  `briefs_completed_total` without a corresponding `brief_completed` event. Attribute write and track
  write are one transaction or both are retried.
- **AT-4 — pre-identify merge.** If U fires `brief_completed` while anonymous and identifies later in
  the same session, the event must appear on the identified CIO profile after merge. No anon-UUID
  profile may retain a terminal event as its only home.
- **AT-5 — profile existence.** A user with a PH email and any CIO-destination event must have a CIO
  profile. (1/25 and 1/15 currently fail this.)
- **AT-6 — fan-out matches taxonomy.** Every event CIO receives is on the 23-event list, or the
  taxonomy is updated to admit it. No silent third state.
- **AT-7 — no silent drops.** Every client→CIO track call logs its HTTP outcome; non-2xx is retried
  with backoff and surfaced in a dashboard.

**Release gate:** AT-1/2/3 pass on a 50-user live sample at **100%**, verified after the fix ships, not before.

### QA matrix

| Case | Path | Expected |
|---|---|---|
| Q1 | Sign in → complete brief (identify before event) | both events on CIO, ≤T |
| Q2 | Complete brief anonymous → sign in after | event on identified profile after merge |
| Q3 | Complete brief anonymous → never signs in | event on anon profile, no orphan on later merge |
| Q4 | Complete brief with CIO API forced to 500 | retried, lands, logged |
| Q5 | Airplane mode during brief completion → reconnect | queued, delivered |
| Q6 | Attribute-only write | **forbidden** — must fail CI |
| Q7 | Fresh install → register → brief in one session | full chain on one CIO id |

---

## 7. Ticket pack

| ID | P | Ticket | Owner | Done when |
|---|---|---|---|---|
| F1 | **P0** | Guarantee `brief_completed` CIO track post-identify. Start from H1: diff the `brief_opened` path (works) against `brief_completed` (fails). | Ritvik / App SDK | AT-1 at 100%, n=50 |
| F2 | **P0** | Guarantee `sign_in_completed` + `register` CIO track, not only person attrs | Ritvik / Auth | AT-2 at 100%, n=50 |
| F3 | **P0** | Make attribute-write and track-write atomic (or both retried) for all 9 events flagged `no setPersonProperties` | Ritvik | AT-3; Q6 fails CI |
| F4 | **P0** | Backfill: replay CIO events for users with PH event and no CIO event since the defect window opened | Animesh + Ritvik | Cohort re-run shows 0% gap on the backfilled set |
| F5 | **P1** | Identify-order guarantee: journey-critical events never final on an anon id without merge | Ritvik | AT-4, Q2/Q3 |
| F6 | **P1** | Log + retry every client→CIO track HTTP outcome; alert on non-2xx rate | Ritvik | AT-7, dashboard live |
| F7 | **P1** | Replace the coverage-% audit method with a per-user assert. Weekly, N=25, `brief_completed` + `sign_in_completed` + `register`, alert if gap > 0. | Data / PM | Runs unattended, one alert channel |
| F8 | **P1** | Decide implement-or-delete on the dead 4: `interest_captured`, `push_delivered`, `push_opened`, `profile_name_updated`. `push_delivered` blocks all push-delivery reporting. | Ranjith + Ritvik | Each row either has volume or is removed from taxonomy |
| F9 | **P2** | Quantify over-fan-out: check all 43 "not expected" events against CIO; identify `article_published`'s real producer; correct its `source` | Animesh | Every CIO catalog name mapped to a producer |
| F10 | **P2** | Update taxonomy destinations to observed reality; add `last_verified_at` per row; fill the 5 blank `audit_status` rows | Ashish / taxonomy | 0 blank rows, destinations match §4 findings |
| F11 | **P2** | Investigate the 5 low-volume CIO-expected events at `daily_count` 0 (`app_updated`, `story_unsaved`, `watchlist_entity_removed`, `notification_settings_changed`, `account_deleted`) — distinguish "low volume" from "dropped" | Animesh | Each classified with a 30d per-user check, not a daily count |

---

## 8. Scope and provenance — what is and is not verified

**Independently verified for this pack (2026-09-12):**
- Taxonomy: 66 App events, exactly 23 with a `customerio` destination — matches the audit.
- The 9 `setPersonProperties`-flagged events, the 5 blank `audit_status` rows, and all `trigger_identify_call`
  values — read directly from `ashish-events-media-datalabs-app-v3.xlsx`.
- §2 and §4 inferences are mine, derived from the audit's own timeline and tables.

**Inherited, not re-pulled:** every PH 30d count, every CIO `daily_count`, the two cohort tables and
Exhibit A. All were live pulls at 2026-09-12 17:19 IST by the prior pass. PostHog MCP is unauthenticated
in this session and there is no Customer.io MCP — re-verification needs an OAuth round or browser access.

**Deliberately not claimed:**
- No CIO 30-day volumes. The API gave `daily_count` (today) and per-profile logs (~30d, 50/page) only.
- Per-user journey depth exists for `brief_completed` and `sign_in_completed` only. The other ~21
  CIO-destination events have event-level presence checks, not per-user parity. Expanding that is the
  next audit, not a finding in this one.
- Root cause is hypothesis-ranked, not confirmed. No one has read the client code yet. F1 starts there.
