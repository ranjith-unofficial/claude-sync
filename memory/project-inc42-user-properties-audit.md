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

FINAL verified counts (after the full-census rebuild): 204 live properties = 108 MENTIONED + **96 NOT MENTIONED**.
By product: Media 109 live (55/54) - DataLabs 69 (50/19) - App 26 (3/23).
Plus 90 system/SDK rows, 13 "NOT FOUND LIVE", 3 "EXISTS AS SDK PROPERTY". Tab is 338 rows x 14 cols.
Columns L/M/N carry PostHog live key counts, null/blank counts and blank %.

**METHOD CORRECTION - load-bearing.** PostHog's `read-data-schema entity_properties person` (the property
DEFINITIONS / taxonomy list) is INCOMPLETE and must not be used as the inventory source. It silently omitted
6 App properties. Use a full key census instead:
`SELECT arrayJoin(JSONExtractKeys(properties)) AS prop, count() FROM persons GROUP BY prop`
and for blank detection:
`countIf(JSONExtractRaw(properties,k)='null' OR JSONExtractRaw(properties,k)='""')`.
Note `properties.X` returns NULL when the key exists with a JSON-null value, so isNotNull() UNDERCOUNTS;
JSONHas/JSONExtractRaw is the reliable test. Also: arrayJoin+count() without a proper null filter returns
the TOTAL person count for every property - a wrong-number trap that bit this session twice.
When aggregating by normalised slug, SUM across Title-Case and lowercase duplicates or counts mismatch.

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
- **App attribution is silently dead.** `attribution_source` and `attribution_campaign` are written on
  1,037 of 1,089 App persons (95%) with a literal JSON `null` value on EVERY one. Neither is in Ranjith's
  sheet, neither is in Customer.io, and neither appeared in the PostHog taxonomy list. Singular install
  attribution is not landing, so campaign-cohort retention cannot be measured. Ties to
  [[project-inc42-app-acquisition]].
- **4 App properties were wrongly labelled Customer.io-only** in the first pass: `sector_groups`,
  `topic_groups` (866 people each), `push_types_enabled` (27), `interest_features` (17) ARE in PostHog.
- **Blank-value rates (PostHog, key present but value null/empty)** - the user-property equivalent of the
  event audit's "properties are blank" bucket:
  Media `Designation` 75% blank (77,266 of 102,926), `Seniority` 64% (59,502 of 93,472), `Phone Number` 59%,
  `Company Website` 46%, `City` 83%, `Company Name` 30%.
  DataLabs `Linkedin` 80% blank (14,627 of 18,316), `Designation` 90%, `Plus Membership Expiry Date` 87%,
  `Full Name` 59%, `DL Use Case` 28%, `Industry` 20%, `Seniority` 18%.
  App: clean apart from the two attribution fields.
  IMPLICATION: the sheet's own volume figures (e.g. row 10 seniority "89354") appear to count KEYS, not
  non-blank values. Real Media seniority coverage is ~34k, not ~89k.
- **`Plus Meter Views Left` is on 1,241,894 Media persons** - the highest-coverage Media property, and
  sheet row 32 marks it Delete. Flag before anyone acts on that row.
- **Media lowercase duplicate slugs are near-empty** (work_email, personal_email, first_name, seniority,
  uid, register_source, phone_number etc. all 1-3 people), so that dedupe is trivial, not a migration.
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

**MASTER tab (5 Sep 2026)** — Ranjith asked for the two tabs merged into one, because maintaining two
will break. Delivered as tab **"MASTER - User Properties"** (gid 1805026241), 219 rows x 14 cols, one row
per canonical property, sorted into 3 sections: "1. NEEDS A FIX OR A DECISION" (104), "2. KEEP AS IS",
"3. NONE - SDK AND VENDOR PLUMBING". Single ACTION column, vocabulary Ranjith specified: nothing to do =
**None**, delete = **Delete**, unsure = **Not sure**, plus his existing Fix/Merge/Keep/Drop/Already added
and a new **Add**. Counts: Keep 49, None 47, Add 44, Delete 20, Not sure 20, Fix 12, Merge 7, Already added 5,
Drop 1 = 205 properties. Column E ("Where this row came from") distinguishes "Your sheet row N" (his
decision, copied verbatim) from "Newly found by audit" (my PROPOSAL, not a decision). Conditional format:
"Not sure" = light yellow 3 on C1:C240.

Merge rule that matters: a row like "LinkedIn URL into linkedin_profile_url" claims only the SOURCE name;
the target keeps its own row. Getting this wrong made row 27 swallow row 50's live data.

**SHEETS SAFETY — near-miss on 5 Sep.** Clicking the "Add Sheet" button via element ref SILENTLY FAILED,
focus stayed on Ranjith's "Unified User Properties" tab, and a 230-row paste overwrote his rows 27-256.
Recovered with a single Cmd+Z and proved clean by SHA-256 against a copy taken before the edit
(02b1be5adb1b6f3031cab119cb1d25cbd8e63ca2051323ca17f7f499718a6f86).
RULES going forward on this file:
1. Before ANY paste, snapshot the target tab's CSV locally and hash it.
2. After creating a tab, SCREENSHOT and confirm the gid changed, the grid is empty and the tab name is
   "SheetNN" BEFORE pasting. Never chain create+paste in one browser_batch.
3. Prefer Insert > Sheet over the "+" Add Sheet button; the ref click on "+" is unreliable.
4. `navigator.clipboard.writeText` needs the page focused (click the grid first), and it OVERWRITES the
   clipboard — always re-run pbcopy and diff against the source file immediately before pasting.

Method note: Google Sheets tab contents are readable without OAuth via
`https://docs.google.com/spreadsheets/d/<id>/gviz/tq?tqx=out:csv&gid=<gid>` fetched from an
authenticated browser tab. Writing back: create tab via the "Add Sheet" button (use element refs, not
pixel coordinates — this Sheets tab has a ~0.86 screenshot-to-viewport scale offset that makes
coordinate clicks land on the wrong cell), then pbcopy a TSV and Cmd+V at A1.

See [[feedback-analytics-destination-scope]], [[reference-inc42-posthog-projects]],
[[reference-inc42-vendor-stack]].

**REWRITE FOR IMPLEMENTERS (8 Sep 2026).** Ranjith could not act on column G ("What to do") of the
"Unified User Properties" tab (gid 350143376) — G7 `user_id` was the trigger. Rewrote in the SAME tab:
**G = "Where to change it", H = "What exactly to do", I = "Done when"**, all 82 property rows, plain
language, no jargon. Columns A–F were NOT touched and were proven byte-identical to a pre-paste snapshot
(83 rows compared cell-by-cell in-page, zero differences); backup at
`unified_BACKUP_before.csv`, SHA-256 e3c5dadd2a0fdfc775758f62d6924e9f72fc5322a1794e862962666c044b71b0.
Old G text is gone — recoverable only from Google version history.

Contradictions surfaced as "DECISION NEEDED" in column H, still unresolved:
row 2 `trial_start_date/trial_end_date` (C says Delete, DataLabs says Keep with 2,539 PH / 1,934 CIO live),
row 4 `datalabs_onboarding_complete` (C says Delete, DataLabs cell says Fix),
row 34 `Username` (delete only if no live DataLabs screen reads it).
Also flagged and NOT fixed: E7 text is truncated (" values (79659). Write slug."), D22/E22 start with a
stray ".", column B mixes priorities P1/P2/P3 with the status "Already fixed", and the 9 seniority levels /
company valuation ladder / 17 dl_use_case values / allowed `interests` values are referenced but written
down nowhere.

**GOOGLE SHEETS GOTCHA (new):** a pasted cell whose text STARTS with an apostrophe loses it — Sheets eats
the leading `'` as its force-text prefix. Two cells lost it silently; caught only by comparing total
character counts of the pasted range against the source. Always compare per-row lengths after a paste,
and never start a cell with `'`.

**Second pass, same day:** rewriting only G/H/I was NOT enough — Ranjith came back pointing at D7
("Fix. Auth string (15190), not numeric PK.") saying he could not understand it either. The per-product
columns **D (Media), E (DataLabs), F (App)** were also rewritten in plain language, 82 rows, keeping every
count. Format per cell: state what is stored TODAY and how many people, prefixed BROKEN / MISSING /
"In use:" / "Not used on <product>", and for the App column what the App must write. Columns A, B, C and
G, H, I were proven unchanged by the D/E/F paste. **Lesson: when he says an action column is unreadable,
the evidence columns beside it are unreadable too — rewrite the whole row, not the one cell he quoted.**
