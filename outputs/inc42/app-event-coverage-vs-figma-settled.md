# App event coverage vs Figma "02 · SCREENS — SETTLED"

**Owner:** Ranjith M · **Date:** 12 September 2026 · **Status:** audit, decisions open
**Design source:** `Inc42-App-2026` file `vKuPUMuhLos0rC1AFR5cWq`, section `5653:12414` — "02 · SCREENS — SETTLED" (48 top-level frames, full node tree parsed)
**Event source:** PostHog project 146258, live query 12 Sep 2026, 30-day window. 48 custom events + 4 SDK autocapture events.
**Method:** every frame name in the section was extracted and matched against the live event/property inventory. Nothing here is from the tracking sheet — the sheet was not consulted, because it has been wrong before.

---

## 1. What we have — the live event inventory (30d volumes)

**Brief** · `brief_page_opened` 10,409 `{is_today, source, edition_date, is_edition_switch}` · `brief_opened` 3,128 `{edition_date, story_count, is_first_brief, source}` · `card_viewed` 16,201 `{story_id, position, card_type, is_boosted, boost_reason, +9 story meta}` · `brief_completed` 1,124 `{edition_date, duration_sec, cards_viewed}` · `brief_story_rate_opened` 27 · `brief_story_rated` 73 `{is_relevant, position, story_id, authenticated}`

**Reading** · `article_opened` 3,096 `{source, position, story_id, story_slug, +9 story meta}` · `scroll_depth` 3,970 `{depth_pct, + story meta}` · `summary_expanded` 2,289 `{surface, story_id, company_id, sector_id}` · `story_saved` 195 · `story_unsaved` 23 · `story_shared` 196 `{channel, source, story_id}`

**Explore / search** · `explore_viewed` 9,120 `{sub_tab, pill_or_slice, filters_count, filters_applied}` · `search_initiated` 404 `{search_scope, surface}` · `search_performed` 1,893 `{query, result_count, search_scope}` · `search_result_tapped` 330 `{query, position, result_type, entity_or_story_id}`

**Companies / sectors** · `company_profile_viewed` 961 `{company_id, company_name, is_tracked, source}` · `profile_section_viewed` 4,351 `{section, company_id, company_name}` · `sector_landing_viewed` 144 `{sector, sub_tab, source}`

**Watchlist** · `watchlist_viewed` 2,056 `{entity_tab, sub_tab, tracked_count}` · `watchlist_entity_added` 275 `{entity_type, entity_id, entity_name, source, watchlist_size_before}` · `watchlist_entity_removed` 33

**Streak** · `streak_opened` 364 `{source}` · `streak_milestone_viewed` 337 `{milestone, milestone_day}`

**Profile / settings** · `profile_opened` 823 `{source}` · `menu_item_tapped` 284 `{item}` · `preferences_updated` 117 `{field, new_values, new_value_count}` · `notification_settings_changed` 61 `{setting, new_value}` · `account_deleted` 6 · `signed_out` 52

**Auth / onboarding** · `onboarding` 5,171 `{status, step_number, step_name, step_answer, selection_count}` · `onboarding_completed` 1,109 `{role, topic_groups, sector_groups}` · `walkthrough` 3,718 `{step_number, step_name, status}` · `sign_in_started` 1,513 · `sign_in_completed` 2,439 `{method, is_new_account}` · `sign_in_prompt_shown` 164 `{source}` · `register` 480 `{method}`

**Lifecycle / push / update** · `app_opened` 5,733 `{source, push_type}` · `app_installed` 1,273 · `app_updated` 43 · `deep_link_opened` 1,198 `{campaign, link_url, destination_screen, source, medium, content}` · `push_permission_prompted` 1,317 / `_granted` 702 / `_denied` 617 `{context, prompt_type}` · `app_update_prompt_shown` 33 / `_dismissed` 20 / `app_update_cta_tapped` 2 / `app_update_flow_started` 2 `{mode, target_version, installed_version, prompt_count}` · `error_shown` 472 `{surface, error_type}`

**Autocapture (SDK, deduplicate later)** · `Application Opened` 5,497 · `Application Became Active` 9,229 · `Application Backgrounded` 11,257 · `$feature_flag_called` 147

**Does not exist, despite being planned:** `push_opened` — 0 events. Every "opened from a notification" number is unavailable today.

---

## 2. Screen-by-screen verdict

| Figma frame | Functionality | Verdict |
|---|---|---|
| `BRIEF PAGE · real content · v1` | brief card, story count, CTA | ✅ covered |
| " · tabs · the week (7 day tabs) | switch to another day's edition | ⚠️ `is_edition_switch` exists but **null on 91%** (9,454 of 10,439); no tab-tap event, no from/to day |
| " · "Picked for you" | personalised rail | ❌ no event |
| " · "This week so far" past editions | tap a past edition card, "All eight read" state | ❌ no card-tap event; completion state of past editions unknown |
| " · headline reel / window | animated headline impressions | ❌ no event |
| `BRIEF PAGE · dark theme · alt` | dark mode | ❌ **no `theme` property on any event** — dark vs light usage is unmeasurable |
| `NAV · floating glass bar` | **Brief / Article / Company** 3-tab nav | ❌ no `nav_tab_tapped`. Note the IA changed — nav is no longer Brief/Explore/Watchlist |
| `ARTICLE PAGE · STORY RAIL · sectors` | sector avatar rail, ring states unread/seen/new | ❌ no rail impression, no tap event, no ring-state property |
| " · `Sub-nav · revamped` (News, In-Depth, Markets, Financials, Startups, D2C, Newsletter) | 7 dev-type tabs | ❌ `explore_viewed.sub_tab` only ever holds `articles` / `companies` |
| " · sections Top Stories / In-Depth / Markets / Financials | section impressions, card taps | ⚠️ `card_viewed` + `article_opened` fire, but `card_type` is only ever `story` and there is no section identity |
| `ARTICLE READING` | back, bookmark, share, body, scroll | ✅ covered (`article_opened`, `scroll_depth`, `story_saved`, `story_shared`) |
| " · TL;DR inline block | expand summary | ✅ `summary_expanded{surface}` |
| `DRAWER · TL;DR` + save states | drawer open, save from drawer, "Read full article" | ❌ drawer is a different interaction from inline expand — no open event, no drawer-scoped save source |
| `COMPANY PAGE v1/v2` | hub screen | ⚠️ no screen-level event; `explore_viewed` is the closest and does not model this |
| " · `Sub-nav` (All, Recently funded, Just launched, Early rounds, Profitable, Unicorns, Sectors) | 7 tabs | ❌ not in any enum |
| " · `SECTION · Stock Watch` (TOP GAINERS / TOP LOSERS / RECENTLY LISTED) | stock rows, price change | ❌ **zero events** — a whole new surface is invisible |
| " · `directory strip` "Browse all 70,000+" | entry to directory | ❌ no event |
| " · `VIEW ALL …` links | section → full list | ❌ no event |
| " · company card `CHIP · RAISED/HQ/TEAM/+3` | chip taps, "+3" expand | ❌ no event |
| `COMPANY DIRECTORY · browse all` | 70,412-row browse screen | ❌ no `directory_viewed` |
| " · `filter bar` chips + `button · Filters` + count + × | apply / remove a filter | ❌ `explore_viewed` carries `filters_count` / `filters_applied` but **no event fires on the filter action, and which filter is never recorded** |
| " · `sort` (Total funding) | change sort | ❌ no event |
| " · `result line` 70,412 COMPANIES | result count after filtering | ❌ not captured on any directory event |
| `DRAWER · Filters` (6 groups, 2 toggles, Reset, Clear all, "Show 12,480") | the whole filter model | ❌ no events: no drawer open, no group interaction, no reset, no clear-all, no apply |
| `DIR CARD · collapsed vs expanded` | "view more" / "View less" | ❌ no event (`summary_expanded` is TL;DR, not this) |
| `COMPANY PROFILE` | profile screen, track, share, View more | ⚠️ `company_profile_viewed` + `watchlist_entity_added` cover view and track. **Share is story-only — no `company_shared`.** "View more" description expand not tracked |
| " · `Sub-nav` (Overview, Financials, Funding, Investments, Acquisitions) | tabs | ⚠️ `profile_section_viewed.section` holds funding / financial_overview / key_people / corporate_activity / recent_activity — **`overview`, `investments`, `acquisitions` are missing** |
| " · charts (FUNDING RAISED OVER YEARS, PROFIT & LOSS) | chart views / interactions | ❌ no event |
| `VIEW ALL · card variant` drawers (Funding rounds, Key people, Corporate activity, Recent activity + its own All/Funding/Financials tabs) | 4 drawers, one with internal tabs | ❌ no drawer-open event; the in-drawer tabs are in no enum |
| `SECTOR PAGE · Articles / Companies · v2` | sector screen, track, share, 2 tabs | ⚠️ `sector_landing_viewed{sub_tab}` covers articles/companies; **track partially** (`watchlist_entity_added.entity_type=sector`, only 5 events in 30d); **share not covered** |
| `WATCHLIST · Articles / Companies / Sectors` | 3 tabs | ⚠️ `watchlist_viewed.entity_tab` is **null on 72%** (1,473 of 2,056) and uses `industry` where `watchlist_entity_added` uses `sector` — the two events disagree |
| `MY PROFILE` × 5 states (streak running, guest no streak, streak not started, guest with streak, not onboarded) | state-dependent screen | ⚠️ `profile_opened{source}` fires; **no property distinguishes which of the 5 states was rendered** |
| " · `complete` card (1/4, "Complete setup") | profile-completion prompt | ❌ no event |
| " · streak block, "VIEW STREAK →", FAQs link | entry to streak | ✅ `streak_opened{source}` |
| " · rows Watchlist / Role / Topics / Sector | tap to edit | ⚠️ `preferences_updated` records the **save**; the row tap and drawer open are not recorded |
| " · about rows | Privacy, Terms, Contact, FAQs, Rate App, App version | ⚠️ `menu_item_tapped.item` = rate_app, faq, contact_us, terms, privacy. **`app_version` row missing** |
| " · logout / Login | sign out, guest login | ✅ `signed_out`, `sign_in_started` |
| `MY STREAK · v1` | hero, stats, badges, history, FAQs, rewards | ⚠️ `streak_opened` + `streak_milestone_viewed` only. **No stats snapshot, no badge tap, no history interaction, no FAQ expand** |
| " · `rewards` (locked marks, unlock) | rewards | ❌ **zero events** — new surface, fully invisible |
| `DRAWER · Edit role / topics / sectors` | chip select, Clear, Cancel, Save | ⚠️ save only, via `preferences_updated`. Abandonment (Cancel) and Clear are invisible |
| `DRAWER · Edit profile` (NAME, EMAIL read-only) | edit name | ❌ no event |
| `DRAWER · Streak FAQs` | FAQ open, row expand | ❌ no event |
| `DRAWER · Sign in` (Apple, Google, email, "not now") | auth entry | ⚠️ `sign_in_prompt_shown{source}` + `sign_in_started{method}` cover it. **"not now" dismissal is not recorded** |
| `PUSH NOTIFICATIONS · v1` | master toggle, Daily brief, Delivery time, Watchlist alerts | ⚠️ `notification_settings_changed.setting` = dailyBrief, watchlistAlerts. **Master toggle and Delivery time missing**; no screen-view event |
| `A · PLAY STORE` sheet ("Enjoyed today's brief?", Rate now / Maybe later, at 8 of 8) | brief-end rating prompt | ❌ no event. `menu_item_tapped.item=rate_app` is the **profile row**, not this sheet |
| `L2 · TINTED CARD` update sheet (VERSION 2.4.0 · 18 MB, Update now / Not now) | forced/soft update | ✅ **fully covered** — `app_update_prompt_shown`, `_dismissed`, `app_update_cta_tapped`, `app_update_flow_started`, `app_updated` |
| `Search field` on Brief header / Company page / Directory | search entry from new surfaces | ⚠️ `search_initiated.surface` only ever holds `explore` |

---

## 3. The gaps, ordered by what they cost

### P0 — a whole surface produces no data

| # | Surface | Why it matters |
|---|---|---|
| 1 | **Stock Watch** (gainers / losers / recently listed) | new, prominent on the Company hub, and would be the first market-data feature in the app. Zero instrumentation = no way to justify keeping it |
| 2 | **Company Directory + filter drawer + sort** | the 70,000-company promise. No event fires on applying a filter, so "which filters do people use" and "do filtered sessions convert to a profile view" are both unanswerable |
| 3 | **3-tab nav (Brief / Article / Company)** | the primary navigation of the app. Without `nav_tab_tapped` there is no tab-switch funnel, and the IA change itself cannot be evaluated |
| 4 | **Sector story rail** (ring states) | the main new discovery mechanic on the Article page. Ring state (unread/seen/new) is the whole point and is not captured |
| 5 | **Rewards** (My Streak) | net-new retention mechanic, zero events |
| 6 | **`push_opened`** | does not exist; "opened via notification" is unanswerable — this is the same gap as the attribution work |

### P1 — event exists but the enum cannot express the new UI

| # | Gap | Evidence |
|---|---|---|
| 7 | Sub-nav tabs everywhere | `explore_viewed.sub_tab` = `articles` / `companies` only; the new sub-navs have 7 tabs (Article page), 7 tabs (Company hub), 5 tabs (Company profile), 2 (Sector), 3 (Watchlist), 3 (Recent-activity drawer) |
| 8 | `card_type` | only `story`; design now has company cards, DIR cards, stock rows, sector cards, edition cards |
| 9 | `profile_section_viewed.section` | missing `overview`, `investments`, `acquisitions` |
| 10 | `watchlist_viewed.entity_tab` | **null on 72%**, and `industry` vs `watchlist_entity_added`'s `sector` — same concept, two names |
| 11 | `search_initiated.surface` | only `explore`; design adds Brief header, Company hub, Directory |
| 12 | `notification_settings_changed.setting` | missing master toggle and `delivery_time` (a value, not a boolean) |
| 13 | `company_profile_viewed.source` | holds both `companies` and `companies_directory` — pick one |
| 14 | `story_shared.source` | holds both `article` and `article_reader` — pick one |
| 15 | Share beyond stories | `story_shared` is story-only; company profile and sector page both have a share control |

### P2 — interaction patterns with no event class at all

| # | Pattern | Appears in |
|---|---|---|
| 16 | **Drawer open / dismiss** | 12+ drawers: Filters, TL;DR, Funding rounds, Key people, Corporate activity, Recent activity, Edit role/topics/sectors/profile, Streak FAQs, Sign in |
| 17 | **Expand / collapse** | DIR card view more/less, chip "+3", company "View more", FAQ rows |
| 18 | **View all** | section → list, "View all 41 investors", "View all 25 funding rounds", VIEW ALL RECENTLY FUNDED |
| 19 | **Filter / sort as actions** | directory, filter bar chips, filter drawer groups, Reset, Clear all |
| 20 | **State of the screen that was rendered** | 5 profile variants, guest vs signed-in, streak started vs not, empty watchlist |
| 21 | **Theme** | dark-theme screens exist; no `theme` property anywhere |
| 22 | **Brief-end rating sheet** | separate from the profile Rate App row |
| 23 | **Profile completion prompt** | 1/4 progress card |

---

## 4. Screen state, refresh and system events — the separate list

These are not features; they are the conditions a screen can be in. None of them are instrumented today, and every funnel silently mixes them together.

| # | Event to add | Properties | Answers |
|---|---|---|---|
| S1 | `screen_refreshed` | `screen`, `method` (`pull_to_refresh` \| `button` \| `auto`), `result` (`fresh` \| `no_change` \| `error`), `content_age_sec`, `new_item_count` | "do people pull to refresh because content is stale?" — today a refresh is indistinguishable from a screen view |
| S2 | `screen_viewed` | `screen`, `referrer_screen`, `referrer_module`, `load_ms`, `data_source` (`network` \| `cache`) | one thin universal event gives the complete nav graph — and removes the need to invent a bespoke view event for every new screen (Company hub, Directory, Sector page, My Streak all lack one today) |
| S3 | `empty_state_shown` | `screen`, `reason` (`no_saved_items` \| `no_results` \| `filters_too_narrow` \| `offline`) | empty watchlist and zero-result filters currently look like successful screen views |
| S4 | `content_load_failed` | `screen`, `error_type`, `is_retryable`, `retry_count` | `error_shown{surface, error_type}` exists (472/30d) but has no retry or retryability |
| S5 | `retry_tapped` | `screen`, `error_type`, `attempt` | whether failures are recoverable in practice |
| S6 | `network_state_changed` | `state` (`online` \| `offline`), `screen` | India-first app; offline reads are a real pattern and invisible |
| S7 | `theme_changed` + `theme` as a **super property** on every event | `theme` (`light` \| `dark` \| `system`), `source` | dark theme is designed and unmeasurable |
| S8 | `session_end` (or accept PostHog's `$session_id` + last event) | — | **not needed** — `$session_id` is on 100% of events; do not build this |

`screen_refreshed` (S1) and `screen_viewed` (S2) are the two that pay for themselves immediately: S2 alone closes gaps 3, 7, and the missing screen-view events for four new screens.

---

## 5. How to go about it — generalise, don't multiply

The 23 gaps above are **not 23 new events**. Most are the same interaction shape repeated across surfaces. Bespoke events would mean ~35 new names and a taxonomy nobody maintains.

### 5.1 Twelve new events cover everything

| # | Event | Properties | Replaces gaps |
|---|---|---|---|
| 1 | `screen_viewed` | `screen`, `referrer_screen`, `referrer_module`, `referrer_position`, `load_ms`, `data_source`, `screen_state` | 3, 20, S2 + view events for Company hub / Directory / Sector / My Streak |
| 2 | `screen_refreshed` | `screen`, `method`, `result`, `content_age_sec`, `new_item_count` | S1 |
| 3 | `tab_changed` | `surface`, `tab_group` (`primary_nav` \| `sub_nav` \| `drawer`), `from_tab`, `to_tab` | 3, 7 — all six sub-navs, the 3-tab bar, and the week tabs in one event |
| 4 | `drawer_opened` / 5 `drawer_dismissed` | `drawer`, `surface`, `entity_type`, `entity_id`; dismissal adds `method` (`cta` \| `cancel` \| `swipe` \| `backdrop`) | 16, 18 (view-all drawers), Sign-in "not now" |
| 6 | `filter_changed` | `surface`, `action` (`apply` \| `remove` \| `reset` \| `clear_all`), `filter_group`, `filter_value`, `active_filter_count`, `result_count` | 2, 19 |
| 7 | `sort_changed` | `surface`, `sort_field`, `sort_direction`, `result_count` | 2, 19 |
| 8 | `item_expanded` | `surface`, `entity_type`, `entity_id`, `action` (`expand` \| `collapse`), `module` | 17 (DIR cards, chips +3, View more, FAQ rows) |
| 9 | `list_opened` | `surface`, `target_list`, `item_count`, `module` | 18 (every VIEW ALL) |
| 10 | `entity_shared` | `entity_type` (`story` \| `company` \| `sector`), `entity_id`, `channel`, `source` | 15 — then retire `story_shared` after a dual-write window |
| 11 | `rating_prompt_shown` / `rating_prompt_actioned` | `trigger` (`brief_end` \| `profile_row`), `action` (`rate` \| `later` \| `dismiss`), `brief_position` | 22 |
| 12 | `stock_row_tapped` | `company_id`, `list_type` (`gainers` \| `losers` \| `recently_listed`), `position`, `change_pct` | 1 — the only genuinely new domain that needs its own event |

`push_opened` (gap 6) and the sector rail (gap 4) are already specified in the attribution docs — rail taps become `screen_viewed` with `referrer_module=story_rail` plus `ring_state`.

### 5.2 Property work, not event work

| Change | Where |
|---|---|
| Add `referrer_screen` / `referrer_module` / `referrer_position` | universal — from `03-implementation-handoff.md` §2 |
| Add `theme` and `auth_state` as **super properties** | every event, set once per session and on change |
| Extend `card_type` | `story` · `company` · `stock` · `sector` · `edition` · `directory` |
| Extend `profile_section_viewed.section` | + `overview` · `investments` · `acquisitions` |
| Fix `watchlist_viewed.entity_tab` | populate it (72% null today) and rename `industry` → `sector` to match `watchlist_entity_added` |
| Extend `search_initiated.surface` | + `brief_header` · `company_hub` · `directory` |
| Extend `notification_settings_changed.setting` | + `master` · `delivery_time`, and allow a time value in `new_value` |
| Collapse duplicate enum values | `company_profile_viewed.source`: `companies` \| `companies_directory` → one. `story_shared.source`: `article` \| `article_reader` → one |
| Populate `brief_page_opened.is_edition_switch` | null on 91% today; and add `edition_day` so the week tabs are analysable |

### 5.3 Sequence

| Phase | Contents | Why this order |
|---|---|---|
| A | `screen_viewed` + `referrer_*` + `theme` / `auth_state` super props | one change closes the largest share of gaps and makes every later event self-describing |
| B | `tab_changed`, `drawer_opened` / `_dismissed`, `item_expanded`, `list_opened` | four generic events, no new domain logic, cover ~15 gaps |
| C | `filter_changed`, `sort_changed`, `stock_row_tapped` | the Directory and Stock Watch surfaces — required before either ships, not after |
| D | `entity_shared`, `rating_prompt_*`, enum extensions, `push_opened` | cleanup + the known-broken items |
| E | `screen_refreshed`, `empty_state_shown`, `content_load_failed`, `retry_tapped`, `network_state_changed` | state and reliability layer |

**Hard rule for anything new:** no event ships without `referrer_screen`, and no new surface (Stock Watch, Directory, Rewards) ships without its events in the same release. Both Stock Watch and the Directory are currently drawn and unins­trumented — if they ship as designed today, they launch blind.

---

## 6. Decisions needed

1. **Generic vs bespoke** — approve the 12-event generalised model, or do you want per-surface events (≈35 names)?
2. **`screen_viewed` on every screen** — it roughly doubles event volume. Approve, or restrict to a screen allowlist?
3. **`story_shared` → `entity_shared`** — dual-write for one release, or break history?
4. **Nav IA change** — the Figma nav bar is Brief / Article / Company. The Master PRD and prior memory record Brief / Explore / Watchlist. Which is current? Every `source` / `referrer_screen` enum depends on the answer.
5. **Stock Watch data source** — is it DataLabs or a market-data vendor? `stock_row_tapped` needs a stable `company_id` that matches the profile screen's.
