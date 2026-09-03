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
Data index > Profile Attributes. **95 properties exist live but are absent from that tab**:
Media 55, DataLabs 19, App 21. Written to a NEW tab "Missing User Properties (4 Sep)"
(gid 440748180), 133 rows x 8 cols. Nothing existing was edited.

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
- **`dnd` is compliance-relevant** and missing — true while a deletion request is pending, suppresses
  ALL Customer.io sends.
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

Method note: Google Sheets tab contents are readable without OAuth via
`https://docs.google.com/spreadsheets/d/<id>/gviz/tq?tqx=out:csv&gid=<gid>` fetched from an
authenticated browser tab. Writing back: create tab via the "Add Sheet" button (use element refs, not
pixel coordinates — this Sheets tab has a ~0.86 screenshot-to-viewport scale offset that makes
coordinate clicks land on the wrong cell), then pbcopy a TSV and Cmd+V at A1.

See [[feedback-analytics-destination-scope]], [[reference-inc42-posthog-projects]],
[[reference-inc42-vendor-stack]].
