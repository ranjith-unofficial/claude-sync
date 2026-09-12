# PER-USER JOURNEY AUDIT REPORT — Inc42 App (PostHog ↔ Customer.io)

**Owner:** Ranjith (PM)  
**Audited:** 2026-09-12 17:19 IST  
**Scope:** Entire App taxonomy (`App.csv`, 66 events) + cohort journey parity + Exhibit A  
**Systems:** PostHog `Inc42 App` project `146258` · Customer.io workspace `Inc42 App` `224949`

---

## 1. Executive summary (gaps only — blunt)

1. **Exhibit A confirmed:** `lalitarorac9@gmail.com` has PH `brief_completed` + `sign_in_completed` (and `register`) after identify on id `209480`. Matching CIO profile exists, but **those three events are missing** from CIO activity. Mid-funnel events (`brief_opened`, `card_viewed`, …) **are** present.
2. **brief_completed cohort gap rate = 12%** (3/25): no CIO profile (1) + profile without event (2). One of the two (nehalk) has **person attributes updated without the event**.
3. **sign_in_completed cohort gap rate = 6.7%** (1/15) — only a missing profile in the top-15 sample; **but Exhibit A proves auth events can still drop** outside that sample.
4. **Hard-dead both systems (expected CIO):** `interest_captured`, `push_delivered`, `profile_name_updated` — still absent (matches Aug 29). `push_opened` also 0/0.
5. **PH>0 but CIO daily≈0 (expected both):** `app_updated`, `notification_settings_changed`, `story_unsaved`, `watchlist_entity_removed`, `account_deleted` (low PH volume).
6. **Root cause is not “wrong workspace”:** App PH + App CIO are correct. Failure modes are **selective fan-out**, **pre-identify anon events**, and **attribute-without-track**.

---

## 2. Exhibit A — lalitarorac9@gmail.com

| Check | PostHog | Customer.io |
|-------|---------|-------------|
| Profile found | YES | YES (`209480` / `b5dd0d00d812d912`) |
| `brief_completed` | **YES** (1× @ 06:23:41Z) | **NO** |
| `sign_in_completed` | **YES** (1× @ 06:22:30Z) | **NO** |
| `register` | YES | NO |
| Mid brief funnel | YES | YES (`brief_opened`, `card_viewed`, …) |

Full write-up: [`journey-lalitarorac9.md`](./journey-lalitarorac9.md)

---

## 3. Cohort gap rates

| Journey event | Sample | Gap (PH yes → CIO event no / no profile) | Notes |
|---------------|--------|------------------------------------------|-------|
| `brief_completed` | 25 | **12% (3/25)** | 1 no profile; 2 no event (1 attr-only) |
| `sign_in_completed` | 15 | **6.7% (1/15)** | 1 no profile; 0/14 event miss in sample |

Details: [`cohort-parity-brief-signin.md`](./cohort-parity-brief-signin.md)

---

## 4. Full event gap table

See [`event-level-ph-cio-gaps.md`](./event-level-ph-cio-gaps.md) and matrix [`app-event-destination-matrix.csv`](./app-event-destination-matrix.csv).

### Top gaps (actionable)

| # | Gap | Evidence |
|---|-----|----------|
| 1 | Per-user miss of `brief_completed` on CIO | Exhibit A + 12% cohort |
| 2 | Per-user miss of `sign_in_completed` / `register` on CIO | Exhibit A (attrs imply auth; events absent) |
| 3 | `interest_captured` / `push_delivered` / `profile_name_updated` absent both | PH 0 + CIO never |
| 4 | Attr-without-event (`last_brief_completed_at` set, no track) | nehalk482 |
| 5 | Pre-identify `brief_completed` landing on anon CIO ids | workspace logs `filter_matches` UUIDs |

---

## 5. Likely root causes

1. **Destination fan-out / selective track:** Mid-funnel tracks to CIO; some terminal events drop for a minority of users (lalit after identify).
2. **Identity timing:** Many CIO `brief_completed` log matches are **anonymous UUIDs** — event before `identify` → wrong/anon profile or orphaned activity.
3. **Identify / setPersonProperties without track:** nehalk has `last_brief_completed_at` but 0 `brief_completed` events — Aug 29 already flagged missing setPersonProperties; inverse also happens.
4. **Naming:** Slack `signin_completed` vs `sign_in_completed` — checked both on Exhibit A; **not** the cause there.
5. **Sheet destinations incomplete:** Events marked PH-only (e.g. `app_opened`) still hit CIO at volume.

---

## 6. Recommended Fixing Events tickets

| Priority | Ticket | Owner hint |
|----------|--------|------------|
| P0 | Guarantee `brief_completed` track to CIO **after** identify; replay/backfill for users with PH event missing CIO | App SDK + Animesh |
| P0 | Guarantee `sign_in_completed` + `register` track (not only person attrs) | Auth / App SDK |
| P0 | Fix identify order: never fire journey-critical events on anon id without merge | App SDK |
| P1 | Resolve attr-without-event path (setPersonProperties vs track) for brief | App SDK |
| P1 | Implement or delete dead events: `interest_captured`, `push_delivered`, `profile_name_updated`, `push_opened` | Product + Eng |
| P2 | Update App sheet destinations to match real CIO fan-out | Taxonomy |
| P2 | Standing audit: weekly N-user PH→CIO event assert for brief + sign_in | Data / PM |

---

## 7. Limitations

- CIO activity logs ~**30 days**, 50/page; no lifetime.
- CIO volume via GET is **`daily_count` only** — not comparable 1:1 to PH 30d counts.
- No `cio` CLI in box; cohort fan-out via MCP (25+15 emails maximized).
- Initial MCP context was Media PH `53557` — **switched** to App `146258` (documented).
- Could not POST CIO profile_count/usage (read-only GET posture).
- Numbers are live pulls; do not invent missing CIO 30d aggregates.

---

## 8. Artifact index

| File | Purpose |
|------|---------|
| `START-HERE.md` | Pack entry + pointer |
| `app-event-destination-matrix.csv` | Phase 1 taxonomy matrix |
| `journey-lalitarorac9.md` | Exhibit A |
| `cohort-parity-brief-signin.md` | Phase 3 gap rates |
| `event-level-ph-cio-gaps.md` | Phase 4 full table |
| `PER-USER-JOURNEY-AUDIT-REPORT.md` | This master report |
