---
name: project-inc42-app-live-feature-status
description: "What is actually live in the Inc42 app vs what the v1 PRD merely specifies — confirmed feature by feature with Ranjith on 30 Aug 2026, including the Decode/30 sec summary naming"
metadata:
  node_type: memory
  type: project
---

Confirmed with Ranjith 2026-08-30, while building the "What the app does today" table at the top of `App PRD (current)` in the Master PRD doc (`13vNB88le_0-mOGv3nueRJEQOUfrLVYIujBWLGAj6qow`).

## The naming correction
The feature specced as **"Decode" ships as the "30 sec summary"**. Decode was an internal document name that never left the doc. **Use "30 sec summary"; never Decode.** 77 occurrences were replaced across the document on 30 Aug (match-case, so the lowercase `decode` event name survived).

## Confirmed live
30 sec summary · brief completion screen (v2 item 6 improves it, it is not broken) · sector landing page · onboarding · first-open walkthrough · sign-in bottom sheet · brief cover and cards · ranking and personalisation · streaks · daily edition line · Explore Articles and Companies · Watchlist · company profile · article reader · account and profile · notification permission prompt · account deletion · deep links (fixed since v2 scoping) · AskInc42 v1.

## Confirmed NOT in the app
**Monetization gates** — specced as dormant and Apple-safe in §8.6, not built. **Dark mode, sector images, app-update prompt, store review prompt, heatmaps, Pulse** — all v2 or backlog.

## The "Rate" control is the like and dislike
Confirmed 30 Aug. The v1 PRD's "Rate" control on brief cards is the **thumbs up and down shown when a story is opened**. It is **live**, and it fires `brief_story_rated`. Nobody calls it a rate control, which is why it briefly got deleted from the inventory as a feature that "does not exist". Usage is tiny: one user in eight days.

## Still open
**Push delivery.** Not delivering despite opt-ins; root cause believed known on iOS. Confirm dead vs misconfigured before scoping the fix.

**Why this memory exists:** I built that table by reading the specification, and the spec describes things that were never made. Ranjith's response was *"there are a lot of such things."* Two of my rows were wrong in opposite directions — I called two live features missing because I did not recognise the names this document uses for them: the 30 sec summary (written as "Decode") and the like/dislike on a story (written as the "Rate" control).

**How to apply:** never infer from a spec that a feature exists, and never infer from an unfamiliar name or a zero-fire event that it does not. Ask what the team calls it and whether it is in the build. See [[reference-inc42-master-prd-update-rules]].
