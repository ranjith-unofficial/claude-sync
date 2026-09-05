---
name: project-inc42-brief-entry-round2-15-uis
description: Brief entry screen round 2 (5 Sep 2026, late night) — fifteen structurally different UIs on the Referencing page of the draft Figma file, built on real days with real reader counts from PostHog; unreviewed
metadata:
  type: project
---

**Built 5 Sep 2026 (23:30–23:55 IST)** on page **"Referencing" (476:2)** of draft file
`dAsaTgNj0xh25w2OGaurZo`, below round 1. Header note at y=2760 (node 528:2); three rows of five
screens at y=3000 / 4400 / 5800, x=100…2100 step 500; a note under every screen (y+880).

**Why:** Ranjith rejected round 1 (A1–D1 + B2–B5) as "majority of the screen has the same UI
setup … try with 15 different types of UI … think of from marketing … this many are reading
currently, these many have completed … create a FOMO … don't maintain the header 'Monday, 8 June,
Morning Ranjith' … ensure the brand colour remains same."

**The fifteen (one mechanic each, no shared header/card):**
01 Live readers (dark, 3 Sep) · 02 Scoreboard opened/finished (4 Sep) · 03 Most read ranked top-3
with veiled 4–5 (13 Aug) · 04 Sealed envelope, zero headlines (10 Jul) · 05 Money tape, sum of
headline figures (8 Jun) · 06 Logo wall (6 Aug) · 07 Newsroom chat, 3 headlines sent (15 Jul) ·
08 Results board with ▲/▼ (29 Jul) · 09 Streak calendar, Day 12 (24 Aug) · 10 Poster, 46px
headline on red + giant "+7" (22 Jul) · 11 Hand of face-down stories (16 Jun) · 12 You vs everyone
split with counts (19 Aug) · 13 Notification stack, lock-screen 7:00 (25 Aug) · 14 One question
quiz gate (3 Sep) · 15 Twenty-four-hour timeline (12 Jun brief).

**Real numbers used (PostHog, pulled 5 Sep):** inc42.com readers per story via `$pageview`
`$pathname` in project 53557 — 3 Sep: slice 982, RentoMojo 451, Cradlewise 344, BYJU'S 259,
BookMyShow 184, Ultrahuman 166; 13 Aug: Infra.Market 406, Shiprocket 375, Zetwerk 264, Navi 197;
19 Aug: Shiprocket–500 Global 1,497, Cashfree 525, Navi 494, Veeba 357. `/buzz/` readers/day
≈ 25–36K. App (146258), 5 Sep: 113 `brief_page_opened`, 74 `brief_opened`, 36 `brief_completed`;
opens peak 8–10 AM at ~5 users/hour. **In-app counts are too small to display** — screens 02, 09,
12 carry a display threshold in their notes; website counts are the honest social proof today.
URL paths appear twice with `%E2%82%B9` vs `%e2%82%b9` (case) — sum both when counting a story.

**Rules applied from earlier rounds:** every story gets a reason label; no "cards" word; no
publish count; no countdown as lead; poster layout only when impact ≥0.70 with ≥0.10 gap (57% of
weekdays); money tape only with ≥3 headline figures; results board only with ≥3 Financials;
question only when lead has figure + company (~45% of days).

**Status:** unreviewed. Screens 04 and 14 were the two that needed collision fixes after
screenshot; 10 and 15 had one-line overflows fixed. Build pattern: one `use_figma` call per
screen with an inline helper (T/R/E/Fr/SB/NAV/CTA/NOTE), Fraunces + Inter + JetBrains Mono.
Related: [[project-inc42-brief-entry-referencing-page]], [[feedback-design-review-ranjith]],
[[reference-figma-mcp-build-techniques]], [[feedback-ui-mockup-research-first]].
