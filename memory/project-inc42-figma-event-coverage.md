---
name: project-inc42-figma-event-coverage
description: "Event coverage audit of the Figma 'SCREENS — SETTLED' section vs live app events — 12 Sep 2026; 23 gaps, 12-event generalised fix, nav IA discrepancy"
metadata:
  type: project
---

Audited Figma file `vKuPUMuhLos0rC1AFR5cWq` section `5653:12414` ("02 · SCREENS — SETTLED", 48 top-level
frames) against the live event inventory (PostHog 146258, 30d to 12 Sep 2026: **48 custom events + 4 SDK
autocapture**). Written to `~/ClaudeDocs/inc42/app-event-coverage-vs-figma-settled.md`. Unreviewed by Ranjith.

**Open discrepancy to resolve:** the Figma nav bar is **Brief / Article / Company** — not the
Brief/Explore/Watchlist 3-tab nav recorded in [[project-inc42-app-structure]]. Every `source` /
`referrer_screen` enum depends on which is current. Ask before treating either as settled.

**P0 surfaces drawn in Figma with ZERO events:** Stock Watch (top gainers/losers/recently listed on the
Company hub) · Company Directory + filter drawer + sort (the 70,412-company screen — no event fires on
applying a filter, and which filter is never recorded) · the 3-tab nav itself · sector story rail with
unread/seen/new ring states · Rewards on My Streak · `push_opened` (still absent).

**Enum limits found live:** `explore_viewed.sub_tab` only `articles`/`companies` (design has six sub-navs,
up to 7 tabs each) · `card_viewed.card_type` only `story` · `profile_section_viewed.section` missing
overview/investments/acquisitions · `watchlist_viewed.entity_tab` **null on 72%** and says `industry` where
`watchlist_entity_added` says `sector` · `search_initiated.surface` only `explore` ·
`notification_settings_changed.setting` missing master toggle + delivery_time ·
`brief_page_opened.is_edition_switch` **null on 91%** so the week-tab switcher is unanalysable ·
no `theme` property anywhere so the dark-theme designs are unmeasurable.
Fully covered, unusually: the **app-update sheet** (shown/dismissed/cta_tapped/flow_started/app_updated).

**Recommended fix is generalisation, not multiplication:** 23 gaps → **12 new events** —
`screen_viewed` (+`referrer_*`), `screen_refreshed`, `tab_changed`, `drawer_opened`/`_dismissed`,
`filter_changed`, `sort_changed`, `item_expanded`, `list_opened`, `entity_shared` (retires `story_shared`),
`rating_prompt_shown`/`_actioned`, `stock_row_tapped` — plus `theme`/`auth_state` super properties.
Bespoke per-surface events would need ~35 names. Ranjith also asked for screen-state/refresh events as a
separate list: `screen_refreshed`, `empty_state_shown`, `content_load_failed`, `retry_tapped`,
`network_state_changed`; explicitly do NOT build `session_end` ($session_id is 100% covered).

See [[project-inc42-attribution-layers]], [[project-inc42-app-ia-news-companies]], [[project-inc42-app-structure]],
[[project-inc42-app-event-validation]], [[reference-figma-mcp-limits]].
