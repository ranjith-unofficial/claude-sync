# Inc42 App Analytics Audit — Execute This Now

## READ THIS BEFORE ANYTHING ELSE

This is a task to execute immediately using your tools. It is not a document to edit, reformat, review, or summarize back.

**Your deliverable is real data**, produced by actually querying PostHog and Customer.io — not by reading this file and describing what you would do.

### DO
- Actually run PostHog queries against project 146258 and get real event names, real volumes, real property payloads.
- Actually open the Google Sheet tabs named below and read every row, including the Status/Notes/Tech Status columns.
- Actually check Customer.io's live event data for the app, using browser tools if no direct API/MCP access exists.
- Write your findings into the two new Sheet tabs specified in Part D — that is the finished deliverable.
- If you hit a login wall or missing tool access, stop and say exactly what's blocked, then wait. Do not proceed on guesses.

### DO NOT
- Do NOT edit, rewrite, restructure, or "clean up" this instructions file. It is reference material for you to follow, not your output.
- Do NOT respond with a plan, an outline, or a description of the steps you're about to take instead of taking them.
- Do NOT infer or guess what PostHog/Customer.io are receiving based on what the sheet claims. Several rows already admit they're wrong (see Part B2) — you must verify live, not trust the doc.
- Do NOT report "I've reviewed the sheet and instructions" as if that were progress. Progress is filled rows in the output tabs (Part D).
- Do NOT fabricate volumes, property names, or "typical" payloads. If you can't query it, say so.
- Do NOT report raw PostHog volume numbers as clean external-user behavior without flagging the internal-user pollution caveat in Part A.
- If your first instinct after reading this is to touch `app-analytics-audit-instructions.md` itself, that is the wrong action — stop and re-read this section.

**The three questions this task exists to answer, and nothing less than this counts as done:**
1. How many events does PostHog/Customer.io actually show for the app, and what are they, with what real volume?
2. For every event that IS in the sheet — is it firing the way the sheet says (same name, same properties), or has it drifted, including the properties already admitted to be broken?
3. Which events are firing that have NO row in the sheet at all?

---

## Part A — Access and tools

1. **PostHog access** to project **146258, "Inc42 App"** (EU cloud). If not authenticated, run `mcp__plugin_posthog_posthog__authenticate` or invoke the `posthog:querying-posthog-data` skill. **Confirm this project is active before every query** — the account has multiple INC42 projects and silently reverts mid-session.
2. **Customer.io access** for the app workspace (Customer.io is confirmed live for both website AND app, EU region — do not assume it's app-only or website-only). No dedicated MCP — use browser automation (`ToolSearch` query `"select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__find"`). If no logged-in session exists, stop and ask Ranjith to log in first.
3. **Known measurement caveat — apply this to every volume you report:** a prior PostHog review found no internal/beta-user exclusion exists on this project — roughly a fifth of "active" users at the time were pre-launch beta/internal people with no filterable property. Flag any volume number that could be materially affected by this rather than presenting it as clean.
4. **Google Sheet access** to the sheet below. Pull tab contents as real data via the CSV export trick — navigate to `https://docs.google.com/spreadsheets/d/1n6r5QXe-9Pq1uAWMKRe7zSgLHSejASzAq-BAqeI3L6Y/export?format=csv&gid=<gid>` for a given tab (get gids by reading `.docs-sheet-tab` click-through URL hashes via `javascript_tool`) — then read the CSV with the `Read` tool.

---

## Part B — Read the source tabs

Sheet: https://docs.google.com/spreadsheets/d/1n6r5QXe-9Pq1uAWMKRe7zSgLHSejASzAq-BAqeI3L6Y

1. Read tab **"App - Events"** in full (98 rows across 11 groups: Lifecycle, Onboarding, Brief, Streak, Watchlist, Explore, Profiles, Notifications, Auth, Ops, Content). Columns: Group, Event, Fires when, Event Property Groups, Event properties, Status, Person Property to Update, Identify Call, PostHog, Firebase, Customer.io, Singular/SKAN, Metric/trigger served, Build status, Notes, Tech Status.
2. Read tab **"App - Event Properties"** in full — the property dictionary (Super/Story/Person groups, then a flat property-by-property list).
3. **The "Status" column on many rows is not a simple checkmark — it contains free-text admissions of known bugs. Read every one of these before treating a row as reliable.** Confirmed issues to verify current state on, not rediscover:
   - `deep_link_opened`: Status says "no source, medium, content" — those UTM/source properties aren't actually captured.
   - `brief_page_opened`: Status says "source is still wrong."
   - `story_shared` / `card_rated`: Status says the `channel` property is wrong; fallback is to keep only the bare event if channel can't be fetched.
   - `streak_milestone_viewed`: Status says it's "firing on unrelated days" (wrong trigger condition).
   - `watchlist_entity_added`: multiple admitted issues — no `setPersonProperties` call fires, `entity_name` is null when tracking a sector but not null when removing it, `watchlist_size_after` is wrong.
   - `search_result_tapped`: `entity_or_story_id` contains a story slug instead of an ID when tapping an article result.
   - `push_permission_granted`, `push_permission_denied`, `notification_settings_changed`, `preferences_updated`: `setPersonProperties` call doesn't work for non-logged-in users, only for logged-in ones.
   - `sign_in_prompt_shown`: marked "not working."
   - `summary_expanded`: sends `entity_or_story_id` instead of a proper `story_id`.
   - A prior instrumentation review found `push_delivered` never fired and `push_opened` fired only twice despite 67% push opt-in, and `decode` (the AI explainer) has zero telemetry.

---

## Part C — Query PostHog and Customer.io for the real event list

1. Confirm active PostHog project = 146258.
2. Run:
   ```sql
   SELECT event, count() AS volume, min(timestamp) AS first_seen
   FROM events
   WHERE timestamp > now() - INTERVAL 90 DAY
   GROUP BY event
   ORDER BY volume DESC
   ```
   via the `posthog:querying-posthog-data` skill. Filter out PostHog-internal events (`$pageview`, `$autocapture`, `$identify`, etc.) unless the sheet expects one.
3. Specifically check: does `push_delivered` or `push_opened` have any volume in the last 30 days? Does `decode` have any volume at all? These are the highest-priority items to re-verify — report their current status explicitly, don't bury them in the general table.
4. For anything unmatched against Part B, or with unexpected properties, run:
   ```sql
   SELECT properties FROM events WHERE event = '<event_name>' ORDER BY timestamp DESC LIMIT 10
   ```
   and record the actual property keys/values — specifically check whether the 9 admitted-broken properties from Part B3 are still broken.
5. Using browser tools, open Customer.io's app workspace → Activity Log / Data Pipelines → Events. Extract the distinct event list and visible counts via `get_page_text`/`read_page`.

---

## Part D — Produce your two deliverable tabs

Using browser automation on the live Google Sheet:

**Tab 1 — "App Audit — [Agent Run Date]"**: duplicate of "App - Events," with columns added and filled for every existing row: `Live in PostHog? (Y/N + volume)`, `Live in Customer.io? (Y/N)`, `Actual Name if Different`, `Actual Properties`, `Bug Status (fixed/still broken/new issue)`, `Recommendation`.

**Tab 2 — "App — New Events Found"**: new tab, one row per event with no corresponding sheet row at all:

| Event name (as seen live) | Platform (PostHog / Customer.io) | First seen | Volume (30 days, flag if internal-user-polluted) | Matches a sheet row? (N) | Actual properties captured | Classification | Recommendation |
|---|---|---|---|---|---|---|---|

Classification options: Confirmed correct / Renamed / Property mismatch / Broken-not firing / Dead-test event.
Recommendation options: update sheet to match reality / fix production to match sheet's intended name-properties / needs product owner decision / no action.

---

## Part E — When you're done

Confirm, explicitly, in your final response:
- Both output tabs exist and are fully filled.
- Current status of `push_delivered`, `push_opened`, and `decode` (Part C step 3), stated plainly.
- Current status of the 9 admitted-broken properties from Part B3 — fixed or still broken, one line each.
- Any blockers hit and what's needed to proceed if incomplete.

Do not describe this as "instructions reviewed" or "sheet read." Report actual completion state of the two tabs and the priority re-checks.
