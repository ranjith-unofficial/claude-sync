# Layer B — Tracking app open source

**Owner:** Ranjith M · **Status:** proposed, not approved · **Date:** 12 September 2026
**Scope:** SESSION ENTRY only — how this session started. Install attribution → `01-tracking-app-installation-source.md`. In-app navigation → `app-attribution-source-mapping-spec.md` §6.
**Live state verified:** PostHog project 146258, 30 days to 12 Sep 2026. Re-run before citing any number as current.

---

## 0. Naming decision

Same as file 01 §0 — **`attribution_*` (install) / `entry_*` (session) / `referrer_*` (in-app)**. This file does **not** use `open_source`, because the word `source` is the field that caused the collision it is meant to fix: today `app_opened.source` holds `organic`/`deeplink` while `article_opened.source` holds `explore`/`brief_card`. Two layers, one word, sibling events.

---

## 1. Problem

The app fires 5,733 `app_opened` events across 5,772 sessions and 1,341 people in 30 days, but `app_opened.source` has only ever held two values — `organic` (4,738) and `deeplink` (995). Push is structurally invisible: the `push_type` property is present on **100% of `app_opened` events with a literal `null` value on 100% of them**, and `push_opened` **does not exist in the project at all** despite ~67% push opt-in and 1,317 permission prompts in the window. Inbound links land in a separate `deep_link_opened` event where 462 of 1,198 events (38.6%) are the app's own Auth0 callback. The result: "how did users get in this session" is answerable only as organic-vs-deeplink, the share channel cannot be separated from the newsletter channel, and no acquisition channel can be crossed with `brief_completed` (1,124 in the window) — the north-star question.

### 1.1 Measured current state (30d to 12 Sep 2026)

| Signal | Live reality |
|---|---|
| `app_opened` | 5,733 events · 5,417 distinct sessions · Android 761 people / iOS 537 / iPadOS 26 |
| `app_opened.source` values | `organic` 4,738 · `deeplink` 995. **No push, share, banner, store or widget value has ever appeared** |
| `app_opened.push_type` | present on 5,733/5,733 events · **value null on all 5,733** |
| `push_opened` | **event does not exist** (0 events, absent from the 55-event census) |
| Sessions without any `app_opened` | 355 of 5,772 (6.2%) — foreground-after-idle rotates `$session_id` with no open event |
| Sessions with more than one `app_opened` | ~316 — mild double-fire alongside the SDK's own `Application Opened` (5,497) |
| `deep_link_opened` | 1,198 events · `campaign=auth_callback` 462 (38.6% noise, unchanged since 6 Sep) · `morning-newsletter` 16 · null 718 |
| `deep_link_opened` UTM-shaped block | **already exists** as `source` / `medium` / `content` / `campaign` / `link_url` / `destination_screen` (no `utm_` prefix) |
| Inbound share clicks | detectable today: `medium=app_share`, `source=inc42_app` → **72 events / 30d** |
| Newsletter clicks | `medium=email`, `source=customer.io`, `content=aug-25`/`sep-11`/… → ~20 events / 30d, consistent with the known Customer.io click-tracker bug |
| `$session_id` coverage | 132,438 / 132,438 = **100%** — the enabler for everything below |
| `entry_channel` / `open_source` / `referrer_screen` | 0 of 132,435 events. Nothing from either draft is implemented |

**Correction to the 6 Sep spec:** it recorded "0 events carry any UTM". Literally true for `utm_`-prefixed names, but `deep_link_opened` **does** carry a parsed `source`/`medium`/`content`/`campaign` block on 1,195 of 1,198 events. The parser exists. What is missing is (a) promoting it to session scope so it lands on *every* event in the session, and (b) the push branch.

---

## 2. Event & property contract

### 2.1 `entry_*` — PostHog super properties, re-registered every session

Registered once per session via `posthog.register({...})`; PostHog then attaches the block to **every subsequent event automatically**, including `brief_completed` and `article_opened`. No per-event work, and none of the ~55 existing call-sites are touched.

| Property | Type | Values / notes | Req |
|---|---|---|---|
| `entry_channel` | enum | `organic` · `push` · `deeplink_web` · `deeplink_email` · `deeplink_share` · `deeplink_social` · `deeplink_paid` · `app_banner` · `widget` · `unknown` | **yes** |
| `entry_source` | string | channel level, matching the Singular Partner convention: `customer_io` · `inc42_web` · `whatsapp` · `linkedin` · `product_hunt` · `offline_qr` · `inc42_app` | no |
| `entry_campaign` | string | from Singular `pcn`, the push payload, or `deep_link_opened.campaign` (`morning-newsletter`, …) | no |
| `entry_content` | string | creative / placement / send-date — from `pcrn` / `psn` / existing `content` | no |
| `entry_destination` | enum | normalised: `article` · `brief` · `company_profile` · `sector_landing` · `home` | no |
| `entry_entity_id` | string | story_id / company_id targeted | no |
| `entry_is_deferred` | bool | `true` when resolved from Singular's deferred payload on a first open | **yes** |
| `entry_resolved` | bool | `false` when the §3.3 timeout fired before any signal arrived | **yes** |
| `share_id` | string | present when `entry_channel=deeplink_share` — joins back to the sharer's `story_shared` | no |

**`deferred` is a modifier, not a channel.** Grok's brief lists `deferred` as a fourth value of open source; that collapses *how they arrived* into *when it resolved*. A deferred install-open from a newsletter link is `entry_channel=deeplink_email` **and** `entry_is_deferred=true` — two facts, both keepable. Making `deferred` a channel value throws away the channel on precisely the highest-value session a user ever has (their first).

### 2.2 `app_opened` — stays the single open event

| Change | Detail |
|---|---|
| `source` | **retire.** Its two values move to `entry_channel`. Dual-write for one release or accept the history break — product call (see §7) |
| `push_type` | already present, always null → becomes real on the push branch: `brief` · `story` · `streak` · `watchlist` · `system` |
| `notif_id` | **add** — message id from FCM / Customer.io, for send→open joins |
| `entry_*` | attached automatically by `register()`, including onto `app_opened` itself (requires §3.3) |

Volume must not change. Any jump means the resolver is emitting a second open.

### 2.3 `push_opened` — new event, currently absent

Fires on notification tap, **in addition to** `app_opened` (which reports the session; this reports the tap). Props: `push_type`, `notif_id`, `entry_campaign`, `entry_destination`, `entry_entity_id`, `push_state` (`cold` · `background` · `foreground`).

Without this event, `entry_channel=push` can never be validated against Customer.io send volume — there is nothing to join to.

### 2.4 `story_shared` — add `share_id` (Phase 2)

196 shares / 30 days (`channel`: link 146 · other 25 · whatsapp 23 · linkedin 1) and **not one of them is traceable to an inbound click**, because the outbound URL carries nothing that identifies the share. Minting a `share_id` into the shared URL and reading it back on entry is the *only* mechanism that makes "someone shared this and it brought people in" measurable. It also closes the loop into `attribution_share_id` (file 01 §2.2) for share-driven installs.

### 2.5 Person properties — last-touch only

| Property | Notes |
|---|---|
| `entry_last_channel` · `entry_last_campaign` · `entry_last_at` | overwritten every session; for Customer.io targeting and recency segments |

Last-touch lives here, **never** in `attribution_*` — that block is immutable install truth.

---

## 3. Runtime flow

### 3.1 The resolver

One function — `resolveEntryAttribution()` — called from exactly four places, writing the whole `entry_*` block in a single `register()`.

| Caller | Sets |
|---|---|
| Cold start | `entry_channel=organic` default, then awaits the signals below |
| Push tap handler (FCM / Customer.io) | `entry_channel=push`, `push_type`, `notif_id`, `entry_campaign` |
| RN `Linking.getInitialURL()` + `addEventListener('url')` | `deeplink_web` / `deeplink_share` / `deeplink_social`, parsed from the URL (+ `share_id`) |
| Singular deep-link callback (`withSingularLink`) | `deeplink_paid` / `deeplink_email`, parsing `pcn` / `pcid` / `pcrn` / `psn`; sets `entry_is_deferred` on first open |
| **AppState → active** after ≥30 min background | re-runs the whole resolver (see §3.2 constraint 2) |

### 3.2 Three constraints — each is a real bug if missed

| # | Constraint | Failure if missed |
|---|---|---|
| 1 | **`register()` persists across app launches** in the PostHog RN SDK. The resolver must rewrite the **entire** block every session, explicitly resetting to `organic` | One push session leaks its campaign into every later organic session. **Highest-risk defect in this design** — it inflates campaign performance indefinitely and looks like success |
| 2 | **Session boundary ≠ `app_opened`.** PostHog rotates `$session_id` after 30 min idle — 355 of 5,772 sessions (6.2%) already have no open event. Hook `AppState → active` on background time ≥30 min | 6% of sessions carry the *previous* session's entry block |
| 3 | **Cold-start race:** `app_opened` fires before the deep-link/push payload arrives | `app_opened` itself is unattributed — the one event most people will break down by |

### 3.3 Race resolution — delay the open, 1,500 ms

**Decision: delay `app_opened`** until the resolver settles or 1,500 ms elapses (fallback `entry_channel=organic`, `entry_resolved=false`), then `register()`, then capture. Every event in the session — `app_opened` included — then carries the correct block.

Acceptable because: `app_opened` is not latency-critical, nothing user-visible waits on it, and the SDK's `captureApplicationLifecycleEvents` already emits `Application Opened` (5,497/30d) for anyone who needs an undelayed lifecycle signal.

**Note the asymmetry with file 01:** installs wait 3,000 ms (once ever), opens wait 1,500 ms (5,700×/month). Same mechanism, different budget, deliberately.

### 3.4 Priority when signals collide

| # | Signal | Wins because |
|---|---|---|
| 1 | Push tap | explicit user intent, unambiguous — a tap on a notification is why this session exists |
| 2 | Explicit deep link URL (`Linking`) | explicit intent, deterministic parse |
| 3 | Singular deferred payload (first open after install only) | the only way a post-install destination is knowable |
| 4 | Singular re-engagement campaign | probabilistic; attaches `entry_campaign` but must **not** override 1–3's channel |
| 5 | nothing by timeout | `entry_channel=organic`, `entry_resolved=false` |

Campaign fields from a lower-priority signal still attach — only `entry_channel` is exclusive.

---

## 4. PostHog vs Singular

| | Singular | PostHog |
|---|---|---|
| Session entry channel | no | **yes — sole owner** |
| Re-engagement campaign credit | **yes** | consumes it into `entry_campaign` |
| Push opens | no (not an MMP concern) | **yes** |
| Share-driven entries | only if the share URL is Singular-wrapped (Phase 2) | **yes, via `share_id`** |
| "Which channel produces Brief completions" | no | **yes** |

Singular is read-only input to Layer B. Every value above except `entry_campaign` on paid/email is computed by the client.

### 4.1 Customer.io caveat

Super properties are a **PostHog-SDK mechanism**. `entry_*` will **not** appear on Customer.io events automatically; if lifecycle campaigns need entry channel it must be passed explicitly per call. Decide before build.

---

## 5. QA matrix

| # | Scenario | Expected |
|---|---|---|
| 1 | Open from icon | `entry_channel=organic`, `entry_resolved=true`, all campaign fields null |
| 2 | Tap push to an article | `entry_channel=push`, `push_type` + `notif_id` set, `entry_destination=article`, **`push_opened` fires**, lands on the article |
| 3 | Push tap while app is in foreground | `push_opened` with `push_state=foreground`; **no** new `app_opened`; `entry_*` updates only if the session boundary was crossed |
| 4 | Cold open via Singular paid link, app installed | `entry_channel=deeplink_paid`, `entry_campaign` matches Singular's own dashboard **by name**, `entry_is_deferred=false` |
| 5 | First open after install via newsletter link | `entry_channel=deeplink_email`, `entry_source=customer_io`, `entry_is_deferred=true`, and `attribution_*` written once (file 01) |
| 6 | Open from a WhatsApp-shared article link | `entry_channel=deeplink_share`, `share_id` present and joinable to the original `story_shared` |
| 7 | Signal arrives at 2,000 ms | one `app_opened` with `entry_resolved=false`; late signal may update `entry_*` for the rest of the session; **never a second open** |
| 8 | **Leakage test — the critical one.** Push session, then an organic session | `entry_channel` returns to `organic` on the next session. A person showing `push` across consecutive sessions means `register()` is not being reset (§3.2 constraint 1) |
| 9 | Background 45 min, foreground | resolver re-runs, new `$session_id` carries a fresh `entry_*` block |
| 10 | Background 2 min, foreground | **no** re-resolve, same session, same block |
| 11 | Auth0 sign-in round trip | **no** `entry_*` change and **no** `deep_link_opened` — today this produces 462 false deep links per 30 days |
| 12 | Volume regression | `app_opened` stays near 5,700/30d and `entry_channel` is non-null on ~100% of events; `unknown` never appears in production |

---

## 6. Why this is not one event with file 01

| Cost of merging | Detail |
|---|---|
| Mutability conflict | `entry_*` must be rewritten every session; `attribution_*` must never be rewritten. One model cannot enforce both |
| Retroactive destruction | A campaign open in October would rewrite the August install source, silently invalidating every acquisition cohort already reported |
| Latency | 3,000 ms once vs 1,500 ms per session |
| Both are needed at once | "Installed from Product Hunt in August, opened from a WhatsApp share today" is a single sentence that a merged model cannot express |

---

## 7. Out of scope for this file

| Topic | Where |
|---|---|
| Which campaign produced the install | `01-tracking-app-installation-source.md` |
| Play Install Referrer, deferred destination storage, write-once rules | `01-…` §2.2, §3 |
| In-app screen origin (`referrer_screen`, `referrer_module`, `referrer_position`) — incl. the 9,120 `explore_viewed` / 2,056 `watchlist_viewed` / 330 `search_result_tapped` events with no origin at all | `app-attribution-source-mapping-spec.md` §6 |
| `deep_link_opened` noise guard (462 auth callbacks, in-app routes, dev-server IPs) | same spec §7 item 1 — **every external number here is wrong until it lands** |
| Dev builds writing to production 146258 | same spec §7 item 2 |
| Routing newsletter links through Singular instead of the Customer.io click-tracker | same spec §7 item 8 — fixes deep linking *and* attribution in one move |
| PostHog ↔ Customer.io destination parity | separate workstream (Animesh) |

---

## 8. What this unlocks (impossible today)

```sql
-- Acquisition quality: which channel produces Brief completions
SELECT properties.entry_channel AS channel,
       uniq(person_id)          AS people,
       countIf(event = 'brief_completed') AS completions
FROM events
WHERE timestamp >= now() - INTERVAL 7 DAY
GROUP BY channel ORDER BY completions DESC
```

```sql
-- Layer B x Layer C: how they got in, and where they tapped from
SELECT properties.entry_channel   AS channel,
       properties.referrer_screen AS from_screen,
       count()                    AS article_opens
FROM events
WHERE event = 'article_opened' AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY channel, from_screen ORDER BY article_opens DESC
```

---

## 9. Decisions needed before this can be built

1. **Naming convention locked** (§0), losing draft marked superseded.
2. **Dual-write `source` and `entry_channel` for one release, or accept the history break** on `app_opened` and `brief_page_opened`? Product call, not engineering.
3. **1,500 ms open delay approved?** It moves a 100%-coverage event behind a timer.
4. **`entry_*` on Customer.io** (§4.1) — needed for lifecycle campaigns, or PostHog-only?
5. **`push_opened` owner** — it does not exist today, and `entry_channel=push` cannot be validated without it.
6. **`share_id` in Phase 1 or Phase 2?** Without it, 196 shares/month stay unattributable, and `medium=app_share` (72 inbound/month) can count clicks but never tie them to a sharer or a story.
