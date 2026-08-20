---
name: feedback-analytics-depth
description: "How Ranjith wants analytics work done — report what users DID next, not where they stopped; and verify an absence before asserting it"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b2024af5-d7ba-4821-944c-c16a524e5e85
  modified: 2026-08-20T13:48:07.469Z
---

Two corrections he gave on 2026-08-20 while working through the Inc42 app behavioural analysis.

## 1. Positions are not insights — report the behaviour

His words, on being handed a card-by-card drop-off table: *"You are not giving me a meaningful data or insights. Because you said card 1, card 2 and everything but how many opened the card and then how people are reacting and if they are dropping in card 2 or 3, then are they going to read full article and that's where the flow breaks or they are simply exiting or how it is working."*

**A funnel table that says where people stopped is only half the work.** What he wants at every step:
- What was the **very next action** — did they advance, go backwards, expand something, tap through to another surface, or actually leave the app?
- Where a step diverts users out, **does the flow ever return?**
- Which exits are satisfied exits versus failures.

Doing this changed the conclusion completely: "22% die on card 1" became "only 10% of card-1 leavers actually exit the app; 21% move backwards inside it → it is a navigation problem, not disinterest," and "94% who open the full article never return to a card" became the single most actionable finding in the report. The mechanism was invisible in the position data.

**How to apply:** for any funnel, use event sequencing (`leadInFrame` over person+day in HogQL) to attach the next action to every step before presenting anything. Same instinct as [[feedback-strategic-report-structure]] — mechanism, not just numbers.

## 2. Verify an absence before asserting it

He pushed back on a claim I had put into an Asana ticket: *"Check in posthog before reporting this and let me know if there's any such error in posthog and confirm here."*

I had written "the app's `error_shown` event only records `load_failed` and `not_found`" based on PostHog's **taxonomy panel**, which only samples recent values. The full-history SQL showed **five** types including `http_500` — which made the ticket's real point stronger (the app *does* emit status codes, so a missing `http_403` is a gap, not an omission by design).

**Rules that follow:**
- PostHog's `read-data-schema` property-values list is a **sample, not the full set**. Confirm with `execute-sql` over full history before saying a value does not exist.
- A negative claim ("X is not captured / never happens") needs an unfiltered, all-time query — a cohort-filtered query cannot support it.
- Do not put an unverified claim into a shared system (Asana, a sheet, a doc) where a colleague will act on it. Verify first, then file.

He also caught two arithmetic/derivation errors in the same session (a 179 vs 188 user-count gap that turned out to be a real 5% `app_installed` under-fire, and a bogus "86% same story" result caused by comparing empty `story_id` strings across surfaces). **He checks the numbers. Show the working and state the limits.** See [[feedback-validation-approach]] and [[project-inc42-app-behaviour]].
