---
name: project-inc42-user-properties-audit
description: "4 Sep 2026 audit of user properties in PostHog + Customer.io vs Ranjith's Unified User Properties sheet — 95 gaps found, written to a new tab"
metadata: 
  node_type: memory
  type: project
  originSessionId: 10a33d1d-d7ff-46ee-ad5f-22b5e353d928
  modified: 2026-09-03T19:35:27.107Z
---

Ranjith's "Unified User Properties" tab (gid 350143376) in the "One Inc42 - Analytics | Master Sheet"
has 82 rows. Audited 4 Sep 2026 against live PostHog person-property definitions and Customer.io
Data index > Profile Attributes.

**Deliverable shape matters**: Ranjith rejected a missing-only list — he could not relate to it. He wants
the FULL inventory of every live property with a Mentioned / NOT MENTIONED column he can filter and act on.
Delivered as tab "User Property Inventory (4 Sep)" (gid 440748180), 307 rows x 10 cols, with conditional
formatting on the STATUS column (NOT MENTIONED = light red 3, MENTIONED = light green 3) and a
"Covered by sheet row" column pointing back to his row numbers. Nothing existing was edited.

Verified counts: 202 live properties (excl. system/SDK) = 108 MENTIONED + 94 NOT MENTIONED.
By product: Media 109 live (55 mentioned / 54 not) - DataLabs 69 (50/19) - App 24 (3/21).
Plus 62 system/SDK rows marked "SYSTEM - ignore", 13 sheet rows "NOT FOUND LIVE", 3 "EXISTS AS SDK PROPERTY".
(An earlier pass said 95 not-mentioned; the correct figure is 94 - newsletter_source IS covered by sheet row 69.)

Source inventory counts (dated snapshot, 4 Sep 2026):
- PostHog person properties: Media (53557) 93 non-$ · DataLabs (66351) 74 · App (146258) 19 + utm_*
- Customer.io profile attributes: Inc42/Media ws 208301 = 119 · Datalabs ws 208719 = 66 · Inc42 App ws 224949 = 27

Customer.io workspace IDs (account "Inc42 Media"): **Inc42 = 208301 (this is Media)**, Datalabs = 208719,
Inc42 App = 224949. Also present: D2CX Foundations, Inc42 Stage, Sample Workspace. There is no fourth
in-scope workspace — the three map 1:1 to the sheet's three columns.

Headline findings:
- **App is the biggest hole.** The sheet has ONE catch-all row ("App canonical slugs") and zero
  App-native properties. All 21 App properties are missing: streak_*, briefs_completed_total,
  watchlist_count, tracked_sector_count, install_date, push_opt_in, push_types_enabled, dnd,
  auth_method, role, sector_groups, topic_groups, walkthrough_status, last_brief_*, is_registered,
  interest_features, registration_date.
- **`dnd` is compliance-relevant** and missing. VERIFIED 4 Sep in PostHog 146258: only **6 people** have
  dnd=true (721 false, 355 unset). Customer.io's "Profiles" percentage is COVERAGE (attribute is set to
  anything), NOT a true-rate - never read a boolean's CIO percentage as a true count.
- **Live deletion-suppression bug**: `account_deleted` fired 20x across 18 people (14 Jul - 1 Sep 2026).
  5 signed back in (dnd=false, correct). Of the 13 who did NOT, only 6 have dnd=true - **7 have no flag
  written at all**, so Customer.io is not suppressing them. Separate P0 from the property audit.
- **Pro billing envelope slug mismatch**: live PostHog+CIO use `pro_trial_start_at`,
  `pro_next_charge_at`, `pro_mandate_status`, `pro_subscription_status`, `pro_lifecycle_stage`,
  `pro_renewal_count`, `pro_current_period_end_at`, `pro_first_paid_at`, `pro_next_charge_amount`,
  `products_held` — on BOTH Media and DataLabs. The sheet's rows 17-21 target different names
  (`pro_membership_start_date` etc.). Must be reconciled before build.
- **A whole CRM enrichment layer exists only in Customer.io Media** and is invisible to the sheet:
  engagement_score/tier, paid_score, nonpaid_score, is_investor, net_ltv_inr, crm_reach_tier,
  membership_orders_count, paid_events_count, company_funding_usd/employees/founded_year/revenue_fy/
  revenue_inr/stage. Several sit at 98% profile coverage = bulk import.
- **`streak_total` is live but undocumented** — not in the App property dictionary, alongside
  streak_current/max.
- **Duplicate physical keys** for one concept (Title Case + snake_case co-existing): 17 on Media,
  1 on DataLabs. e.g. `Email`/`email`, `First Name`/`first_name`, `Event Type`/`Event_Type`/`Event_type`,
  `Plus Subscription ID`/`Plus_Subscription_ID`. The sheet lists each concept once so the dedupe is invisible.
- **The 13 `datalabs_popup_*` flags** described in [[project-inc42-knowledge-repo]]'s property dictionary
  do NOT exist as Customer.io attributes — corrected.

Excluded as system/SDK, listed separately at the bottom of the tab, not counted as gaps: PostHog
$-prefixed autocapture (~120/project), ad-click params (gclid/fbclid/msclkid/twclid/wbraid/li_fat_id/
mc_cid/ph_keyword/utm_*), is_superuser/is_staff, Customer.io reserved (cio_id, cio_iso_*, cio_latitude,
_created_in_customerio_at, unsubscribed, id) and cio_subscription_preferences + topics.topic_1..6.

Open decision: `cio_subscription_preferences` (Customer.io's native subscription centre, 39-46% coverage
on Media) vs the sheet's rows 59-70 which model each newsletter as its own slug. Only one should be canonical.

**Live collaborator warning (4 Sep)**: while this work was in progress another editor was active in the
same spreadsheet - they added a tab "Event Audit (4 Sep)", their green cursor appeared inside my tab, and
5 rows of my pasted block were deleted mid-session. Ranjith's own tabs were never touched (re-verified
83 rows x 7 cols). Always re-verify his tab integrity via gviz CSV after any editing session on this file.

Method note: Google Sheets tab contents are readable without OAuth via
`https://docs.google.com/spreadsheets/d/<id>/gviz/tq?tqx=out:csv&gid=<gid>` fetched from an
authenticated browser tab. Writing back: create tab via the "Add Sheet" button (use element refs, not
pixel coordinates — this Sheets tab has a ~0.86 screenshot-to-viewport scale offset that makes
coordinate clicks land on the wrong cell), then pbcopy a TSV and Cmd+V at A1.

See [[feedback-analytics-destination-scope]], [[reference-inc42-posthog-projects]],
[[reference-inc42-vendor-stack]].
