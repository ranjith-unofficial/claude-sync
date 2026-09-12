# Event-level PostHog ↔ Customer.io gaps (full App taxonomy)

**Audited:** 2026-09-12 17:19 IST  
**PH project:** Inc42 App `146258` (30d HogQL counts)  
**CIO workspace:** Inc42 App `224949`  
**CIO volume metric:** `event_names.get` → `daily_count` (today only; not 30d). Existence via catalog + `last_seen_at`.  
**Limitation:** No bulk CIO 30d event volume API via GET; profile-count POSTs exist but were not used (read-only GET). Prior Aug 29 `% of profiles` cited where useful.

## Master gap table (all 66 App.csv events)

| event_name | expected_PH | expected_CIO | PH_30d_cnt | PH_30d_uniq | CIO_daily | CIO_status | Gap flag |
|------------|-------------|--------------|------------|-------------|-----------|------------|----------|
| `app_opened` | Y | N | 5731 | 1321 | 105 | live | CIO_UNEXPECTED |
| `deep_link_opened` | Y | N | 1202 | 579 | n/a | not expected (dest) | ok |
| `app_installed` | Y | Y | 1276 | 1263 | 18 | live | ok |
| `app_updated` | Y | Y | 43 | 40 | 0 | catalog Y / daily 0 | CIO_NEAR_ZERO;PH>0_CIO_daily0 |
| `force_update_shown` | Y | N | 0 | 0 | n/a | not expected (dest) | PH_DEAD |
| `onboarding` | Y | N | 5176 | 1277 | n/a | not expected (dest) | ok |
| `onboarding_completed` | Y | Y | 1112 | 1044 | 15 | live | ok |
| `walkthrough` | Y | Y | 3734 | 1026 | 48 | live | ok |
| `brief_page_opened` | Y | N | 10424 | 1090 | n/a | not expected (dest) | ok |
| `brief_opened` | Y | Y | 3138 | 700 | 57 | live | ok |
| `card_viewed` | Y | N | 16273 | 701 | n/a | not expected (dest) | ok |
| `article_opened` | Y | N | 3088 | 641 | n/a | not expected (dest) | ok |
| `decode` | Y | N | 0 | 0 | n/a | not expected (dest) | PH_DEAD |
| `brief_completed` | Y | Y | 1130 | 338 | 24 | live | ok |
| `brief_fallback_shown` | Y | N | 0 | 0 | n/a | not expected (dest) | PH_DEAD |
| `story_saved` | Y | Y | 194 | 68 | 1 | live | ok |
| `story_unsaved` | Y | Y | 23 | 12 | 0 | catalog Y / daily 0 | CIO_NEAR_ZERO;PH>0_CIO_daily0 |
| `story_shared` | Y | N | 196 | 84 | n/a | not expected (dest) | ok |
| `card_rated` | Y | N | 0 | 0 | n/a | not expected (dest) | PH_DEAD |
| `streak_opened` | Y | N | 364 | 163 | n/a | not expected (dest) | ok |
| `streak_milestone_viewed` | Y | N | 337 | 207 | n/a | not expected (dest) | ok |
| `watchlist_entity_added` | Y | Y | 274 | 75 | 2 | live | ok |
| `watchlist_entity_removed` | Y | Y | 32 | 19 | 0 | catalog Y / daily 0 | CIO_NEAR_ZERO;PH>0_CIO_daily0 |
| `watchlist_viewed` | Y | N | 2056 | 924 | n/a | not expected (dest) | ok |
| `watchlist_limit_hit` | Y | N | 0 | 0 | n/a | not expected (dest) | PH_DEAD |
| `explore_viewed` | Y | N | 9118 | 1032 | n/a | not expected (dest) | ok |
| `sector_landing_viewed` | Y | N | 144 | 39 | n/a | not expected (dest) | ok |
| `search_initiated` | Y | N | 396 | 155 | n/a | not expected (dest) | ok |
| `search_performed` | Y | N | 1866 | 149 | n/a | not expected (dest) | ok |
| `search_result_tapped` | Y | N | 324 | 118 | n/a | not expected (dest) | ok |
| `company_profile_viewed` | Y | N | 954 | 293 | n/a | not expected (dest) | ok |
| `profile_opened` | Y | N | 825 | 330 | n/a | not expected (dest) | ok |
| `profile_section_viewed` | Y | N | 4349 | 290 | n/a | not expected (dest) | ok |
| `locked_feature_tapped` | Y | N | 0 | 0 | n/a | not expected (dest) | PH_DEAD |
| `interest_captured` | Y | Y | 0 | 0 | 0 | ABSENT/never | PH_DEAD;CIO_ABSENT |
| `push_permission_prompted` | Y | N | 1319 | 1133 | n/a | not expected (dest) | ok |
| `push_permission_granted` | Y | Y | 705 | 700 | 11 | live | ok |
| `push_permission_denied` | Y | Y | 616 | 432 | 6 | live | ok |
| `push_delivered` | Y | Y | 0 | 0 | 0 | ABSENT/never | PH_DEAD;CIO_ABSENT |
| `push_opened` | Y | Y | 0 | 0 | 0 | catalog Y / daily 0 | PH_DEAD;CIO_NEAR_ZERO |
| `notification_settings_changed` | Y | Y | 60 | 16 | 0 | catalog Y / daily 0 | CIO_NEAR_ZERO;PH>0_CIO_daily0 |
| `sign_in_prompt_shown` | Y | N | 162 | 91 | n/a | not expected (dest) | ok |
| `sign_in_started` | Y | N | 1520 | 1069 | n/a | not expected (dest) | ok |
| `sign_in_completed` | Y | Y | 2439 | 961 | 45 | live | ok |
| `register` | Y | Y | 481 | 479 | 9 | live | ok |
| `signed_out` | Y | Y | 51 | 22 | 1 | live | ok |
| `account_deleted` | Y | Y | 6 | 6 | 0 | catalog Y / daily 0 | CIO_NEAR_ZERO;PH>0_CIO_daily0 |
| `rating_prompt_shown` | Y | N | 0 | 0 | n/a | not expected (dest) | PH_DEAD |
| `error_shown` | Y | N | 472 | 116 | n/a | not expected (dest) | ok |
| `preferences_updated` | Y | Y | 112 | 36 | 3 | live | ok |
| `menu_item_tapped` | Y | N | 276 | 43 | n/a | not expected (dest) | ok |
| `scroll_depth` | Y | N | 3966 | 504 | n/a | not expected (dest) | ok |
| `summary_expanded` | Y | N | 2296 | 453 | n/a | not expected (dest) | ok |
| `profile_name_updated` | Y | Y | 0 | 0 | 0 | ABSENT/never | PH_DEAD;CIO_ABSENT |
| `article_published` | Y | Y | 0 | 0 | 3 | live | PH_DEAD;CIO_ONLY_REVERSE |
| `Application Backgrounded` | Y | N | 11301 | 1272 | n/a | not expected (dest) | ok |
| `Application Foregrounded` | Y | N | 0 | 0 | n/a | not expected (dest) | PH_DEAD |
| `Application Installed` | Y | N | 0 | 0 | n/a | not expected (dest) | PH_DEAD |
| `Application Opened` | Y | N | 5493 | 1337 | n/a | not expected (dest) | ok |
| `brief_open_today` | Y | N | 0 | 0 | n/a | not expected (dest) | PH_DEAD |
| `brief_story_rated` | Y | N | 73 | 13 | n/a | not expected (dest) | ok |
| `company_untracked` | Y | N | 0 | 0 | n/a | not expected (dest) | PH_DEAD |
| `industry_untracked` | Y | N | 0 | 0 | n/a | not expected (dest) | PH_DEAD |
| `push_priming_dismissed` | Y | N | 0 | 0 | n/a | not expected (dest) | PH_DEAD |
| `share_initiated` | Y | N | 0 | 0 | n/a | not expected (dest) | PH_DEAD |
| `Application Became Active` | Y | N | 9275 | 1270 | n/a | not expected (dest) | ok |

## Highlighted gaps (both-dest or dead)

| event | exp PH/CIO | PH_30d | CIO_daily | flag |
|-------|------------|--------|-----------|------|
| `app_opened` | Y/N | 5731 | 105 | CIO_UNEXPECTED |
| `app_updated` | Y/Y | 43 | 0 | CIO_NEAR_ZERO;PH>0_CIO_daily0 |
| `force_update_shown` | Y/N | 0 | n/a | PH_DEAD |
| `decode` | Y/N | 0 | n/a | PH_DEAD |
| `brief_fallback_shown` | Y/N | 0 | n/a | PH_DEAD |
| `story_unsaved` | Y/Y | 23 | 0 | CIO_NEAR_ZERO;PH>0_CIO_daily0 |
| `card_rated` | Y/N | 0 | n/a | PH_DEAD |
| `watchlist_entity_removed` | Y/Y | 32 | 0 | CIO_NEAR_ZERO;PH>0_CIO_daily0 |
| `watchlist_limit_hit` | Y/N | 0 | n/a | PH_DEAD |
| `locked_feature_tapped` | Y/N | 0 | n/a | PH_DEAD |
| `interest_captured` | Y/Y | 0 | 0 | PH_DEAD;CIO_ABSENT |
| `push_delivered` | Y/Y | 0 | 0 | PH_DEAD;CIO_ABSENT |
| `push_opened` | Y/Y | 0 | 0 | PH_DEAD;CIO_NEAR_ZERO |
| `notification_settings_changed` | Y/Y | 60 | 0 | CIO_NEAR_ZERO;PH>0_CIO_daily0 |
| `account_deleted` | Y/Y | 6 | 0 | CIO_NEAR_ZERO;PH>0_CIO_daily0 |
| `rating_prompt_shown` | Y/N | 0 | n/a | PH_DEAD |
| `profile_name_updated` | Y/Y | 0 | 0 | PH_DEAD;CIO_ABSENT |
| `article_published` | Y/Y | 0 | 3 | PH_DEAD;CIO_ONLY_REVERSE |
| `Application Foregrounded` | Y/N | 0 | n/a | PH_DEAD |
| `Application Installed` | Y/N | 0 | n/a | PH_DEAD |
| `brief_open_today` | Y/N | 0 | n/a | PH_DEAD |
| `company_untracked` | Y/N | 0 | n/a | PH_DEAD |
| `industry_untracked` | Y/N | 0 | n/a | PH_DEAD |
| `push_priming_dismissed` | Y/N | 0 | n/a | PH_DEAD |
| `share_initiated` | Y/N | 0 | n/a | PH_DEAD |

## Both-dest events (23) — live CIO daily vs PH 30d

| event | PH_30d | PH_uniq | CIO_daily | Notes |
|-------|--------|---------|-----------|-------|
| `app_installed` | 1276 | 1263 | 18 |  |
| `app_updated` | 43 | 40 | 0 | PH 43 / CIO daily 0 |
| `onboarding_completed` | 1112 | 1044 | 15 |  |
| `walkthrough` | 3734 | 1026 | 48 |  |
| `brief_opened` | 3138 | 700 | 57 |  |
| `brief_completed` | 1130 | 338 | 24 | PH 1130 / CIO daily 24 — live but per-user gaps (12% cohort) |
| `story_saved` | 194 | 68 | 1 |  |
| `story_unsaved` | 23 | 12 | 0 | PH 23 / CIO daily 0 |
| `watchlist_entity_added` | 274 | 75 | 2 |  |
| `watchlist_entity_removed` | 32 | 19 | 0 | PH 32 / CIO daily 0 |
| `interest_captured` | 0 | 0 | 0 | ABSENT both PH+CIO — still broken (Aug 29 STILL BROKEN) |
| `push_permission_granted` | 705 | 700 | 11 |  |
| `push_permission_denied` | 616 | 432 | 6 |  |
| `push_delivered` | 0 | 0 | 0 | ABSENT both — still broken |
| `push_opened` | 0 | 0 | 0 | PH 0 / CIO daily 0 — near-dead |
| `notification_settings_changed` | 60 | 16 | 0 | PH 60 / CIO daily 0 |
| `sign_in_completed` | 2439 | 961 | 45 | PH 2439 / CIO daily 45 — live; intermittent per-user miss (Exhibit A) |
| `register` | 481 | 479 | 9 |  |
| `signed_out` | 51 | 22 | 1 |  |
| `account_deleted` | 6 | 6 | 0 | PH 6 / CIO daily 0 (low volume) |
| `preferences_updated` | 112 | 36 | 3 |  |
| `profile_name_updated` | 0 | 0 | 0 | ABSENT both |
| `article_published` | 0 | 0 | 3 | PH 0 but CIO daily 3 — reverse / backend-only? |

## Destination sheet vs reality

- Taxonomy `destinations` marks **23** events for Customer.io; CIO App catalog lists **56** event names (many PH-only sheet events still arrive, e.g. `brief_page_opened`, `app_opened` daily_count=105).
- `app_opened` is **posthog-only** on sheet but live in CIO (daily 105) — sheet under-lists fan-out.
- Aug 29 aggregate `% of profiles` cannot prove per-user parity (this audit’s point).

## API limitations

1. CIO `GET .../customers/:id/events` is **not** in schema; use `GET .../logs?internal_id=&type=event` (~30d, max 50/page).
2. `event_names.list` `last_seen` field is 0; use `event_names.get` for `daily_count` + `metadata.last_seen_at`.
3. No GET bulk 30d CIO volume; `daily_count` is today-only — do not invent 30d CIO totals.
4. Profile-count / usage endpoints are POST — not used in this read-only pass.
