---
name: project-inc42-article-company-events-15sep
description: "Final Article/Company page event list agreed with Ranjith 15 Sep 2026: section_viewed + section_page_viewed shared, previous_screen + entry_point instead of source; Test sheet tab"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2624b566-f568-4d3f-a505-a606cd79797b
  modified: 2026-09-15T07:51:32.954Z
---

Agreed 15 Sep 2026 after several naming rounds. Lives in the "Test" spreadsheet, tab
**"App Events - Article & Company (15 Sep)"** (gid 342970239), 63 rows: events, property groups,
previous_screen rules, values.

- Both pages share `section_viewed` (scroll block on home; entry_point scroll | top_bar) and
  `section_page_viewed` (entry_point view_all | top_bar | tag, previous_screen, previous_section).
- Browse all 70,000+ = `company_browse_viewed`. Home pages: `article_home_viewed`, `company_home_viewed`.
- Card taps are NOT new click events: extend `article_opened` / `company_profile_viewed` with
  previous_screen + section_name (+ position on company).
- `card_viewed` gets `card_location` (brief | article_story), because `card_type` already means
  editorial/signal/recap in App - Events.
- Never use `source` on new events: it already mixes channel and screen in App - Events.
  Use `previous_screen` (only on events where a new screen opens) + `entry_point` (what was tapped).
- Rejected names: "list" (home is also a list), category_viewed alongside section_viewed (confusing).

**Why:** Ranjith found the long 13 Sep plan confusing; he wants only his pointers, crisp names,
properties on the same row, and gaps flagged, not new concepts.

**How to apply:** start from this tab for any app event work on these pages. Open Figma gaps:
no View all on Article sections, no Article section page frame, Company v1 vs v2, Company top
bar tags undesigned. Related: [[project-inc42-figma-event-coverage]].
