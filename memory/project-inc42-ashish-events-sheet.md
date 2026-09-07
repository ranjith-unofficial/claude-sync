---
name: project-inc42-ashish-events-sheet
description: "Ashish's 19-column event QA/test format, and the 158-row single-tab events sheet built for it on 8 Sep 2026 in the Analytics Master Sheet"
metadata:
  type: project
---

**Ashish's format** is a 19-column event-testing layout. Two tabs were added to
"One Inc42 - Analytics | Master Sheet" (`1n6r5QXe-9Pq1uAWMKRe7zSgLHSejASzAq-BAqeI3L6Y`) on **8 Sep 2026**:
`Ashish - Events (All Properties)` (158 rows: 46 inc42 / 47 datalabs / 65 app) and
`Ashish - Property Groups` (20 group definitions). Durable copy:
`~/ClaudeDocs/inc42/events-audit-ashish-format-8sep.csv`. Counterpart file from 7 Sep for user properties:
`~/ClaudeDocs/inc42/user-properties-audit-ashish-format-7sep.csv`.

**The two property columns are NOT redundant — this was explicitly questioned and settled:**
- `event_property_groups` names standing bundles only (page, user, super, story, interaction…).
- `custom_event_properties` lists ONLY that event's unique properties, typed: `name:string:required`,
  `name:string:enum[a|b|c]`. Ashish leaves it blank where an event has none — that is design, not omission.
- **Why it matters:** nearly every known bug lives in an event-unique property (`story_shared.channel` wrong,
  `search_result_tapped.entity_or_story_id` returns a slug, `brief_page_opened.source` wrong,
  `Table Sort Orderby` misnamed, `pro_billing.billing_stage` the only success/failure discriminator).
  Group names alone make all of them invisible — the tester sees the event arrive and marks it green.

**`event_name` = planned/spec name; `display_name` = the exact live string to search for in PostHog.**
15 of 158 rows carry real drift (e.g. `card_rated`→`brief_story_rated`, `Report View`→`Report Interaction`,
`Registered`→`user_registered`, `Customise`→`Customize Columns Applied`, `Pageview`→`$pageview`).

**Ranjith's decisions for this deliverable (8 Sep):** everything real (~160 rows), junk dropped and
planned/live duplicate pairs merged; `audit_status`/`audit_date`/`audit_notes` left BLANK for Ashish to fill,
with all known findings pushed into `test_notes`; destinations = real only (`posthog | customerio`, plus
`firebase | singular` on App) — Mixpanel, MoEngage and Amplitude dropped entirely, GA4-only misrouting noted
in test_notes instead. NOTE the 7-Sep user-properties file did the opposite and pre-filled the audit columns.

**Where the property groups actually live in the master sheet** (needed to fill the groups column):
- `Inc42 - Media - Events Properties` — 5 side-by-side blocks. "Property Group 1" = content,
  "Property Group 2" = page/session, plus User Data Fields, Custom Properties, Plus Properties. The Events
  tab references them as bare NUMBERS (`1`, `2`, `1,2`) and the numbers are never named in words anywhere.
- `Datalabs - Events Properties` — named `Property Group` column, but **130 of 163 rows are hidden** and the
  tab renders as one row plus a black bar. Do NOT unhide (see [[feedback-shared-system-safety]]); rebuild
  from `~/ClaudeDocs/inc42/datalabs-event-properties-full.csv`. Its "Colour Code" and "ABCDEFG" groups are
  legend artefacts, not real groups — an earlier tool scraped them in as 5 fake event rows.
- `App - Event Properties` — named groups: Super (11, on every event), Story (11), Person (23, identify-only).

Related: [[project-inc42-event-audit-4sep]], [[project-inc42-user-properties-audit]],
[[feedback-sheets-clipboard-paste-safety]], [[reference-inc42-vendor-stack]].
