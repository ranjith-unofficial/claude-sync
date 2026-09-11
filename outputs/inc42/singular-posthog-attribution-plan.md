# Singular → PostHog attribution — implementation plan

**Date:** 11 Sep 2026 · **Status:** draft to lock with Dev  
**Constraint:** Singular = only MMP for now · PostHog = product analytics  
**Goal:** Every app open/install path is attributable in PostHog without double-counting opens; later stitch to logged-in user.

---

## 1. Principles (lock these)

1. **Singular owns** install + campaign / link attribution.  
2. **PostHog owns** product behaviour (screens, articles, shares, QIA inputs).  
3. On open: **one** PostHog `app_opened` (or existing open event name — use current name if already live).  
4. Wait briefly for Singular (and push/deeplink context), then fire PH open **with** attribution props.  
5. Late Singular callback → **enrich person** (`$set`) + optional `attribution_updated` — **never** a second open.  
6. On login: **same `user_id`** into PostHog `identify` and Singular custom user id.  
7. External entries (web CTA, share, paid) that must be attributed → **Singular links** (bare URLs stay blind organic).

---

## 2. Scope

### In scope (Phase 1)
- Open reason: `organic` | `push` | `deeplink` | `deferred`
- Copy Singular attribution fields onto PH person + open event
- Deferred deep link → navigate to content after first open
- Push tap → open props + navigate
- Login identity stitch (PH + Singular)
- QA matrix for the four open types

### Out of scope (Phase 1)
- Replacing Singular dashboards inside PostHog
- Multi-MMP / AppsFlyer
- Perfect share→install without Singular-wrapped share URLs (Phase 2)
- Universal `source_screen` on every in-app nav (Phase 2 — already called out with Utkarsh; separate ticket)
- Discover Companies new events (Phase 2 — product events, not MMP)

### Phase 2 (follow-on tickets)
- Article/company **share** uses Singular link template + `content_shared` event
- Web “Get App / Open in App” → Singular links only
- Universal `source_screen` / `source_module` on key screens
- Discover Companies event pack

---

## 3. Event & property contract

### 3.1 Open event (use existing name if already shipping)

**Event:** `app_opened` *(or current equivalent — confirm with Dev and Lifecycle sheet)*

| Property | Type | Values / notes |
|---|---|---|
| `open_source` | string | `organic` \| `push` \| `deeplink` \| `deferred` \| `unknown` |
| `attr_pending` | bool | `true` if fired on timeout before Singular returned |
| `attr_is_organic` | bool | From Singular |
| `attr_network` | string | Singular network (nullable) |
| `attr_campaign` | string | nullable |
| `attr_creative` | string | nullable |
| `attr_singular_link` | string | nullable |
| `deeplink_path` | string | Path/query from link (nullable) |
| `content_type` | string | `article` \| `company` \| `brief` \| … (nullable) |
| `content_id` | string | article_id / company_id / etc. (nullable) |
| `notif_id` | string | If push (nullable) |
| `session_id` | string | App session id |

### 3.2 Person properties (`$set` on open + on late attribution + on identify)

| Property | Meaning |
|---|---|
| `attr_first_network` / `attr_first_campaign` | First-touch (set once) |
| `attr_last_network` / `attr_last_campaign` | Last non-organic touch |
| `attr_last_open_source` | Last open_source |
| `attr_install_at` | ISO time if known |
| `attr_is_organic_install` | From first install attribution |

### 3.3 Optional late event

**Event:** `attribution_updated`  
Props: same attr_* fields + `reason=late_singular_callback`  
Do **not** increment open counts off this event.

### 3.4 Login

- PostHog: `identify(user_id)` + alias anonymous → user  
- Singular: set custom user id = **same** `user_id`  
- Re-`$set` person attrs so install attribution sticks on the known user

---

## 4. Runtime flow (implementation)

### 4.1 Cold start / resume

```
1. Init Singular SDK
2. Init PostHog SDK
3. Register:
   - Singular attribution callback
   - Singular / OS deeplink + deferred deeplink callback
   - Push open payload (if launched from notif)
4. Build OpenContext (mutable):
   - default open_source = unknown
   - fill from push payload immediately if present → open_source=push
   - fill from deeplink URL if present → open_source=deeplink + content_*
5. Wait up to T_ATTRIB (recommend 1500–2000 ms) for Singular attribution
   - if install-from-link / deferred → open_source=deferred, fill attr_*, content_*
   - if re-engagement campaign → fill attr_*; keep push/deeplink if already set
   - if organic → open_source=organic (unless push/deeplink already set)
6. Fire ONE PostHog open event with OpenContext
7. $set person properties (first-touch only if empty; always update last-touch)
8. Navigate if content_* present
9. If Singular returns AFTER timeout:
   - $set person
   - fire attribution_updated (no second open)
   - if deferred destination arrived late and UI still on home → navigate once
```

### 4.2 Priority if multiple signals

`push` or `deeplink` (explicit UI intent) **wins** for `open_source`.  
Singular campaign fields still attached.  
`deferred` only on **first open after install** from a link.

### 4.3 Timeout

- Default **2000 ms** (configurable).  
- On timeout: `open_source` = push/deeplink if known, else `unknown` or `organic`; `attr_pending=true`.

---

## 5. Engineering work breakdown

| # | Ticket | Owner | Done when |
|---|---|---|---|
| P1.1 | Confirm current open event name + existing PH props (Lifecycle / Event Agent) | Dev + Ranjith | Name locked; no rename without Lifecycle update |
| P1.2 | OpenContext module + Singular callback wiring | Dev | Unit/integration: props filled from mock callbacks |
| P1.3 | Single open emission + timeout + late enrichment | Dev | Never 2 opens; late → attribution_updated only |
| P1.4 | Push path: payload → OpenContext → navigate | Dev | QA: tap notif → correct screen + open_source=push |
| P1.5 | Deeplink + deferred path | Dev | QA: installed + link; fresh install + deferred |
| P1.6 | identify stitch PH + Singular on login | Dev | Same user_id both sides; anon merge in PH |
| P1.7 | QA matrix + PostHog insight sanity | Dev + Ranjith | Breakdown of opens by open_source + campaign |

**Phase 2 tickets (file after P1 ships)**  
P2.1 Share → Singular link template + `content_shared`  
P2.2 Web CTAs → Singular only  
P2.3 Universal `source_screen`  
P2.4 Discover Companies events  

---

## 6. QA matrix (must pass before “done”)

| # | Scenario | Expect in PostHog |
|---|---|---|
| 1 | Open from icon (no link) | `open_source=organic` (or unknown→organic), no campaign |
| 2 | Tap push to article | `open_source=push`, `content_id` set, lands on article |
| 3 | Cold open via Singular link (app installed) | `open_source=deeplink`, attr_* set, lands on content |
| 4 | Install via Singular link → first open | `open_source=deferred`, install attrs on person, lands on content |
| 5 | Singular slower than timeout | One open with `attr_pending=true`; later `attribution_updated`; still one open |
| 6 | Login after organic then later campaign open | identify merges; last-touch updates; first-touch stable |
| 7 | Double-open regression | Session start does not emit 2 opens |

---

## 7. Rollout

1. **Lock this doc** with Dev (property names + timeout + event name).  
2. Implement behind no feature flag needed if additive props only (safe).  
3. Validate in PostHog on staging / internal builds (QA matrix).  
4. Ship production; watch open volume (should not jump 2×).  
5. Add Phase 2 tickets for share/web/source_screen.

---

## 8. Decisions to confirm in the Dev sync (10 min)

1. Exact **open event name** today?  
2. Timeout **2000 ms** OK?  
3. First-touch person props: write-once — agree?  
4. Phase 1 excludes share/web Singular wrapping — agree?  
5. Who owns Lifecycle sheet update for new props — Ranjith / Ashish?

---

## 9. One-liner for the team

*Wait briefly for Singular + push/deeplink → fire one PostHog open stamped with open_source and campaign → late Singular only enriches → on login identify the same user_id in both SDKs.*
