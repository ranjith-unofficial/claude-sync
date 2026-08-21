---
name: project-inc42-morning-tape
description: "Daily 7am IST cloud routine producing the Inc42 Morning Tape analytics brief across web, DataLabs and app — plus the HogQL method rules it must follow"
metadata: 
  node_type: memory
  type: project
  originSessionId: 72387b56-834c-4778-99ee-da11505342fe
  modified: 2026-08-21T08:44:56.901Z
---

**Inc42 Morning Tape** — daily one-screen analytics brief across the three properties, built 21 Aug 2026.

- Artifact (stable URL, republished in place daily): https://claude.ai/code/artifact/cada14d2-1af2-4dff-934e-95ee29809bad
- Routine: `trig_01TivYHQj3K7XSj2xA2JADxe` — https://claude.ai/code/routines/trig_01TivYHQj3K7XSj2xA2JADxe
- Cron `30 1 * * *` UTC = **7:00am IST daily**, model Opus 5, PostHog connector attached, no git repo.
- Local source of the first edition: `~/ClaudeDocs/inc42/morning-tape.html`

**Method rules baked into the routine prompt** (do not change without reason):
- Compare yesterday against the **mean of the prior 7 days**, never day-over-day — Sat/Sun run 30-40% below weekdays on all three properties.
- `uniq(person_id)`, never `distinct_id`. Uniques don't sum across days, so no weekly totals.
- App project (146258) is **UTC**; wrap with `toTimeZone(timestamp,'Asia/Kolkata')`. Web and DataLabs are already IST.
- Restore active project to 146258 as the last PostHog action — shared login, see [[reference-inc42-posthog-projects]].

**Two HogQL traps that produced published errors on day one:**
1. **Never use relative dates** (`today() - 1`) in these queries — it silently returned 19 Aug data while the day-grouped tables correctly returned 20 Aug, so a whole referrer narrative was off by one day. Use explicit `toDate('YYYY-MM-DD')`.
2. **`uniq(...) over a 7-day window ÷ 7` is not a daily average** — uniques dedupe across days, so it badly understates the baseline. Always group by day first, then average the daily values (the routine does this in Python, not by hand).

Also: mobile events arrive late. App counts drifted +1/+2 between two queries 30 min apart, ~14h after the day closed. A 7am run may slightly under-count the app.

Standing data-trust issues it re-checks each run — see [[project-inc42-funnel-analysis]] and [[project-inc42-posthog-review]] for context.
