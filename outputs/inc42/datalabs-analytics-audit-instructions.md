# DataLabs Analytics Audit — Execute This Now

## READ THIS BEFORE ANYTHING ELSE

This is a task to execute immediately using your tools. It is not a document to edit, reformat, review, or summarize back.

**Your deliverable is real data**, produced by actually querying PostHog and Customer.io — not by reading this file and describing what you would do.

### DO
- Actually run PostHog queries against project 66351 and get real event names, real volumes, real property payloads.
- Actually open the Google Sheet tabs named below and read every row, including the Remarks column.
- Actually check Customer.io's live event data, using browser tools if no direct API/MCP access exists.
- Write your findings into the two new Sheet tabs specified in Part D — that is the finished deliverable.
- If you hit a login wall or missing tool access, stop and say exactly what's blocked, then wait. Do not proceed on guesses.

### DO NOT
- Do NOT edit, rewrite, restructure, or "clean up" this instructions file. It is reference material for you to follow, not your output.
- Do NOT respond with a plan, an outline, or a description of the steps you're about to take instead of taking them.
- Do NOT infer or guess what PostHog/Customer.io are receiving based on what the sheet claims. The entire point of this task is that the sheet may be wrong — you must pull live data yourself.
- Do NOT report "I've reviewed the sheet and instructions" as if that were progress. Progress is filled rows in the output tabs (Part D).
- Do NOT fabricate volumes, property names, or "typical" payloads. If you can't query it, say so.
- If your first instinct after reading this is to touch `datalabs-analytics-audit-instructions.md` itself, that is the wrong action — stop and re-read this section.

**The three questions this task exists to answer, and nothing less than this counts as done:**
1. How many events does PostHog/Customer.io actually show for DataLabs, and what are they, with what real volume?
2. For every event that IS in the sheet — is it firing the way the sheet says (same name, same properties), or has it drifted?
3. Which events are firing that have NO row in the sheet at all?

---

## Part A — Access and tools

Before starting, confirm you have:
1. **PostHog access** to project **66351, "Inc42 Datalabs | Live"** (EU cloud). **PostHog is already connected via MCP in this session — do not wait on a fresh OAuth link or re-authenticate.** Just invoke the `posthog:querying-posthog-data` skill (or the already-connected MCP tools directly) and confirm project 66351 is active. **Do not proceed past Part C without confirming this project is the active one** — this PostHog account has multiple INC42 projects and silently reverts to a different one mid-session; re-check before every query, not just once.
2. **Customer.io access** for the DataLabs workspace. There is no dedicated MCP for this — use browser automation (`claude-in-chrome` tools: load with `ToolSearch` query `"select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__find"`). If no logged-in session exists and credentials would be required, **stop and ask Ranjith to log in first** — never type a password yourself.
3. **Google Sheets access** to the sheet below — via browser automation, the same way. If you need to pull tab contents as data rather than screenshots, you can navigate directly to `https://docs.google.com/spreadsheets/d/1n6r5QXe-9Pq1uAWMKRe7zSgLHSejASzAq-BAqeI3L6Y/export?format=csv&gid=<gid>` for a given tab's gid (get gids by reading `.docs-sheet-tab` elements' click-through URL hash via `javascript_tool`, same method as pulling any other tab) — this downloads a real CSV you can then read with the `Read` tool, which is far more reliable than screen-scraping a spreadsheet UI.

---

## Part B — Read the source tabs (do this before querying anything)

Sheet: https://docs.google.com/spreadsheets/d/1n6r5QXe-9Pq1uAWMKRe7zSgLHSejASzAq-BAqeI3L6Y

1. Read tab **"Datalabs - Events"** in full (~40 rows). Extract every row into a structured list: category, event name, trigger, properties, destinations, remarks.
2. Read tab **"Datalabs - Events Properties"** in full (~820 rows) — the property dictionary. Pay particular attention to the **Lifecycle Envelope / Subscription / Billing** groups near the bottom — these belong to `pro_subscription`/`pro_billing`, covered in Part E.
3. From the Remarks column, three things are ALREADY CONFIRMED bugs — your job in Part D is to check whether they're STILL true today, not to rediscover them:
   - "Customise Columns Applied" is the intended name; production fires it as **"Customise Column Clicked."**
   - `Table Sort` fires an unrelated property ("Customise Column Properties") and, on the company-search table, sends `Table Name = company` instead of `company search`.
   - `onboarding_lifecycle`'s completion flag is 99% correct in PostHog but 66% broken in Customer.io (a sync issue, not a field-definition issue).
4. Note which rows are colored "Live Properties" vs "Backlog" vs other categories in the color legend at the bottom of the Events tab — a plain CSV export will NOT show this color, so read it from a live rendered view (screenshot or `read_page`) specifically for this step, not from the CSV.

---

## Part C — Query PostHog for the real event list

1. Confirm active project = 66351 (see Part A).
2. Run a query (via the `posthog:querying-posthog-data` skill, or the underlying HogQL query tool) equivalent to:
   ```sql
   SELECT event, count() AS volume, min(timestamp) AS first_seen
   FROM events
   WHERE timestamp > now() - INTERVAL 90 DAY
   GROUP BY event
   ORDER BY volume DESC
   ```
3. This is your real, ground-truth event list — every event name PostHog has actually received, whether or not it's in the sheet. Store the full result.
4. Filter out obvious PostHog-internal events (`$pageview`, `$autocapture`, `$identify`, etc. — these are platform-level, not DataLabs product events) unless the sheet specifically expects one of them.
5. For every event name that does NOT appear (or appears with unexpected volume) relative to your Part B list, run:
   ```sql
   SELECT properties FROM events WHERE event = '<event_name>' ORDER BY timestamp DESC LIMIT 10
   ```
   Record the actual property keys/values returned — do not infer them from the event name.
6. If querying `posthog:querying-posthog-data` or a related skill isn't yet loaded, load it now — don't attempt to hand-roll an API call without it.

---

## Part D — Get the real event list from Customer.io, then produce your two deliverable tabs

1. Using browser tools, open Customer.io, confirm the **DataLabs workspace** is active, and open Activity Log / Data Pipelines → Events.
2. Extract the distinct event list and any visible volume/date data using `get_page_text` or `read_page` — not a screenshot you eyeball, actual extracted text you can compare programmatically against Part B and Part C.
3. For unfamiliar events, click into an instance and extract the raw property payload the same way.
4. **Now produce two new tabs in the live Google Sheet** (via browser automation — duplicate the "Datalabs - Events" tab, rename it; create a new blank tab for the second one):

   **Tab 1 — "Datalabs Audit — [Agent Run Date]"**: the duplicated Events tab, with these columns added and filled for every existing row: `Live in PostHog? (Y/N + volume)`, `Live in Customer.io? (Y/N)`, `Actual Name if Different`, `Actual Properties`, `Classification`, `Recommendation`.

   **Tab 2 — "Datalabs — New Events Found"**: new tab, one row per event that appeared in Part C/D but has no corresponding row in the original sheet at all:

   | Event name (as seen live) | Platform (PostHog / Customer.io) | First seen | Volume (30 days) | Matches a sheet row? (N) | Actual properties captured | Classification | Recommendation |
   |---|---|---|---|---|---|---|---|

   Classification options: Confirmed correct / Renamed / Property mismatch / Broken-not firing / Dead-test event.
   Recommendation options: update sheet to match reality / fix production to match sheet's intended name-properties / needs product owner decision / no action.

---

## Part E — `pro_subscription` / `pro_billing`: OUT OF SCOPE for this audit

Do NOT investigate `pro_subscription` or `pro_billing` any further — no PostHog property checks, no Meta/Google Ads conversion checks, no Customer.io campaign trigger checks. This was originally in scope but has been descoped: these two events don't exist in Customer.io yet, so the ads-conversion risk they were meant to guard against isn't live either.

**In your Part F final report, state plainly: "`pro_subscription` and `pro_billing` are not covered by this audit — descoped."** Do not silently drop them; call this out explicitly so nobody mistakes their absence from your report for a clean pass.

---

## Part F — When you're done

Confirm, explicitly, in your final response:
- Both output tabs exist and are fully filled (not partially — every original row has a verdict).
- The explicit descope note from Part E: `pro_subscription`/`pro_billing` not covered.
- Any blockers you hit (missing login, missing tool access) and what you need to proceed if incomplete.

Do not describe this as "instructions reviewed" or "sheet read" — report actual completion state of the two tabs and the money-event check.
