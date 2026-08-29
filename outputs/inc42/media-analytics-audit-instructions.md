# Inc42 Media (Website) Analytics Audit — Execute This Now

## READ THIS BEFORE ANYTHING ELSE

This is a task to execute immediately using your tools. It is not a document to edit, reformat, review, or summarize back.

**Your deliverable is real data**, produced by actually querying PostHog and Customer.io — not by reading this file and describing what you would do.

### DO
- Actually run PostHog queries against project 53557 and get real event names, real volumes, real property payloads.
- Actually read the existing event-auditor findings (Ranjith has them — ask if you don't) before doing manual work that tool already did.
- Actually open the Google Sheet tabs named below and read every row.
- Actually check Customer.io's live event data, using browser tools if no direct API/MCP access exists.
- Write your findings into the two new Sheet tabs specified in Part D — that is the finished deliverable.
- If you hit a login wall or missing tool access, stop and say exactly what's blocked, then wait. Do not proceed on guesses.

### DO NOT
- Do NOT edit, rewrite, restructure, or "clean up" this instructions file. It is reference material for you to follow, not your output.
- Do NOT respond with a plan, an outline, or a description of the steps you're about to take instead of taking them.
- Do NOT infer or guess what PostHog/Customer.io are receiving based on what the sheet's Destinations column claims — it's already known to be stale (see Part B2).
- Do NOT report "I've reviewed the sheet and instructions" as if that were progress. Progress is filled rows in the output tabs (Part D).
- Do NOT fabricate volumes, property names, or "typical" payloads. If you can't query it, say so.
- If your first instinct after reading this is to touch `media-analytics-audit-instructions.md` itself, that is the wrong action — stop and re-read this section.

**The three questions this task exists to answer, and nothing less than this counts as done:**
1. How many events does PostHog/Customer.io actually show for inc42.com, and what are they, with what real volume?
2. For every event that IS in the sheet — is it firing the way the sheet says (same name, same properties, same destinations), or has it drifted?
3. Which events are firing that have NO row in the sheet at all?

---

## Part A — Access and tools

1. **PostHog access** to project **53557, "Inc42 | Live"** (EU cloud). If not authenticated, run the PostHog authentication tool (`mcp__plugin_posthog_posthog__authenticate`) or invoke the `posthog:querying-posthog-data` skill. **Confirm this project is active before every query** — this account has multiple INC42 projects and silently reverts mid-session.
2. **Customer.io access** for the website workspace. No dedicated MCP — use browser automation (`ToolSearch` query `"select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__find"`). If a logged-in session doesn't already exist, stop and ask Ranjith to log in first — never type a password yourself.
3. **The existing event-auditor findings.** A Playwright-based tool already ran 6 scripted browser journeys against inc42.com and produced `~/ClaudeDocs/inc42/event-auditor/runs/<latest>/report.html` and `findings.json`. Read this file directly (`Read` tool) before doing any manual PostHog/CIO work — do not re-derive what it already answered:
   - Only 5 of 63 planned events properly implemented; 24 partial, 32 missing.
   - GA4 receives MORE distinct event types than PostHog on identical journeys (autocapture is off).
   - Customer.io receives only page-view calls, zero `track()` calls.
   - Specific "not tested" events have documented reasons (e.g. the freewall/register-gate never rendered during the test runs) — read these before assuming those events are simply broken.
   Your manual work should (a) confirm these are still true today and (b) find events outside the 6 scripted journeys (paid flows, logged-in-only pages, forms).
4. **Google Sheet access** to the sheet below. Pull tab contents as real data via the CSV export trick — navigate to `https://docs.google.com/spreadsheets/d/1n6r5QXe-9Pq1uAWMKRe7zSgLHSejASzAq-BAqeI3L6Y/export?format=csv&gid=<gid>` for a given tab (get each tab's gid by reading `.docs-sheet-tab` click-through URL hashes via `javascript_tool`) — then read the downloaded CSV with the `Read` tool. Do not screen-scrape a rendered spreadsheet when a real CSV is one navigation away.

---

## Part B — Read the source tabs

Sheet: https://docs.google.com/spreadsheets/d/1n6r5QXe-9Pq1uAWMKRe7zSgLHSejASzAq-BAqeI3L6Y

1. Read tab **"Inc42 - Media - Events"** in full (~30 rows): Event Name, Triggers, Trigger Type, Event Property Groups, Custom Event Properties, Triggers Identify Call?, Definition, Destinations.
2. Read tab **"Inc42 - Media - Events Properties"** in full — the property/sample-value dictionary.
3. **Already-confirmed issues — verify current state, do not rediscover as new findings:**
   - Destinations column lists GA4/Mixpanel/MoEngage/Amplitude/Meta Ads on nearly every row. MoEngage is removed from the real stack (stubbed SDK); Mixpanel/Amplitude were never real. PostHog and Customer.io are the tools actually live on the site, yet PostHog appears as a destination on exactly 1 of ~30 rows ("Login Modal").
   - "Newsletter Subscribed" and a row literally named "s" have identical trigger/properties/destinations — likely an accidental duplicate.
   - "Scroll Depth (Paused)" lists GA4 only, nothing to PostHog — the event-auditor found three separate scroll-depth implementations on the live site, none reaching PostHog.
   - A prior check found `distinct_id` stays an anonymous UUID even for fully signed-in users (WordPress + Auth0 cookies present) — if still true, every "per-user" PostHog number for logged-in behavior is unreliable.
   - "Plus Lock" was previously found firing ~22×/session to GA4 and 0× to PostHog.

---

## Part C — Query PostHog and Customer.io for the real event list

1. Confirm active PostHog project = 53557.
2. Run:
   ```sql
   SELECT event, count() AS volume, min(timestamp) AS first_seen
   FROM events
   WHERE timestamp > now() - INTERVAL 90 DAY
   GROUP BY event
   ORDER BY volume DESC
   ```
   via the `posthog:querying-posthog-data` skill. This is your real event list. Filter out PostHog-internal events (`$pageview`, `$autocapture`, etc.) unless the sheet expects one.
3. For anything unmatched against Part B, or with an unexpected volume, run:
   ```sql
   SELECT properties FROM events WHERE event = '<event_name>' ORDER BY timestamp DESC LIMIT 10
   ```
   and record the actual property keys/values.
4. Using browser tools, open Customer.io's website workspace → Activity Log / Data Pipelines → Events. Extract the distinct event list and any visible counts via `get_page_text`/`read_page`. Click into unfamiliar events for raw payloads the same way.

---

## Part D — Produce your two deliverable tabs

Using browser automation on the live Google Sheet:

**Tab 1 — "Media Audit — [Agent Run Date]"**: duplicate of "Inc42 - Media - Events," with columns added and filled for every existing row: `Live in PostHog? (Y/N + volume)`, `Live in Customer.io? (Y/N)`, `Actual Name if Different`, `Actual Properties`, `Classification`, `Recommendation`.

**Tab 2 — "Media — New Events Found"**: new tab, one row per event with no corresponding sheet row at all:

| Event name (as seen live) | Platform (PostHog / Customer.io) | First seen | Volume (30 days) | Matches a sheet row? (N) | Actual properties captured | Classification | Recommendation |
|---|---|---|---|---|---|---|---|

Classification options: Confirmed correct / Renamed / Property mismatch / Broken-not firing / Dead-test event.
Recommendation options: update sheet to match reality / fix production / needs product owner decision / no action.

---

## Part E — Priority checks (do these even before finishing the general sweep)

1. **Dead-vendor check.** Using browser tools, check inc42.com's live page source and GTM container for any non-commented-out script referencing MoEngage, Mixpanel, or Amplitude. A text match on a commented-out script is a false positive — confirm it's not inside `<!-- -->` or `//`. If any is genuinely still live, report immediately as a standalone finding.
2. **Identify-call check.** If you can access an authenticated session (or ask Ranjith to provide one), check whether PostHog's `distinct_id` for that session is the anonymous UUID or tied to the account. Report as a standalone finding either way — this affects how every other number in this audit should be interpreted.
3. **Scroll-depth reconciliation.** Confirm from PostHog query results whether any scroll-depth event reaches PostHog at all. If not, flag this as priority — restoring it is a locked company strategy item, not a routine gap.
4. **Duplicate "Newsletter Subscribed"/"s" rows** — confirm and note for sheet cleanup (low priority, log it, don't spend more time than that).

---

## Part F — When you're done

Confirm, explicitly, in your final response:
- Both output tabs exist and are fully filled.
- Results of the three Part E priority checks, stated plainly.
- Any blockers hit and what's needed to proceed if incomplete.

Do not describe this as "instructions reviewed" or "sheet read." Report actual completion state of the two tabs and the priority checks.
