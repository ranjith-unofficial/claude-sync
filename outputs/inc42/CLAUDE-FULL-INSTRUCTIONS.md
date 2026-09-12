# CLAUDE AGENT INSTRUCTIONS — Inc42 App PostHog ↔ Customer.io event parity + context

**Date packed:** 2026-09-12 (IST)  
**From:** Ranjith via Product Manager agent (Grok Bot)  
**Purpose:** Paste/open this as the full brief for Claude. Do not invent numbers; cite artifacts below. Act on the “What Claude should do next” section unless Ranjith overrides.

---

## 0. One-line problem

**Some App users have complete journeys in PostHog (including `brief_completed` and `sign_in_completed`) but the same terminal events never appear (or appear inconsistently) on their matching Customer.io profile — so CIO campaigns/automation that depend on those events will miss users even when product analytics says they converted.**

This is **not** the Singular attribution problem. Singular = MMP / install & open. This pack is **destination parity: PostHog ↔ Customer.io** for the Inc42 App.

---

## 1. What Claude should tell / how to frame it (for humans)

Use this framing when summarizing to Ranjith, Ritvik, Animesh, or Eng:

> We audited Inc42 App events across PostHog and Customer.io. Aggregate “event exists” is not enough. For a given user, the journey events that fired in PostHog must also land on the same Customer.io identity.  
> Animesh’s example (`lalitarorac9@gmail.com`) is confirmed: PostHog has `brief_completed`, `sign_in_completed`, and `register` after identify on id `209480`; Customer.io has the same profile and mid-funnel events (`brief_opened`, `card_viewed`, etc.) but is **missing those three terminal events**.  
> Across a 25-user sample who completed brief in PostHog, **12%** lack `brief_completed` on CIO (no profile or no event). Auth event drops are intermittent (sample understates; Exhibit A proves drop after identify).  
> Root causes in evidence: selective fan-out of tracks, pre-identify anon events on UUID CIO ids, and attribute-updates without track events.  
> Separate backlog: several events are dead in both systems (`interest_captured`, `push_delivered`, `profile_name_updated`, `push_opened`).  
> Do not conflate with Singular→PostHog open attribution / `source_screen` work — that is a parallel epic.

---

## 2. Background — what happened (chronology)

### A. Prior audit (29 Aug 2026) — aggregate only
- Sheet / Ashish App rows carry `audit_*` from **App Audit 2026-08-29**.
- Method: PostHog 90d volume Y/N + Customer.io **% of profiles** (not per-email journey).
- `brief_completed`: PH Y (953/90d), CIO Y but only **16% of profiles**, status **no setPersonProperties** — under-escalated.
- `sign_in_completed`: marked **Working** (PH Y, CIO 41%) — **false comfort**; method cannot catch “PH yes / CIO no for this email.”
- That is why Animesh’s class of bug looked “new” even though brief_completed CIO weakness was already visible at aggregate level.

### B. 11 Sep 2026 — Singular → PostHog attribution (different problem)
- Ranjith asked how someone opens the app + previous-screen navigation.
- Draft plan: `singular-posthog-attribution-plan.md`
  - Phase 1: one `app_opened` after ~1.5–2s Singular/push/deeplink wait; `open_source` = organic|push|deeplink|deferred; late Singular → `$set` / `attribution_updated` only; same `user_id` on login in PH + Singular.
  - Phase 2: Singular-wrapped shares/web; universal `source_screen` / `source_module` / `source_position` (previous screen; event name = current surface).
- App sheet today often misuses `source` with DataLabs enum `woocommerce|razorpay` — **not** navigation.
- **Out of scope for that thread:** CIO fan-out / Fixing Events destination parity.

### C. 12 Sep 2026 ~4:19 PM IST — Animesh Slack
Exact issue (paraphrase ok; substance locked):

> @Ranjith M @Ritvik Sethi found profiles where some events are not triggered on CIO.  
> Example: **lalitarorac9@gmail.com** — completed brief and is signed-in in PostHog, but CIO missing events like **brief_completed** & **signin_completed**.

Notes:
- Sheet/Lifecycle name is **`sign_in_completed`** (underscores). Slack said `signin_completed`. Both were checked on Exhibit A — **neither** on CIO. Naming alone is not the bug for that user.
- Ranjith asked: what audit did we do; was this mentioned; why missed; store everything for Claude.

### D. 12 Sep 2026 — New audit commissioned
Ranjith required:
1. Entire App event list checked in PostHog **and** Customer.io.
2. **Combined user journey:** for a given user, the set of events that should have fired must appear in both systems; report gaps.
3. Not only Exhibit A.

**What was actually delivered (be precise with Claude):**

| Layer | Coverage | Depth |
|-------|----------|--------|
| Event-level matrix | **All 66** events in `App.csv` | PH 30d counts + CIO catalog/daily_count vs expected destinations |
| Per-user journey cohort | **`brief_completed` (n=25)** and **`sign_in_completed` (n=15)** | PH person with email → CIO profile → event logs |
| Exhibit A full journey | **lalitarorac9@gmail.com** | Full PH timeline vs CIO activity diff |

**Not yet done:** multi-user journey cohort for every one of the ~23 CIO-expected App events (only brief + sign_in got that depth). Next pass if Ranjith asks.

---

## 3. Systems of record (do not mix projects)

| System | Name | ID |
|--------|------|-----|
| PostHog | **Inc42 App** | project **`146258`** |
| Customer.io | **Inc42 App** | workspace **`224949`** |
| Taxonomy | Ashish / Lifecycle App list | `/workspace/inc42/ashish-v3-csv/App.csv` (66 events) |

**Trap:** MCP/default PostHog context can open **Media** project `53557` first — App events will look empty. Always use App `146258` for this audit.

Local Mac copies (Ranjith):
- `~/ClaudeDocs/inc42/PER-USER-JOURNEY-AUDIT-REPORT.md`
- `~/ClaudeDocs/inc42/event-level-ph-cio-gaps.md`
- `~/ClaudeDocs/inc42/cohort-parity-brief-signin.md`
- `~/ClaudeDocs/inc42/CLAUDE-ATTRIBUTION-CIO-PACK.md` (earlier start pack)
- `~/ClaudeDocs/inc42/singular-posthog-attribution-plan.md`

Box pack folder:
`/workspace/inc42-handover/claude-attribution-cio-pack/`  
Files: `PER-USER-JOURNEY-AUDIT-REPORT.md`, `journey-lalitarorac9.md`, `cohort-parity-brief-signin.md`, `event-level-ph-cio-gaps.md`, `app-event-destination-matrix.csv`, `START-HERE.md`, this file.

---

## 4. Exhibit A — detailed (lalitarorac9@gmail.com)

### Identity
| | |
|--|--|
| Email | lalitarorac9@gmail.com |
| PH person_id | `41d2a88e-7ca5-55a4-b505-c6a632d44ff1` |
| PH / CIO shared external id | **`209480`** |
| CIO internal_id | `b5dd0d00d812d912` |
| Profile in both? | **YES** |

CIO attrs present: `is_registered=true`, `registration_date=2026-09-12T06:22:29.916Z`, walkthrough completed, push_opt_in.  
CIO attrs **missing** despite PH brief complete: `last_brief_completed_at`, `briefs_completed_total`.

### PostHog timeline (2026-09-12 UTC) — abbreviated
1. anon: `app_installed` → `app_opened` → `push_permission_granted` → `sign_in_started` → `deep_link_opened`
2. **identify to `209480`:** `sign_in_completed`, `register`, `onboarding_completed`, `brief_page_opened`, walkthrough×4
3. `brief_opened` → `card_viewed`×8 → **`brief_completed`** (06:23:41Z)

### Customer.io activity (~30d logs)
**Present:** brief_opened, brief_page_opened, card_viewed, explore_viewed, onboarding_completed, walkthrough, watchlist_viewed  

**Absent (critical):** brief_completed, sign_in_completed, signin_completed, register  

### Verdict
Same id stitched. Mid-funnel tracks to CIO. **Terminal auth + brief_completed tracks do not.** Looks like **selective fan-out / track drop** (or attrs-without-event for auth), **not** “wrong profile.”

---

## 5. Cohort results (must cite)

### brief_completed (n=25, PH last 30d with email → CIO lookup)
- **Parity:** 22/25 = **88%** have CIO `brief_completed`
- **Gap:** **12% (3/25)**
  - no CIO profile: pabandeepswain@zohomail.in
  - profile, **no event, no attr:** **lalitarorac9@gmail.com**
  - profile, **attr without event:** nehalk482@gmail.com (`last_brief_completed_at` set, 0 tracks)

### sign_in_completed (n=15)
- **Gap:** **6.7% (1/15)** — only missing profile in sample
- **Caveat:** Exhibit A is **outside** this top-15 window and **still** misses `sign_in_completed` on CIO → sample **understates** intermittent auth drops

### Workspace signal
CIO logs for `brief_completed` show many **anonymous UUID** customer ids → events often fire **before identify**.

---

## 6. Full taxonomy gaps (all 66 — event level)

See `event-level-ph-cio-gaps.md` for the full table. Highlights:

**Dead / absent both (expected CIO):**
- `interest_captured`, `push_delivered`, `profile_name_updated`
- `push_opened` ~0 both

**PH>0, CIO daily≈0 (expected both):**  
`app_updated`, `notification_settings_changed`, `story_unsaved`, `watchlist_entity_removed`, `account_deleted`

**Sheet vs reality:**  
`app_opened` marked PH-only on sheet but **does** hit CIO (CIO_UNEXPECTED) — destinations matrix is stale.

**PH dead (various):** decode, force_update_shown, brief_fallback_shown, card_rated, rating_prompt_shown, locked_feature_tapped, watchlist_limit_hit, Application Foregrounded/Installed, etc.

**Important:** Event-level “live” for `brief_completed` / `sign_in_completed` (PH volume + CIO daily_count > 0) **does not contradict** per-user gaps — same lesson as Aug 29 aggregate audit.

---

## 7. Likely root causes (evidence-ranked)

1. **Selective destination fan-out:** Mid events track to CIO; some terminal events drop for a minority (Exhibit A after identify).
2. **Identify timing:** Pre-identify `brief_completed` on anon UUID CIO profiles; may orphan or fail to merge onto email profile.
3. **setPersonProperties / identify without track:** Auth attrs / `last_brief_completed_at` without corresponding events (nehalk; Exhibit A auth attrs).
4. **Not naming alone** for Exhibit A (`signin` vs `sign_in` both absent).
5. **Taxonomy destinations outdated** vs real CIO fan-out.

---

## 8. Recommended engineering tickets (P0 first)

| P | Ticket |
|---|--------|
| P0 | Guarantee `brief_completed` **track** to CIO **after** identify; backfill users with PH event missing CIO |
| P0 | Guarantee `sign_in_completed` + `register` **tracks** (not only person attrs) |
| P0 | Identify order: do not leave journey-critical events on anon id without merge to known id |
| P1 | Fix attr-without-event path for brief |
| P1 | Implement or delete dead: interest_captured, push_delivered, profile_name_updated, push_opened |
| P2 | Update App sheet destinations to match reality |
| P2 | Standing weekly N-user PH→CIO assert for brief + sign_in (+ expand to all CIO-expected events) |

Owners to loop: **Ritvik** (App), **Animesh** (CIO / lifecycle), Ranjith (PM lock).

**Standing rule:** Never Slack/email externally without Ranjith double-approving the exact draft.

---

## 9. Parallel epic (do not mix into Fixing Events unless asked)

**Singular → PostHog attribution + in-app `source_screen`**
- Plan: `singular-posthog-attribution-plan.md` (§10 = previous-screen contract)
- Open: `open_source` on `app_opened`; nav stamps `source_screen` as previous; event name = current
- Separate from CIO parity

---

## 10. What Claude should do next (default task list)

Unless Ranjith says otherwise:

1. **Confirm understanding** in your own words (problem ≠ Singular).
2. **Propose a Fixing Events PRD / ticket pack** with acceptance tests:
   - For user U with PH `brief_completed` after identify, CIO profile for same id/email must show `brief_completed` within T minutes.
   - Same for `sign_in_completed` and `register`.
   - QA matrix: pre-identify vs post-identify brief complete; attr-only path forbidden.
3. **Optional expand audit:** per-user cohort for **every** App event with `customerio` in destinations (~23 events), same method as brief/sign_in.
4. **Do not** claim the Aug 29 audit already solved this; explain methodology gap.
5. **Do not** invent CIO 30d volumes — API gave daily_count / per-profile logs only in this audit.
6. If drafting Slack to Ritvik/Animesh: prepare exact draft for Ranjith double approval; do not send.

---

## 11. Copy-paste “problem statement” for tickets

**Title:** App PH→CIO selective track drop for `brief_completed` / `sign_in_completed` / `register`

**Problem:**  
Customer.io automations that key off brief completion and sign-in miss a non-trivial minority of users who clearly completed those actions in PostHog. Confirmed on `lalitarorac9@gmail.com` (shared id `209480`): mid-funnel events present on CIO; terminal events absent. Cohort gap for `brief_completed` ≈ 12% (3/25). Additional failure modes: CIO person attributes updated without track events; many `brief_completed` CIO log hits on anonymous UUID customers (pre-identify).

**Success:**  
100% of sampled users with PH `brief_completed` / `sign_in_completed` after identify show the same named events on the CIO profile within SLA; no attr-only completion; identify merge covers pre-identify tracks; dead events either implemented or removed from taxonomy.

---

## 12. Honest scope disclaimer (always include)

This pack’s **deep per-user journey parity** was executed for **`brief_completed` and `sign_in_completed` (+ Exhibit A full journey)**.  
The **entire 66-event App list** was audited at **event-level PH vs CIO presence/volume**.  
Expanding journey cohorts to all CIO-expected events is the natural next audit step.

---

*End of Claude instructions. Prefer reading sibling files in this folder for raw evidence rather than re-querying unless verifying live.*
