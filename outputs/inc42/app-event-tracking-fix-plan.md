# App event tracking: how we fix the gaps

**Date:** 13 September 2026 · **Status:** plan, 5 decisions open
**Full evidence:** `app-event-coverage-vs-figma-settled.md` (same folder). This page is the short version.

---

## 1. The problem, in three lines

- The new app designs (Figma "SCREENS SETTLED") have **23 places where a user can do something and we record nothing**, or record it too vaguely to use.
- Some are whole screens: Stock Watch, the Company Directory with its filters, Rewards, the bottom nav bar.
- If these ship as designed today, they launch with no data. We will not be able to say whether anyone uses them.

## 2. The approach, in one idea

**Build a few reusable events, not one event per button.**

Most of the 23 gaps are the same action repeated on different screens: opening a drawer, switching a tab, expanding a card, tapping "View all". So one event for "a drawer was opened" (with a field saying *which* drawer) covers all 12+ drawers.

| Option | New event names | Upkeep |
|---|---|---|
| **Reusable events (recommended)** | 12 | one list, new screens need no new events |
| One event per button/screen | about 35 | grows with every new screen |

## 3. The 12 new events, in plain words

| # | Event | What it records | Example |
|---|---|---|---|
| 1 | `screen_viewed` | a screen was shown, and which screen the user came from | Company page, came from Brief |
| 2 | `screen_refreshed` | user pulled to refresh, and whether anything new came back | Brief refreshed, nothing new |
| 3 | `tab_changed` | user switched a tab: bottom nav bar, any sub-tab row, week tabs | Company hub: All → Unicorns |
| 4 | `drawer_opened` | a bottom sheet opened | Filters drawer |
| 5 | `drawer_dismissed` | a bottom sheet closed, and how (button, cancel, swipe) | Sign-in sheet closed with "Not now" |
| 6 | `filter_changed` | a filter was applied, removed, reset or cleared, and which one | Directory: Sector = Fintech, 12,480 results |
| 7 | `sort_changed` | the sort order changed | Directory sorted by total funding |
| 8 | `item_expanded` | a card or row was expanded or collapsed | Directory card "View more" |
| 9 | `list_opened` | user tapped "View all" into a full list | "View all 25 funding rounds" |
| 10 | `entity_shared` | share tapped on a story, company or sector | replaces today's story-only share event |
| 11 | `rating_prompt_shown` / `_actioned` | the "Enjoyed today's brief?" sheet appeared, and what the user chose | "Maybe later" |
| 12 | `stock_row_tapped` | a row in Stock Watch was tapped | Top gainers, row 3 |

**Attached to every event automatically:** `theme` (light or dark) and `auth_state` (guest or signed in). Today we cannot tell dark-mode usage at all.

## 4. Fixes to events that already exist

| Event today | What is wrong | Fix |
|---|---|---|
| Explore / sub-tab field | only knows 2 tabs; the new design has up to 7 per screen | covered by `tab_changed` |
| `card_viewed` card type | always says "story" | also allow company, stock, sector, edition, directory |
| `profile_section_viewed` | no value for Overview, Investments, Acquisitions | add those three |
| `watchlist_viewed` tab | empty on 72% of events; says "industry" where the add event says "sector" | always fill it; use "sector" in both |
| `search_initiated` surface | only ever says "explore" | add Brief header, Company hub, Directory |
| `notification_settings_changed` | no master on/off switch, no delivery time | add both |
| `brief_page_opened` edition switch | empty on 91% of events | always fill it; add which day was picked |
| `push_opened` | does not exist at all | build it (already specified in the attribution docs) |

## 5. Screen state list (separate, as asked)

| Event | What it records |
|---|---|
| `screen_refreshed` | refresh, and whether content was new, unchanged or failed |
| `empty_state_shown` | screen showed "nothing here" (empty watchlist, no filter results, offline) |
| `content_load_failed` | content failed to load, and whether it can be retried |
| `retry_tapped` | user tapped retry after a failure |
| `network_state_changed` | phone went offline or came back online |
| ~~`session_end`~~ | **do not build.** PostHog already marks every event with a session |

## 6. Order of work

Each step is one release's worth of work. Where to change it, for all steps: **the INC42 app (Android and iOS), in the code that sends events to PostHog.**

| Step | What exactly to do | Done when |
|---|---|---|
| **A. Screen views** | Add `screen_viewed` with "came from" fields. Attach `theme` and `auth_state` to every event. | In PostHog (app project), every screen in the Figma list shows up under `screen_viewed`, and a random event shows `theme` filled in |
| **B. Common actions** | Add `tab_changed`, `drawer_opened`, `drawer_dismissed`, `item_expanded`, `list_opened`. | Tapping each tab, drawer, "View more" and "View all" on a test phone produces one event each, with the right screen name |
| **C. Directory and Stock Watch** | Add `filter_changed`, `sort_changed`, `stock_row_tapped`. **Must ship in the same release as those screens, not after.** | Applying a filter on a test phone records which filter and the result count |
| **D. Clean-up** | Add `entity_shared` (send it alongside the old story share event for one release, then stop the old one). Add rating sheet events. Make every fix in section 4. Build `push_opened`. | Section 4 fields are no longer empty; opening the app from a notification records `push_opened` |
| **E. Screen state** | Add the section 5 events. | Turning on airplane mode on a test phone records `network_state_changed` and, on a failed screen, `content_load_failed` |

**Why this order:** step A alone closes the largest share of gaps and makes every later event show where the user came from.

## 7. Rules from now on

1. No new event ships without the "came from screen" field.
2. No new screen ships without its events in the same release.

## 8. Decisions needed

| # | Decision | Recommendation |
|---|---|---|
| 1 | Reusable events (12) or one per button (about 35)? | Reusable |
| 2 | `screen_viewed` on every screen, or only a chosen list? It roughly doubles event volume. | Every screen. Current volume is low (the busiest event is 16,201 in 30 days). Confirm PostHog billing first |
| 3 | Share event: send old and new together for one release, or switch at once and lose comparable history? | Send both for one release |
| 4 | **Bottom nav:** Figma shows Brief / Article / Company. Older docs say Brief / Explore / Watchlist. Which is current? | **Needs your answer.** Every "came from" screen name depends on it |
| 5 | Stock Watch data: DataLabs or an outside market-data provider? | **Needs your answer.** The stock row must use the same company ID as the company page |
