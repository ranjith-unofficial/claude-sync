# App event tracking: how we fix the gaps

**Updated:** 13 September 2026 · **Status:** approach agreed, event names proposed
**Full evidence:** `app-event-coverage-vs-figma-settled.md` (same folder).

---

## 1. The problem

- The new app designs have **23 places where a user can do something and we record nothing**, or record it too vaguely to use.
- The app no longer has an Explore screen. It has an **Article section and a Company section, each with its own tabs**. Our events still describe the old Explore screen.
- Card events cannot tell a Brief card from an Article card, so we cannot say which card a user saw.

## 2. What we agreed (13 Sep)

| # | Decision | What it means |
|---|---|---|
| 1 | Fix existing events first, then add new ones | Step 1 is only fixes to events that already fire. New events start in Step 2 |
| 2 | Bottom nav is Brief / Article / Company. No Explore | `explore_viewed` is replaced. Every "came from" value uses Brief, Article, Company |
| 3 | One view event for the Article page and one for the Company page, with the tab as a field | Switching tabs inside Article or Company fires the same event with a different tab value |
| 4 | The landing page of Article and of Company works like Explore, with many sections | New event `section_viewed`, with a page type field (article home or company home) |
| 5 | Add `story_opened`; `card_viewed` must say where the card is | `card_viewed` gets a field: brief or article |

## 3. Step 1: fix events that already exist

| Event today | What is wrong | Fix |
|---|---|---|
| `card_viewed` card type | Always says "story". Cannot tell a Brief card from an Article card | Add a field for where the card is: brief or article. Also allow card types company, stock, sector, edition, directory |
| `profile_section_viewed` | No value for Overview, Investments, Acquisitions | Add those three |
| `watchlist_viewed` tab | Empty on 72% of events; says "industry" where the add event says "sector" | Always fill it; use "sector" in both |
| `search_initiated` surface | Only ever says "explore" | Replace with Brief header, Article home, Company home, Directory |
| `notification_settings_changed` | No master on/off switch, no delivery time | Add both |
| `brief_page_opened` edition switch | Empty on 91% of events | Always fill it; add which day was picked |
| `company_profile_viewed` source | Two values for the same place: "companies" and "companies_directory" | Keep one |
| `story_shared` source | Two values for the same place: "article" and "article_reader" | Keep one |
| `push_opened` | Does not exist at all | Build it (already specified in the attribution docs) |

## 4. Step 2: Article and Company pages, sections, stories, cards

| Event | When it fires | Fields | Example |
|---|---|---|---|
| `article_home_viewed` | User lands on the Article page or switches a tab on it | tab (News, In-Depth, Markets, Financials, Startups, D2C, Newsletter), source | Article page, tab Markets, came from Brief |
| `company_home_viewed` | User lands on the Company page or switches a tab on it | tab (All, Recently funded, Just launched, Early rounds, Profitable, Unicorns, Sectors), source | Company page, tab Unicorns, came from nav bar |
| `section_viewed` | A section on the Article or Company landing page comes into view | page_type (article_home or company_home), tab, section_name, position | company_home, Stock Watch, position 2 |
| `story_opened` | User opens a story | source_type (brief or article), story_id, position | Opened from Brief, card 3 |
| `card_viewed` (existing, extended) | A card is shown | source_type (brief or article), card_type, story_id or company_id, position | Article home, Top Stories, card 5 |
| `explore_viewed` (existing) | Retire | Send alongside the two new home events for one release, then stop it | |

## 5. Step 3 onward: other new events

| Event | What it records | Example |
|---|---|---|
| `filter_changed` | A filter was applied, removed, reset or cleared, and which one | Directory: Sector = Fintech, 12,480 results |
| `sort_changed` | The sort order changed | Directory sorted by total funding |
| `stock_row_tapped` | A row in Stock Watch was tapped | Top gainers, row 3 |
| `drawer_opened` / `drawer_dismissed` | A bottom sheet opened or closed, and how it closed | Sign-in sheet closed with "Not now" |
| `item_expanded` | A card or row was expanded or collapsed | Directory card "View more" |
| `list_opened` | User tapped "View all" into a full list | "View all 25 funding rounds" |
| `entity_shared` | Share tapped on a story, company or sector | Replaces today's story-only share event |
| `rating_prompt_shown` / `_actioned` | The "Enjoyed today's brief?" sheet appeared, and what the user chose | "Maybe later" |
| `theme` and `auth_state` on every event | Light or dark mode; guest or signed in | Today dark-mode usage cannot be measured |

## 6. Screen state (last)

| Event | What it records |
|---|---|
| `screen_refreshed` | Refresh, and whether content was new, unchanged or failed |
| `empty_state_shown` | Screen showed "nothing here" (empty watchlist, no filter results, offline) |
| `content_load_failed` | Content failed to load, and whether it can be retried |
| `retry_tapped` | User tapped retry after a failure |
| `network_state_changed` | Phone went offline or came back online |
| ~~`session_end`~~ | **Do not build.** PostHog already marks every event with a session |

## 7. Order of work

Where, for all steps: **the INC42 app (Android and iOS), in the code that sends events to PostHog.**

| Step | What exactly to do | Done when |
|---|---|---|
| **1. Fix existing** | Make every fix in section 3 | In PostHog (app project), none of the section 3 fields are empty, and `card_viewed` shows brief or article on every event |
| **2. Pages and cards** | Add `article_home_viewed`, `company_home_viewed`, `section_viewed`, `story_opened`. Extend `card_viewed`. Send `explore_viewed` alongside for one release | On a test phone: every tab switch on Article and Company fires one event with the right tab; scrolling a landing page fires `section_viewed` per section; opening a story from Brief and from Article shows the right source_type |
| **3. Directory and Stock Watch** | Add `filter_changed`, `sort_changed`, `stock_row_tapped`. Ship in the same release as those screens | Applying a filter on a test phone records which filter and the result count |
| **4. Common actions** | Add drawer, expand, "View all", share and rating events, plus `theme` and `auth_state` on every event | Tapping each drawer, "View more" and "View all" on a test phone produces one event each |
| **5. Screen state** | Add the section 6 events | Airplane mode on a test phone records `network_state_changed` and, on a failed screen, `content_load_failed` |

## 8. Rules from now on

1. Every view event carries where the user came from.
2. No new screen ships without its events in the same release.

## 9. Still open

| # | Question | Why it matters |
|---|---|---|
| 1 | `story_opened` vs the existing `article_opened`: is `story_opened` the tap on a story card, and `article_opened` the full article reading screen? | If both mean the same thing, keep one and avoid double counting |
| 2 | Confirm the event names in section 4 | Names are hard to change once data starts flowing |
| 3 | Stock Watch data: DataLabs or an outside market-data provider? | The stock row must use the same company ID as the company page |
