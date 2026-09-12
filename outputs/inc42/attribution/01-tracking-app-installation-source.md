# Layer A — Tracking app installation source

**Owner:** Ranjith M · **Status:** proposed, not approved · **Date:** 12 September 2026
**Scope:** INSTALL / first-touch attribution only. Session opens → `02-tracking-app-open-source.md`. In-app navigation → `app-attribution-source-mapping-spec.md` §6.
**Live state verified:** PostHog project 146258, 30 days to 12 Sep 2026 (132,435 events · 5,772 sessions · 1,341 people · 1,437 persons lifetime). Re-run before citing any number as current.

---

## 0. Naming decision — read before anything else

Two drafts exist with conflicting property names. **This file uses the `attribution_*` / `entry_*` / `referrer_*` convention** from `app-attribution-source-mapping-spec.md` (6 Sep), not the `attr_*` / `open_source` / `source_screen` convention from `singular-posthog-attribution-plan.md` (11 Sep).

| Layer | Adopted prefix | Rejected alternative |
|---|---|---|
| A · install | `attribution_*` (person, immutable) | `attr_*` |
| B · session entry | `entry_*` (super property) | `open_source` |
| C · in-app nav | `referrer_*` (event property) | `source_screen` |

Three reasons, in order of weight:

1. **The keys already exist in production.** `attribution_source` and `attribution_campaign` are present on **1,386 of 1,437 persons (96.4%)** — the `$set` call already fires on nearly every install. Adopting this prefix means *filling a null field*, not adding a field.
2. **`open_source` / `source_screen` both reuse the word `source`** — the exact overloaded field that caused this problem. `app_opened.source` and `article_opened.source` currently hold values from two different layers. Reusing the word guarantees the collision comes back.
3. The 6 Sep spec is measured against live data and carries the `register()` leakage analysis; the 11 Sep plan is a cleaner runtime flow. **Take the naming from 6 Sep, the runtime flow from 11 Sep.**

**Action:** whichever is locked, the losing draft must be marked superseded in the same pass, or a third convention will appear in the next ticket.

---

## 1. Problem

The app cannot answer "which campaign, link or share produced this install" for any user, because no install-attribution value has ever reached PostHog. `app_installed` fires 1,273 times per 30 days carrying only device and streak context — no referrer, no campaign, no network. The person-level slots for the answer exist and fire on 96.4% of persons, but their value is **literal `null` on all 1,386** — the `$set` path is wired and the resolver behind it returns nothing. Singular resolves installs server-side and is never read back. Consequently every acquisition-quality question ("do Product Hunt installs finish the Brief?") has no denominator, and paid spend cannot be judged against in-app behaviour at all.

### 1.1 Measured current state (30d to 12 Sep 2026)

| Signal | Live reality |
|---|---|
| `app_installed` volume | 1,273 events |
| `app_installed` attribution props | **none** — carries only `platform`, `device_model`, `manufacturer`, `os_version`, `app_version`, `install_date`, `days_since_install`, `streak_day`, `streak_tier`, `push_opt_in`, `watchlist_count`, `is_registered` |
| `attribution_source` / `attribution_campaign` (person) | key present on 1,386/1,437 persons; **value is JSON `null` on all 1,386**, empty string on 51. Never once populated |
| `utm_source` / `utm_medium` / `utm_campaign` (event) | **0 of 132,435 events** |
| `utm_*` (person) | 2 persons lifetime |
| `install_referrer_raw` or any Play referrer field | does not exist |
| Deferred deep-link destination | not captured anywhere |
| `share_id` on outbound shares | does not exist — `story_shared` (196 events) carries `story_id`, `channel`, `source` and article metadata, but nothing that can be read back on the inbound click |

**Correction to the 6 Sep spec:** it recorded `attribution_source` / `attribution_campaign` as "0% populated". Precisely: the **keys are written on 96.4% of persons with a null value**. The distinction matters for engineering — this is a resolver that returns nothing, not a missing `$set` call.

---

## 2. Event & property contract

### 2.1 `app_installed` — unchanged, do not block it

Fires once at first launch, immediately, with no waiting. It is a **counting** event and must never be delayed for attribution. No new properties.

### 2.2 Person properties — the system of record for install source

Written **once per install and never overwritten** (`$set_once` semantics, plus a persisted local `attribution_locked` flag so a reinstall-in-place cannot clobber).

| Property | Type | Values / notes | Req |
|---|---|---|---|
| `attribution_state` | enum | `resolved` · `organic` · `unresolved_timeout` · `unavailable_platform` | **yes** |
| `attribution_is_organic` | bool | from Singular | **yes** |
| `attribution_source` | string | channel level, Singular Partner convention: `Google Ads` · `Meta` · `Product Hunt` · `Email` · `Web Banner` · `Offline Events` · `App Share` · `organic` | **yes** |
| `attribution_medium` | string | `cpc` · `email` · `social` · `referral` · `qr` · `store` | no |
| `attribution_campaign` | string | Singular `pcn` | no |
| `attribution_creative` | string | Singular `pcrn` | no |
| `attribution_placement` | string | Singular `psn` | no |
| `attribution_network` | string | Singular network name | no |
| `attribution_singular_link` | string | the `sng.link` that resolved | no |
| `install_referrer_raw` | string | Android Play Install Referrer string verbatim; iOS AdServices/`ct` token | no |
| `install_store` | enum | `play` · `app_store` · `testflight` · `internal` · `unknown` | **yes** |
| `install_deferred_destination` | enum | `article` · `brief` · `company_profile` · `sector_landing` · `home` — null if none | no |
| `install_deferred_entity_id` | string | story_id / company_id the link targeted | no |
| `attribution_share_id` | string | present only when the install came from an in-app share link (Phase 2) | no |
| `attribution_install_at` | ISO8601 | first launch time | **yes** |
| `attribution_resolved_at` | ISO8601 | when Singular actually answered — gives latency, and proves whether the timeout is right | **yes** |
| `attribution_conflict` | bool | `true` when Play referrer and Singular disagree (see §3.3) | no |

**Deliberately excluded:** any `attribution_last_*` field. Last-touch is a *session* fact and lives in `entry_*` (file 02). Putting both on the person is how the two layers merged in the first place.

### 2.3 `install_attributed` — one-time event

| Property | Notes |
|---|---|
| all `attribution_*` fields above | mirrored onto the event so install cohorts can be built as a funnel step, not only as a person filter |
| `resolved_late` | bool — `true` if it arrived after the §3.2 timeout |
| `resolve_latency_ms` | int — `attribution_resolved_at` − `attribution_install_at` |

Fires **at most once per install**, ever. It is not an open, not a session, and must never be used as a volume metric for installs — `app_installed` is.

---

## 3. Runtime flow

### 3.1 Sequence

```
1.  Detect first launch (no attribution_install_at in local storage)
2.  Init PostHog SDK, init Singular SDK
3.  Fire app_installed IMMEDIATELY (device context only — never delayed)
4.  Android: read Play Install Referrer API -> install_referrer_raw
    iOS:     request AdServices token / read Apple `ct` -> install_referrer_raw
5.  Register Singular attribution callback + deferred deep-link callback
6.  Wait up to T_INSTALL = 3000 ms
7.  On resolve:
      - resolve conflicts per 3.3
      - $set_once the attribution_* block
      - set local attribution_locked = true
      - fire install_attributed
      - navigate to install_deferred_destination if present
8.  On timeout:
      - $set_once { attribution_state: 'unresolved_timeout' }  (fields left null)
      - keep the callback registered for the rest of the session
      - if it resolves later: overwrite ONLY attribution_state + the null fields,
        fire install_attributed with resolved_late = true
9.  Never write any attribution_* field once attribution_locked = true
```

### 3.2 Timeout — 3,000 ms, not 1,500 ms

Install attribution happens **once in the lifetime of the app** and gates every acquisition question. The open-event timeout (1,500 ms, file 02) is tuned for a user staring at a splash screen every session; this one is not. `app_installed` has already fired by step 3, so nothing user-facing is blocked — the wait only delays `install_attributed` and the deferred navigation, and the first-launch path already shows onboarding (5,171 `onboarding` events / 30d), which absorbs the latency.

Set `attribution_resolved_at` on every install so the timeout can be re-tuned from real latency after two weeks instead of argued about.

### 3.3 Priority when signals disagree

| # | Signal | Why it wins |
|---|---|---|
| 1 | Play Install Referrer with a `utm_source` | deterministic, from the store, not probabilistic |
| 2 | Singular resolved non-organic | MMP is the contracted system of truth |
| 3 | Singular deferred deep-link payload | gives destination even when campaign is thin |
| 4 | Singular organic | genuine organic store install |
| 5 | nothing | `attribution_state = unresolved_timeout` |

If 1 and 2 disagree on campaign: **take Play referrer for `attribution_*`, keep Singular's values on `attribution_singular_link` / `attribution_network`, and set `attribution_conflict = true`.** Do not silently pick one; a conflict rate above ~5% means the link config in §5 is wrong.

### 3.4 Config prerequisite — this design fails without it

Every Singular link must carry `utm_source` / `utm_medium` / `utm_campaign` in its **Google Play referrer / custom referrer parameters**. Without it, Play returns an empty referrer, only Singular can resolve the install server-side, and priority 1 never fires. This is a link-configuration job in Singular, not app code, and it is the single highest-leverage item in this file.

---

## 4. PostHog vs Singular

| | Singular (MMP) | PostHog (product) |
|---|---|---|
| Decides which campaign gets credit | **yes — sole authority** | never |
| Fraud / SKAdNetwork / iOS privacy handling | yes | no |
| Paid spend and ROAS reporting | yes | no |
| Stores install source per person | yes (its own) | **yes — copy, for behavioural joins** |
| Answers "did this cohort finish the Brief" | no | **yes** |
| Source of `attribution_*` values | produces them | consumes them, read-only |

**Rule:** PostHog never computes attribution, only records what Singular (or the Play referrer) hands it. If the two dashboards disagree on install counts, **Singular is right about installs** and the gap is a PostHog delivery problem to investigate — not a number to reconcile by adjusting PostHog.

---

## 5. QA matrix

| # | Scenario | Expected |
|---|---|---|
| 1 | Organic Play Store install, no link | `attribution_state=organic`, `attribution_is_organic=true`, `attribution_source=organic`, `install_store=play`, campaign fields null |
| 2 | Install via Singular link with UTMs in referrer params | `attribution_state=resolved`, `attribution_source`/`_campaign` match the link, `install_referrer_raw` non-empty, `attribution_conflict=false` |
| 3 | Install via Singular link **without** referrer params | resolved from Singular only, `install_referrer_raw` empty — proves §3.4 is unconfigured for that link |
| 4 | Install via deferred deep link to an article | `install_deferred_destination=article`, `install_deferred_entity_id` set, **app lands on that article after onboarding**, `install_attributed` fired once |
| 5 | Install from an in-app share link (Phase 2) | `attribution_source=App Share`, `attribution_share_id` present and joinable to a `story_shared` event |
| 6 | iOS, ATT denied | `attribution_state=resolved` or `organic`; campaign may be null; **must not** be `unresolved_timeout` |
| 7 | Singular answers at 4,500 ms | one `install_attributed` with `resolved_late=true`; `attribution_state` upgraded from `unresolved_timeout`; **no second `app_installed`** |
| 8 | First launch in airplane mode, network returns next session | `attribution_state=unresolved_timeout` on day 1; resolves on the later session **only if `attribution_locked` is still false** — decide and document (recommend: keep listening for 7 days, then lock permanently) |
| 9 | Reinstall on the same device | new install, new attribution row; on login the PostHog person merges — **expect first-touch to be the *original* install unless the merge overwrites it. Test this explicitly; it is the most likely silent data corruption** |
| 10 | TestFlight / internal build | `install_store=testflight\|internal` and the event does **not** reach project 146258 at all (see §7 item 2) |
| 11 | Re-open weeks later from a campaign | **no** `attribution_*` field changes. Any movement here means write-once is broken |

---

## 6. Why this is not one event with file 02

Collapsing install and open into a single model costs three things:

| Cost | Detail |
|---|---|
| Immutability is lost | Install source must never change; entry source must change every session. One field cannot have both rules — this is exactly the `app_opened.source` failure (`organic` and `deeplink` sitting where `brief`/`explore` also sit on sibling events) |
| Campaign leakage | A campaign open in October would rewrite the install source from August, destroying every acquisition cohort retroactively and silently |
| Different latency budgets | Install tolerates 3,000 ms once; a session open tolerates ~1,500 ms, 5,700 times a month |

The two are joined at analysis time by `person_id`, which is free. Merging them in the schema is not reversible.

---

## 7. Out of scope for this file

| Topic | Where it belongs |
|---|---|
| How a session was started (`organic` · `push` · deep link · deferred) | `02-tracking-app-open-source.md` |
| `entry_*` super properties, `register()` leakage, session boundaries | `02-tracking-app-open-source.md` §3 |
| In-app screen-to-screen origin (`referrer_screen`) | `app-attribution-source-mapping-spec.md` §6 |
| `deep_link_opened` noise guard (462/1,198 events are `auth_callback`) | `app-attribution-source-mapping-spec.md` §7 item 1 |
| Dev builds writing to production project 146258 | `app-attribution-source-mapping-spec.md` §7 item 2 — blocks clean install counts, fix first |
| PostHog ↔ Customer.io destination parity | separate workstream (Animesh), do not mix |
| Firebase / GA4 install reporting | out of scope entirely — Singular is the only MMP |

---

## 8. Decisions needed before this can be built

1. **Naming convention locked** (§0) — and the losing draft marked superseded.
2. **Singular link referrer params** (§3.4) — who configures, and for which links first? Without this, items 2 and 3 of the QA matrix are indistinguishable.
3. **Late-resolution window** (QA 8) — keep listening for 7 days, or lock at end of first session?
4. **Reinstall / person-merge behaviour** (QA 9) — is first-touch the first install ever, or the current install?
5. **Owner of the Singular → PostHog write** — app client reading the Singular callback (recommended, no server work), or a server-side postback → PostHog capture API?
