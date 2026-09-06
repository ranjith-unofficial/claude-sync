# Inc42 App — Source Attribution & Journey Mapping Spec

**Status:** proposed, not approved
**Owner:** Ranjith M
**Date:** 6 September 2026
**Data source:** PostHog project 146258 (Inc42 App), 30 days to 6 Sep 2026
**Related:** `change-request-workflow.md` · "One Inc42 - Analytics | Master Sheet" (App tabs)

> Every volume in this document is a dated snapshot from the window above. Re-run the queries
> before citing a number as current.

---

## 1. The problem

Two questions the app cannot answer today:

1. **Where did this user come from?** — push, newsletter, share, web, paid, organic
2. **Where inside the app did they open this from?** — Brief card vs Explore vs search

Question 2 mostly works. Question 1 does not exist.

**Root cause:** one event property, `source`, is being made to answer both. Its value set mixes
external channels with in-app screens. `brief_page_opened` shows the collision plainly:

```
organic    5,434   <- external channel
deeplink     283   <- external channel
brief      1,165   <- in-app screen
watchlist    653   <- in-app screen
explore      523   <- in-app screen
profile      260   <- in-app screen
streak        92   <- in-app screen
tab           11   <- in-app screen
```

Because these are mutually exclusive values of one field, neither question can be asked
cleanly — and the combined question ("which acquisition channel produces users who finish the
Brief?") cannot be asked at all.

---

## 2. Measured current state

### 2.1 External attribution — effectively zero

| Signal | Reality |
|---|---|
| `utm_source` / `utm_medium` / `utm_campaign` | **0 events** carry any — across `app_opened` (4,358), `app_installed` (1,085), `deep_link_opened` (978), `register` (394) |
| `attribution_source` / `attribution_campaign` (person props) | **0% populated** — the Singular postback never writes back to PostHog |
| `app_opened.source` | Only two values ever: `organic` (3,648), `deeplink` (710). No push, banner, store, or share |
| `push_opened` | **0 events in 30 days**, despite ~67% push opt-in |
| Newsletter → app | 6 events carry `source=customer.io` — consistent with the known Customer.io click-tracker deep-link bug |
| Singular links | `sng.link` URLs arrive as raw `destination_screen`; **campaign never parsed in-app** |

### 2.2 `deep_link_opened` is 54% noise

978 events in 30 days. Only ~451 are genuine external entries.

| Bucket | Events | People | Verdict |
|---|---|---|---|
| `campaign=auth_callback` (Auth0 OAuth return) | 396 | 371 | noise |
| Real `inc42.com` web links | 279 | 103 | ✅ genuine |
| `sng.link` (Singular), campaign unparsed | 172 | 66 | ✅ genuine, unusable |
| In-app routes (`brief/read`, `(tabs)/profile`, `streak`) | 75 | 9 | noise — real code path |
| `192.168.1.x:8083` (Expo/Metro dev servers) | 56 | 4 | noise — dev builds |

**Confirming evidence:** 396 `auth_callback` events vs 394 `register` events in the same
window — essentially 1:1 with sign-ins. The deep-link handler logs *any* inbound URL, including
the app's own OAuth return.

**Verified 6 Sep:** the in-app-route rows are **not** just developers. Of the 12 people
producing dev-IP or in-app-route events, only one produces both; eight log in-app-route deep
links with zero dev traffic. The in-app router is calling the deep-link logger on internal
navigation in production. The guard must therefore test "was the app entered from outside",
not merely exclude dev builds.

**Consequences today:** "% of entries via deep link" is overstated ~1.7×; any "deep link →
article opened" conversion has a denominator that is 40% auth redirects which structurally
never open an article; and the dev-server rows prove dev builds write to the production
PostHog project, which pollutes far more than this one event.

### 2.3 In-app navigation already works on 7 events

`article_opened.source`:

| Value | Opens |
|---|---|
| explore | 858 |
| brief_card | 600 |
| deeplink | 586 |
| article_reader | 116 |
| search | 76 |
| company_page | 59 |
| sector_landing | 21 |
| watchlist | 12 |

Same pattern on `story_saved`, `story_shared`, `company_profile_viewed`,
`sector_landing_viewed`, `profile_opened`, `streak_opened`.

**Gaps:** `explore_viewed` (7,419 events), `watchlist_viewed` (1,797), `search_result_tapped`
(274) carry no origin property at all.

**Enabler already in place:** `$session_id` is present on 100% of events — 105,975 events
across 4,390 sessions in 30 days.

---

## 3. The model — three layers, never merged

| Layer | Question | Scope | Storage | Prefix |
|---|---|---|---|---|
| 1 · Install | Which campaign brought this install? | Once per install, permanent | Person properties | `attribution_*` |
| 2 · Session entry | How did they get in *this time*? | Once per session, on every event in it | PostHog super properties | `entry_*` |
| 3 · Navigation | Which screen did they come from? | Per event | Event property | `referrer_*` |

**Hard rule:** no property may hold values from two layers. `deeplink` is only ever an
`entry_channel`. `explore` is only ever a `referrer_screen`.

**Naming guard — must be written into the tracking sheet:** despite the web connotation,
`referrer_*` here means **in-app origin screen only**. External origin is always `entry_*`.
This was chosen deliberately over `from_screen`; the ambiguity is accepted and must be spelled
out wherever the property is defined.

**`surface` is NOT reusable for Layer 3.** It already exists in production and means *"which
screen this element is displayed on"* — the opposite of origin:

| Event | `surface` values |
|---|---|
| `summary_expanded` | brief_card 762 · company_card 564 · explore_gist 232 · explore_s1 89 · company_page 30 |
| `error_shown` | explore 215 · brief 141 · brief_reader 49 · company_profile 26 |

The value vocabulary overlaps almost exactly with Layer 3's, with inverted meaning. Leave
`surface` untouched.

---

## 4. Layer 1 — Install attribution (person properties)

`attribution_source` · `attribution_medium` · `attribution_campaign` · `attribution_creative` ·
`attribution_network` · `install_referrer_raw`

- Written on `app_installed` from the Singular postback + Play Install Referrer + Apple `ct`
  token. **Immutable after first write** — never overwrite on a later session.
- Requires the already-diagnosed link fix: add `utm_source` / `utm_medium` / `utm_campaign`
  under each Singular link's **Google Play referrer / custom referrer parameters**, so Firebase
  and PostHog see the campaign instead of only Singular resolving it server-side.
- Keep the existing Singular convention: channel-level source (`Offline Events`, `Email`,
  `Web Banner`, `Product Hunt`), campaign identity in `pcn`, creative in `pcrn`, placement in
  `psn`.

---

## 5. Layer 2 — Session entry (super properties)

### 5.1 Properties

| Property | Values |
|---|---|
| `entry_channel` | `organic` · `push` · `deeplink_web` · `deeplink_email` · `deeplink_share` · `deeplink_social` · `app_banner` · `widget` |
| `entry_source` | `customer_io` · `inc42_web` · `whatsapp` · `linkedin` · `product_hunt` · `offline_qr` — channel-level, matching the Singular Partner convention |
| `entry_campaign` | from `pcn` / push payload — e.g. `morning_newsletter`, `d2c_retail_summit_2026` |
| `entry_content` | creative / placement — from `pcrn` / `psn` |
| `entry_destination` | normalised screen: `article` · `brief` · `company_profile` · `home` |
| `entry_entity_id` | story_id / company_id the link targeted |
| `entry_is_deferred` | true when resolved from Singular's deferred deep-link payload post-install |
| `share_id` | present when `entry_channel = deeplink_share` |

### 5.2 How it is tracked

A single resolver — `resolveEntryAttribution()` in the app's analytics module — called from
exactly four places, writing the block once via `posthog.register({...})`.

From that call on, PostHog attaches `entry_*` to **every** subsequent event automatically.
No per-event work, and no touching the 55 existing event call-sites.

| Caller | Sets |
|---|---|
| Cold start / foreground after session expiry | `entry_channel = organic` (default) |
| Singular deep-link callback (`withSingularLink`) | `deeplink_*`; parse `pcn` / `pcid` / `pcrn` / `psn` into `entry_campaign` / `entry_content` |
| RN `Linking.getInitialURL()` + `addEventListener('url')` | `deeplink_web` / `deeplink_share`, parsed from the URL |
| Push tap handler (FCM / Customer.io) | `entry_channel = push`, `entry_campaign` from the message payload |

### 5.3 Three constraints — each is a real bug if missed

1. **`register()` persists across sessions in the PostHog RN SDK.** The resolver must rewrite
   the *entire* `entry_*` block every session, including explicitly resetting to `organic`.
   Otherwise one push-opened session leaks its campaign into every subsequent organic session.
   **This is the highest-risk defect in the design.**
2. **Session boundary ≠ `app_opened`.** PostHog rotates `$session_id` after 30 minutes idle.
   Hook `AppState → active` and re-run the resolver when background time ≥ 30 min, not only on
   cold start.
3. **Cold-start race.** `app_opened` fires before the deep-link/push payload arrives.
   **Decision: delay `app_opened`** until the resolver settles or a **1,500 ms timeout** fires
   (falling back to `organic`), then `register()`, then capture. Every event in the session —
   including `app_opened` itself — then carries correct attribution. Acceptable because
   `app_opened` is not latency-critical and is already double-fired by the SDK's
   `captureApplicationLifecycleEvents` autocapture.

### 5.4 Shares

`story_shared` mints a `share_id` into the outbound URL. Inbound resolution reads it back →
`entry_channel = deeplink_share` + `share_id`. This is the only mechanism that makes "someone
shared it" measurable.

### 5.5 Customer.io

Super properties are a PostHog-SDK mechanism. If the `entry_*` block is wanted on Customer.io
events too, it must be passed explicitly in those calls — it will not appear automatically.

---

## 6. Layer 3 — Navigation origin (event property)

`referrer_screen` · `referrer_position` (rank in list/carousel) · `referrer_module`
(`related_stories`, `beyond_brief`, `trending`)

`referrer_screen` enum: `brief_card` · `brief_end` · `explore_articles` · `explore_companies` ·
`search` · `watchlist` · `company_page` · `sector_landing` · `article_reader` · `profile` ·
`streak` · `tab_bar`

- The 7 events already using `source` correctly keep their existing values — this is a rename,
  not a re-derivation.
- Add to the three events with no origin today: `explore_viewed`, `watchlist_viewed`,
  `search_result_tapped`.
- Remove `organic` / `deeplink` from `brief_page_opened` and `article_opened`; those values move
  to `entry_channel`.

---

## 7. Fix sequence

| # | Change | Type | Rationale |
|---|---|---|---|
| 1 | Guard `deep_link_opened`: fire only when the app was cold/backgrounded, the host is a public owned domain, and the path is not the auth callback | Bug fix | 54% of the event is noise; every external number is wrong until this lands |
| 2 | Route dev builds to a separate PostHog project (or kill-switch analytics in dev) | Bug fix | Dev builds currently write to production |
| 3 | Make `push_opened` fire | Bug fix | 0 events / 30d blocks `entry_channel = push` entirely |
| 4 | Parse the Singular deep-link payload in-app into `entry_*` | Schema | Turns 172 opaque `sng.link` opens into campaigns |
| 5 | Add UTMs to Singular link referrer params | Config | Fixes Firebase/GA4 showing installs with no campaign |
| 6 | Wire the Singular postback → PostHog person props | Integration | `attribution_source` is 0% populated |
| 7 | Ship the Layer 2 resolver + `register()`, and rename `source` → `referrer_screen` **in the same release** | Schema | Values must never mix across the cut |
| 8 | Route newsletter links through Singular instead of the Customer.io click-tracker | Config | Fixes deep linking *and* attribution in one move |

Steps 1–3 are independent bug fixes and can ship first with no schema decision.
Steps 4–8 are the schema change and go through `change-request-workflow.md`, with the
"One Inc42 - Analytics | Master Sheet" App tabs updated in the same pass.

**Breaking change to flag:** step 7 makes `brief_page_opened` and `app_opened` history
un-joinable across the cut. Decide before the release whether to dual-write `source` and
`referrer_screen` for one version, or accept the break.

---

## 8. Verification

All queries against PostHog project 146258.

**After steps 1–3**
- `deep_link_opened` volume drops to roughly the ~451/30d genuine baseline
- Zero rows where `campaign = 'auth_callback'`, or `destination_screen` matches an IP literal
- `push_opened` returns non-zero; cross-check against Customer.io send volume for the window
- No production events carry a `192.168.x.x` destination

**After step 7 — Layer 2**
- Every session carries exactly one non-null `entry_channel`; `pending` never appears
- `organic` is the clear majority; `push` is non-zero
- **Leakage test (the critical one):** for each person, confirm `entry_channel` returns to
  `organic` on the session *after* a `push` session. A person showing `push` across many
  consecutive sessions means `register()` is not being reset — the failure mode from
  constraint 1 in §5.3.
- Cross-check `entry_campaign` values against Singular's own dashboard for the same dates —
  they should agree on campaign *names*, not just counts

**After step 7 — Layer 3**
- `referrer_screen` never contains `organic` or `deeplink`
- `explore_viewed`, `watchlist_viewed`, `search_result_tapped` >95% populated
- `surface` values unchanged on `summary_expanded` / `error_shown` — proves the rename did not
  disturb the adjacent property

**The payoff query** — impossible today, works after step 7:

```sql
SELECT properties.entry_channel   AS channel,
       properties.referrer_screen AS from_screen,
       count()                    AS opens
FROM events
WHERE event = 'article_opened'
  AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY channel, from_screen
ORDER BY opens DESC
```

Plus `brief_completed` (north star) broken down by `entry_channel` — the acquisition-quality
question that has no answer at all right now.

---

## 9. Open items

- **Dual-write decision** for step 7 (§7) — product call, not engineering.
- **`entry_*` on Customer.io** — decide whether lifecycle campaigns need entry channel; if so it
  must be passed explicitly per call (§5.5).
- **Project owner sign-off** — `change-request-workflow.md` step 3 requires it; no owner registry
  exists for the App project.
