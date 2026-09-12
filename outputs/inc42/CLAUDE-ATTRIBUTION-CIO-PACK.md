# Claude pack — Attribution + CIO event miss (12 Sep 2026)

**Owner:** Ranjith / Product Manager agent  
**Purpose:** Full context to continue discussion in Claude. Do not invent; cite this pack.

---

## A. Slack issue (Animesh Kumar · 12 Sep ~4:19 PM IST)

**Slack (pasted):**
> @Ranjith M @Ritvik Sethi have found a few profiles where some of the events are not triggered on CIO.
> One such profile is lalitarorac9@gmail.com. This user has completed the brief, and he is a signed-in user as per PostHog, but I'm unable to see any events like brief_completed & signin_completed on CIO

**What it means**
- PostHog has evidence of brief completion + signed-in user.
- Customer.io (CIO) is missing `brief_completed` and sign-in completion for at least this profile (and “a few” others).
- Event name in Slack: `signin_completed` — Lifecycle/App sheet name is **`sign_in_completed`** (underscore). Check both when querying CIO.

**Likely failure classes to investigate (ordered)**
1. **Identity stitch:** PH person identified by email / distinct_id, but CIO profile never got the same `identify` / id — events fire in PH under anon or different id, never land on CIO profile Animesh is looking at.
2. **Destination fan-out:** Event fires to PostHog SDK path but CIO SDK / Rudder / reverse-ETL route drops it for some users.
3. **Name / schema mismatch:** CIO listens for different event name than app sends.
4. **Timing / session:** brief_completed fired before identify; CIO never backfills.

**Not the same problem as:** Singular install attribution (MMP). This is **PostHog ↔ Customer.io delivery / identity**.

---

## B. What audit did we do?

**Name / date:** App Audit **2026-08-29** (sheet tab “App Audit - 2026-08-29”; rows carried into Ashish App v3 as `audit_*` columns).

**Method (aggregate, not per-user):**
- For each taxonomy event: does it appear in **PostHog** in last ~90d (Y/N + volume)?
- Does it appear in **Customer.io** as **% of profiles** (Y + %)?
- Spot notes on broken props / missing setPersonProperties / renames.
- Destinations matrix from taxonomy: PostHog / Firebase / Customer.io / Singular.

**What it was NOT:**
- Not a per-email journey audit (PH user X → same events on CIO profile X).
- Not live QA of `lalitarorac9@gmail.com`.
- Not a full CIO campaign trigger test.
- Later taxonomy inventory (Event Audit / PM pack) explicitly treated Aug 29 audit tabs as **orientation only**, not SoT for property keys — Lifecycle sheet keys won for naming.

**Canonical App destinations count (taxonomy-summary):** ~55 App events → PostHog ~55, Customer.io **23**, Firebase 7, SKAN/Singular 10.

---

## C. Was Animesh’s issue in the audit?

### `brief_completed`
**YES — partially flagged, not as per-user miss.**

From App v3 / Aug 29 audit row:
- Destinations: `posthog | firebase | customerio | singular`
- PostHog: **Y** (953 in 90d)
- Customer.io: **Y (16% of profiles)** ← aggregate gap already visible
- `audit_status`: **no setPersonProperties call**
- Notes: Status unresolved — property-level not re-verified

So: audit said “event exists in CIO for some profiles” but **16% CIO vs healthy PH volume** already screamed incomplete fan-out / identity. It did **not** say “users with PH brief_completed lack CIO brief_completed.”

### `sign_in_completed`
**NO — not flagged as broken.**

Aug 29 row:
- Destinations: `posthog | customerio`
- PostHog: Y (1,250 in 90d)
- Customer.io: Y (**41% of profiles**)
- Status: **Working** — “No known issue; confirmed live”

41% was treated as “live” (many users never sign in → lower % expected). Audit **did not** reconcile PH-signed-in users vs CIO presence of `sign_in_completed`. Animesh’s case is exactly that missing reconciliation.

### Related CIO-hard fails that WERE called out (different events)
- `interest_captured` — absent BOTH PH and CIO (STILL BROKEN)
- `push_delivered` — absent both
- `profile_name_updated` — absent both
- `push_opened` — near-dead volume
- Several “setPersonProperties not working for non-logged-in” family

---

## D. Why was this missed in recent discussion (11 Sep attribution thread)?

1. **Wrong problem frame:** 11 Sep work was **Singular → PostHog open attribution** + **`source_screen` navigation**. Explicit Phase 1 out-of-scope: CIO fan-out, Fixing Events backlog, per-destination delivery.
2. **Audit false comfort:** Aggregate “CIO: Y (N% profiles)” for `sign_in_completed` / `brief_completed` looked “Working enough” — methodology cannot catch “this email has PH but not CIO.”
3. **brief_completed signal under-escalated:** 16% CIO + “no setPersonProperties” was logged but never promoted to a must-do / Fixing Events owner ticket in morning briefs the way rating-prompt / Design Done were.
4. **Naming:** Slack `signin_completed` vs sheet `sign_in_completed` can make CIO search look empty even when a differently named event exists (verify before concluding drop).
5. **Dev “Fixing Events”** sat open in Asana/briefs but was not the thread Ranjith pulled into PM chat that week (Companies IA + design + Singular dominated).

**Honest answer for Ranjith:** The CIO per-profile miss was **not invented today** — `brief_completed` already had a weak CIO % on 29 Aug — but we **did not** design an audit that would have found Animesh’s user, and we **did not** keep that gap in the active discussion queue. `sign_in_completed` was incorrectly marked “no known issue” at aggregate level.

---

## E. Attribution (store for Claude) — summary of locked draft

**File:** `singular-posthog-attribution-plan.md` (box: `/workspace/inc42-handover/`; also intended under `~/ClaudeDocs/inc42/`)

### Problem 1 — How did they open the app?
- Singular = MMP SoT for install/campaign.
- PostHog = product analytics; copy attr fields in.
- One `app_opened` after ~1.5–2s wait for Singular + push/deeplink.
- `open_source`: `organic` | `push` | `deeplink` | `deferred`
- Late Singular → `$set` + `attribution_updated` only (never second open).
- Login: same `user_id` in PH identify + Singular custom user id.

### Problem 2 — Previous screen inside app
- Event name = current surface.
- Stamp **`source_screen`** (previous) + optional `source_module` / `source_position`.
- Client keeps `last_screen` in session memory.
- Today App sheet has **no** universal `source_screen`; many rows wrongly show `source` enum `woocommerce|razorpay` (DataLabs leak).

### Story E2E example
1. `app_opened` open_source=organic  
2. `brief_page_opened` source_screen=home  
3. `brief_opened` source_screen=brief  
4. `card_viewed` …  
5. `article_opened` source_screen=brief_card  
6. `scroll_depth`  
7. `story_shared` source_screen=article  

Push path: `app_opened` open_source=push → `push_opened` → `article_opened` source_screen=push.

### Current App events inventory (66 in Ashish v3)
Includes lifecycle opens, brief funnel (`brief_page_opened` → `brief_opened` → `card_viewed` → `article_opened` → `brief_completed` / share/save), search, explore, company_profile, watchlist, push, auth (`sign_in_*`, register), onboarding, Application_* autocapture (dedupe TBD).

---

## F. How to go seamless (recommended next)

1. **Immediate (Ritvik + Animesh):** For `lalitarorac9@gmail.com` dump PH event timeline + CIO activity for same email / id; confirm event names; check identify order vs first brief_completed.
2. **Audit upgrade:** Sample N users who have PH `brief_completed` + identify email → assert CIO has same event within T minutes. Same for `sign_in_completed`. Fail = Fixing Events P0.
3. **Do not conflate** with Singular attribution ticket — separate epic: **Destination parity PH→CIO**.
4. Re-open Aug 29 findings that already smelled: brief_completed 16% CIO, missing setPersonProperties.

---

## G. Local paths
- This pack: `/workspace/inc42-handover/claude-attribution-cio-pack/START-HERE.md`
- Attribution plan: `/workspace/inc42-handover/singular-posthog-attribution-plan.md`
- App events + audit columns: `/workspace/inc42/ashish-v3-csv/App.csv`
- Taxonomy summary: `/workspace/inc42/taxonomy-summary.md`
