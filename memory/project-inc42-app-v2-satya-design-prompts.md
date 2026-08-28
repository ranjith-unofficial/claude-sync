---
name: project-inc42-app-v2-satya-design-prompts
description: "Three detailed design prompts written for Satya (28 Aug 2026) — brief-completion gratification screen, rating flow, welcome screen — plus the verified Play/App Store review-prompt policy finding"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2cd616ce-c26c-47d0-b3e4-38edf280ada5
  modified: 2026-08-28T13:20:27.506Z
---

Built 2026-08-28, after the 28 Aug Team Catch-up call ([[project-inc42-app-v2-sync-26aug]] is the prior sync; this is the same-day follow-up where Ranjith asked for Satya-ready design briefs on 3 screens). Ranjith's instruction: give product clarity/psychology/data, not design principles — Satya already knows those.

## 1. Brief-completion gratification screen
Problem: value promise is "an authority cut the noise for you," but the payoff screen repeats the identical message every day, so it stops landing by day 4-5. Confirmed scope: **full 5-variant rotating system** (not the leaner 2-variant option offered), cycled deterministically (day-of-week or session-count, not random):
1. Time/effort — uses real `session_duration_sec` (median is 78s, see [[project-inc42-app-behaviour]])
2. Curation/authority — "N stories, handpicked by the newsroom" — directly answers Ravi Kumar's finding that the app never states it's personalized ([[project-inc42-app-ravi-critique]])
3. Identity/status — reuses the existing streak hero as-is; streak reward hierarchy is deliberately identity-based not extrinsic-reward-based ([[project-inc42-content-personalization]])
4. Personal relevance — "N stories were in [your sector]" — **needs a fallback to mode 1/2 on days with zero matches**, since 86% of articles have no sector tag ([[project-inc42-content-personalization]])
5. Cumulative/weekly — streak count × per-brief time estimate

Modifies the existing brief-end sequence (streak hero → "Explore Trending Stories" carousel → "EXPLORE MORE" pill, confirmed via Figma in [[project-inc42-app-structure]]) — not a rebuild. Ritvik needs the named data fields (`session_duration_sec`, `card_count`, `matched_sector_count`, `streak_count`) to wire it; hand-off must be templated copy with variable slots, not static strings.

## 2. Rating flow — the compliance finding
🔴 Ranjith's original ask (ask 1-5 → route 4-5★ to store, ≤3★ to feedback) is a **documented policy violation on both platforms**, verified live 2026-08-28:
- **Google**: `developer.android.com/guide/playcore/in-app-review` — "Your app shouldn't ask the user any questions before or while presenting the rating button or card... including questions about their opinion." Confirms the same restriction already flagged in [[project-inc42-app-v2-release]]'s ratings section (21-23 Aug scoping).
- **Apple**: no single explicit line, but functionally identical — HIG: "Don't use buttons or other controls to request feedback," `SKStoreReviewController` caps at 3 prompts/365 days with no result callback, and guidance is to time the trigger to a behavioral moment, not a preceding question.

**Locked design (confirmed by Ranjith):** split into two decoupled surfaces, not one branching flow.
- **A. Custom satisfaction/feedback survey** (no policy issue since it never gates the native prompt) — "How was today's brief?" 1-5, shown at brief completion (the 78s mark), never after a full-article webview exit (94% never return, per [[project-inc42-app-behaviour]]). 4-5★ → thank-you (optional share prompt, not a store redirect). ≤3★ → 1 qualifying multiple-choice question ("What wasn't right? Content not relevant / Repeated stories / App slow or buggy / Hard to navigate / Other" — Ranjith confirmed keeping these generic categories, no existing taxonomy to reuse) then an open text box.
- **B. Native store review prompt** — separate trigger, behavior-gated only (≥3 completed briefs, no crash that session, ≥2 sessions), Android-only for now. No preceding screen, no question. Matches the compliant pattern already proposed in [[project-inc42-app-v2-release]]'s ratings section.

## 3. Welcome/onboarding screen
Problem: current screen is a static screenshot of the brief page — shows what the product looks like, not why to trust it. Same gap as Ravi Kumar's "app never states it's personalized" finding.
- Needs explicit value-prop copy: noise across many sources → one editorially-filtered brief.
- Needs a **verified** authority/credibility stat from Ranjith/marketing — explicitly told Satya not to invent a number here.
- Visual should show the noise→signal transformation (scattered sources converging into one card), not just a screenshot of the destination UI.
- Stretch idea (flagged open, not committed): pull a real/templated teaser of *today's* actual top story instead of a static mock, for the same freshness reason as screen 1's fatigue problem — only if it doesn't block the Sunday design-lock deadline.
- Coordinate language with the separate homepage-banner redesign (also explaining "what is brief," a returning-user surface — see Thread 1 #2 of [[project-inc42-app-v2-scope-full]]) so the two don't diverge.

## Process note
Mid-task, Ranjith corrected the approach: several scope-changing judgment calls (rotation count, the rating-flow architecture split, feedback category wording) had been decided unilaterally rather than confirmed. Instruction: **ask before finalizing a deliverable when a judgment call changes scope**, not just when a fact is uncertain — folded into [[feedback-ask-before-assuming]].

**Next step, not yet done:** Ranjith wants these three screens (plus data-field dependencies) broken into Asana tasks under the V2 parent task.
