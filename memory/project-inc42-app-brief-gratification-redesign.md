---
name: project-inc42-app-brief-gratification-redesign
description: "Brief page redesign concept from 3 Wispr calls (26-27 Aug 2026) — Brief→Gratification→Explore as separated beats, screen-by-screen spec, and two unresolved conflicts with existing locked scope"
metadata: 
  node_type: memory
  type: project
  originSessionId: 43f2af93-d997-425d-ace1-dc28c1bcdd2e
  modified: 2026-08-29T07:47:36.147Z
---

Source: 3 Wispr Flow recordings — **"Optimizing Wispr Brief Design"** (27 Aug 2026, 07:53-08:11 IST, meeting id `1f7caee8-771c-4b9f-b523-21c6e0f0c018`), **"Brief Card Design Refresh"** (26 Aug, `b83ed5f9-51b0-4cac-9dd9-4b604261f7da`), **"Improving Brief Page Conversion"** (26 Aug, `669e5f6a-29ea-451e-8ced-655fdc2d5b65`). Drafted into a Slack message for Satya + Rithvik. Supplements [[project-inc42-app-v2-scope-full]] and [[project-inc42-app-v2-sync-26aug]] with more concrete, screen-level detail from the actual transcripts (not just meeting-notes summaries).

## The core concept
"We've been solving the packaging, not the gift." Showing articles inside the brief itself creates a contradiction — user finishes and can't tell if they read enough or should read more. Fix: split the experience into three explicit, separated beats — **Brief → Gratification → Explore** — don't blur gratification into the explore-more content the way today's build does.

## Screen-by-screen

**Home / Brief entry**
- Card should preview 2-3 articles, not 1 (A/B vs today's single-card) — signals "curated list," not one story. This is what Satya's in-progress card already solves for.
- Header (date/greeting) currently too visually dominant over brief content — needs a more refined pass.
- Calendar/past-briefs: don't remove outright — collapse behind a small "past briefs" pill button, only expand on tap. Validate real usage before cutting it.
- Sector chips (e.g. e-commerce/fintech/pain-tech row) must route to the actual article/topic, not be decorative — confirmed dead-click risk.
- "Brief" as a word may not land with news readers — "story"/"quick read" floated, not decided. **Resolved 27-29 Aug in the Explore-tab design-direction thread** — see [[project-inc42-explore-articles-companies-design]]: keep "Brief" (Quartz Daily Brief precedent), fix via a segmented Instagram/Snapchat-style progress bar instead of a rename; "Story" would collide with Inc42's own tag vocabulary.

**Inside the brief (story cards)**
- Tap to advance, not scroll — final.
- Progress indicator ("4/8, tap for next") — build this.
- Real fix needed only at card 1→2 (45-50% drop) — no fatigue curve past card 2, don't spread effort across all cards.
- Longer-term: brief content should read as distilled data/stats with a tappable source tag (article vs Data Labs), not article-style previews.
- "Read full article" stays (only 9% use it, fine at low prominence) — needs a return path back into the brief, not removal.

**Completion / "thank you" / gratification screen**
- Must be its own beat: tell the user plainly "we collated this so you didn't have to" (the time-saved payoff) before showing anything else.
- Today's flow (streak animation → straight into "Explore Trending Stories") blurs gratification and explore-more together — root cause of the "was that enough?" feeling. Separate them.
- **Fleshed out further same day (28 Aug) in a separate session** — see [[project-inc42-app-v2-satya-design-prompts]]: a full 5-variant rotating gratification message system (time/effort, curation/authority, identity/streak, personal relevance, cumulative/weekly), cycled deterministically so the payoff doesn't go stale by day 4-5.

**After gratification — explore surface**
- Sector-based "more this week" for followed sectors; fallback to ranking-driven "more relevant to you" if nothing fresh there.
- Longer-term, not this build: tighter company↔article↔Data Labs interlinking — e.g. a comparison table (Uber vs Ola vs Rapido) prompted from a company page, starting on the Data Labs website first.

**Rating** — no new info at the time this was drafted; flagged as an open conflict between [[project-inc42-app-v2-release]] (Play policy bans the sentiment-gate) and [[project-inc42-app-v2-sync-26aug]] (26 Aug sync logged the sentiment-gate version as a planned A/B test). **Since resolved same day (28 Aug) in a separate session** — see [[project-inc42-app-v2-satya-design-prompts]]: locked as two decoupled surfaces (custom satisfaction survey, never gates the native prompt; separate behavior-gated native store prompt, Android-only). Verified against both Play and Apple policy text, not just Play as this memory originally flagged.

## ⚠️ Two conflicts this surfaced — flag before citing either as final

1. **Calendar/banner supersession.** [[project-inc42-app-v2-scope-full]] Thread 1 #2 (24 Aug Weekly App Review) said "replace calendar/greeting block with banner inventory." The 27 Aug morning call instead decided: keep main card + past-brief in the current build, just collapse the calendar behind a pill button and validate usage data before cutting it. **Treat the 27 Aug version as current** — it's more recent — but this hasn't been reconciled back into the Thread 1 tracking sheet.
2. **Engagement metric conflict.** The 27 Aug call says completion should NOT be the primary engagement metric — track overall engagement (clicks/user, currently ~7, target 9-10) instead. This is a different north star than `completed_engaged` (brief completed AND duration ≥60s), which is the metric already locked in the 25 Aug events-fix Asana ticket (see [[project-inc42-app-v2-scope-full]] Thread 6). Nobody has explicitly reconciled these — needs a decision before reporting against either.

## Process note (from 27 Aug "Team Catch-up", `0210d748-490c-4662-abb9-b687ad7ef822`)
Utkarsh's feedback on the brief card has stayed subjective ("not impactful") without structural specifics, which is what's blocking Satya from proceeding. Ranjith's action: give Satya concrete data-point direction per company bucket (IPO/funded/early-stage) via Prapti, then push Utkarsh for approval citing the dev block. This Slack message (this memory) is meant to be that concrete, structural brief.

## Status
Only **2-3 article preview cards** and the **progress indicator** are confirmed for the current build. Everything under "gratification screen" and "explore surface" is direction for a later build, not this release.

**Why:** this is the first time the "what is Brief, really" problem got a concrete screen-by-screen answer instead of vague "make it more impactful" feedback — directly unblocks the Satya/Utkarsh stalemate.

**How to apply:** when asked about Brief-page design direction, lead with this (most recent, most concrete) over the 20 Aug Satya sessions or the 24 Aug Weekly Review scope — but surface the two conflicts above rather than silently picking a side.
