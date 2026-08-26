---
name: project-inc42-app-v2-sync-26aug
description: "26 Aug 2026 Ranjith-Rithvik (+Animesh) v2 scoping sync — funnel re-diagnosis, card/explore hypotheses, 5-page scope due 27 Aug, live bugs found, Satya comms breakdown, AskInc42 overlay placement, events-unification consultant hire"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5a4e3da5-0238-421a-9f45-64735b99f5d6
  modified: 2026-08-26T13:40:37.329Z
---

Recorded meeting, Ranjith (product) + Rithvik Sethi (eng/design), Animesh joined by phone near the end for deep-link testing (transcribed as "Aniways" — inferred match to team roster in [[project-inc42-launch]], not confirmed by name).

## Funnel data reconfirmed live
- Card1→Card2 drop ~50%; of those who drop, only 9% click "read full article", rest exit and don't return
- 75–80% of people who advance past card 1 complete the brief
- Median completion time 75s (skimming, not deep reading) — consistent with [[project-inc42-app-behaviour]]'s 78s finding
- Post-19 Aug open rate 48–77% flagged by both as too small a sample to trust yet
- Explore section: scroll depth very low, exploratory behaviour minimal

**Why:** this is a fresh re-read of the same behaviour data already in [[project-inc42-app-behaviour]] and [[project-inc42-app-ravi-critique]], used to re-derive card/explore design direction.
**How to apply:** treat as confirmation of existing findings, not new numbers — don't average with the 24 Aug review, which is a separate/uncertain dataset ([[project-inc42-posthog-review]]).

## Design decisions
- Single hero-card layout is a risky one-shot bet — agreed to A/B two card variants rather than lock one design
- Add 2-3 article thumbnails to the hero card so users understand a brief = curated list (echoes Ravi Kumar's "what is Brief?" critique)
- "Brief" as vocabulary flagged as unfamiliar to news readers; "story"/"quick read" floated, no decision
- Sector chips (Satya's in-progress card, e-commerce/fintech/pain-tech) confirmed must route to underlying article, not be decorative — same dead-click risk flagged in [[project-inc42-app-v2-scope-full]]
- Continue-where-you-left-off CTA: good-to-have, not priority (~10-15% of users affected)
- Tap-vs-scroll-to-advance re-litigated: Ranjith holds firm on tap, does not believe scroll affordance drives drop-off
- Explore redesign logic (Rithvik): signal-based cohorts instead of flat chronological list — articles by category, companies surfaced by 90-day headcount/revenue deltas as card hero, not static "latest"

## V2 scope plan — 5 pages, deadline 27 Aug 2026
Brief, Article Explore, Company Explore, Article Detail, Company Detail. Ranjith drafted 3/5 screens (Article Detail pending). Once locked: Satya designs, Rithvik builds, only on-the-fly tweaks allowed post-lock.

**Why:** repeated slippage on scope closure (see [[project-inc42-app-v2-scope-full]]'s "two unreconciled lists") — this sync was explicitly to force a hard deadline.
**How to apply:** treat 27 Aug as the real lock date for v2 design direction; anything not in this 5-page list is out of scope for this release.

## A/B test sequencing agreed
1. Card design (two hero variants)
2. Loader/completion animation (with/without personalized animation)
3. Story strip on brief page (with/without)
Explore page: standard layout, minimal A/B (maybe top-fold hero only). New: in-app rating card on brief completion (positive→store redirect, negative→more feedback — doesn't exist today). Onboarding copy moving to Customer.io's native virtual-tour feature so copy edits skip app releases.

## AskInc42 AI overlay — new placement
Proposed as lightweight overlay across Explore tabs (not a dedicated tab), feature-flagged. If backend-only, does NOT need a frontend app-update gate. Ranjith's estimate: 0.75-2 days own time. Next: share AI answer-quality test URLs with team, define error-handling UX. Links to [[project-inc42-askinc42]] and [[project-inc42-askinc42-next-week]].

## Events/analytics unification — deferred
Inconsistent event naming across products (e_mail/email/E-mail variants), no unification layer. Rithvik hiring an external analytics-events consultant (8 yrs experience) to decide on PostHog workspace consolidation and to push back on over-tooling (feature flags should be a simple backend API, not a heavyweight tool). Explicitly parked as "not yet started."

**Why:** this is the opening line of the meeting ("we are trying to unify events") — a new initiative not yet captured elsewhere.
**How to apply:** flag as a new thread distinct from [[project-inc42-analytics-stitching]] (which is about web/app ID stitching, not event-name unification) and from [[project-inc42-event-auditor]] (audit tool, not unification).

## Company-data signaling experiment
Rithvik's hypothesis tested on only ~100 companies manually vs. real base of ~75,000 — self-rated 30-40% baked. Next: pull full dataset via paginated API (Prapti to help), analyze DataLabs usage for real "signal" companies, then Rithvik+Ranjith+Utkarsh finalize before Satya designs.

## Live bugs found (in-call testing)
- Save/Rate race condition on story card: rapid Save→Rate taps silently drop the Save — needs action-locking
- Streak icon intermittently shows "–" instead of correct number on "already counted" screen — not consistently reproducible
- Asset load failure: "Build today's brief/Explore more stories" SVGs sometimes fail despite being lightweight — suspect bundling, not size
- Network timeout (~20s) intermittent in dev/Expo build, not reproduced on other phones simultaneously — inconclusive
- iOS back-button dead after 3-4+ card advances, TestFlight build 52 — reproduced live on 26th & 27th Aug briefs with Animesh; possibly fixed in build 54, unconfirmed
- Premature brief creation: hitting a future-date brief-id link before the 6am cron runs auto-creates that day's brief from a rolling 24h window — confirmed intended fallback, not a bug, but needs a check the 6am cron doesn't then double-create

**Why:** these surfaced by accident during live product testing, not from a formal QA pass — likely not yet in any bug tracker.
**How to apply:** verify these are filed/fixed before treating the v2 release scope in [[project-inc42-app-v2-scope-full]] as ready to ship.

## Team process issue — Satya (design)
Recurring uncommunicated design delays; Utkarsh asks Rithvik directly and he has no good answer to give. Root cause: no first-half/second-half structure anymore, fully async hours with minimal overlap, no standing sync (e.g. Satya WFH wasn't flagged in advance).

**Why:** Rithvik is being held accountable upward for delays outside his control; this is a recurring friction point, not a one-off.
**How to apply:** agreed fix — lightweight daily async Slack update (not a meeting), Rithvik+Ashish to set up. Agreed escalation path: Ranjith is the single point of contact for design direction on this workstream; informal Rithvik↔Satya syncs are fine for context-sharing but formal sign-off routes through Ranjith/Utkarsh. Relevant if Satya-owned deliverables (brief card, explore visuals, "Compass"/AskInc42 mockups) keep slipping.

## Deep-link test (with Animesh)
Confirmed `brief_date=YYYY-MM-DD` param controls which day's brief opens, always landing on that brief's first card (cannot deep-link into a specific card index). Verified working 26th & 27th Aug. Decision: tomorrow's notification uses the plain app-open link, not the direct-card deep link, until the iOS back-button bug is confirmed fixed. Relevant to [[project-inc42-deep-linking]].
