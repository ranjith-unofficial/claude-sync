---
name: project-inc42-app-feedback-rating-system
description: "Inc42 app feedback and rating system, locked 30 Aug 2026 into the Master PRD Copy — two decoupled systems, behaviour-gated native prompt, frequency caps, and the non-compliant plan it replaced"
metadata:
  node_type: memory
  type: project
---

Locked 2026-08-30 and written into the **Copy of Inc42 App Master PRD**
(`13vNB88le_0-mOGv3nueRJEQOUfrLVYIujBWLGAj6qow`), tab **"Feedback and rating: placement
plan"** (`?tab=t.qs6f8imv7h0n`, section 2), plus a new **section G** in `0.1 Decisions log`.
Extends the 28 Aug architecture in [[project-inc42-app-v2-satya-design-prompts]] with the
frequencies, triggers and interruption budget that were never specified.

## What the tab said before, and why it was wrong
The pre-existing "Inc42 rating prompt — placement plan" tab specified a custom
**"Enjoying Inc42? Rate us · Not now"** dialog fired before the native sheet. That is the
exact pattern Google Play forbids, so the plan sitting in the PRD would have failed review.
It also gated on "not a past reviewer", which is unimplementable: the native sheet returns
no callback, so we can only ever track that we *asked*. Both replaced. The old text is kept
below a "Superseded" marker in the same tab, per the document's archive rule.

## The locked design
**Two decoupled systems. They never fire in the same session and A never gates B.**

- **A. Feedback (ours, private).** A1 story-card "More like this / Less like this" (live
  today as the misnamed Rate heart, fires `brief_story_rated`, one user in eight days) ·
  A2 inline thumb on article and company detail · A3 brief-completion 1-5 survey ·
  A4 Profile "Send feedback" · A5 public replies to every store review ≤3★ ·
  A6 the WhatsApp/Tally screener (research recruitment, not a product surface).
- **B. Native store sheet.** No preamble, no redirect — the sheet renders in-app.
  Eligibility is **behavioural**, which is legal; a *question* is not.
  Gate: ≥3 completed briefs, ≥2 distinct active days, streak ≥3, ≥1 "More like this" and
  **0** "Less like this" in 7d, no error that session, no survey that session, no attempt
  in 120d. Triggers, highest wins: streak day 7 → 5th brief in rolling 14d → 3rd Watchlist
  save.

**Frequencies (the part that was missing):** passive surfaces unlimited; A3 first at the
5th completed brief then ≤1 per 45 days; B ≤1 attempt per 120 days (iOS OS-caps at 3/365),
so ~2 attempts per user per year maximum.

**Global interruption budget:** ≤1 modal ask per user per 14 days across app-update prompt,
notification permission re-ask, feedback survey and native review. Blocking update exempt.
Without this the four stack on the same reader.

## Two things to carry forward
- **Never link A to B.** Any build where a positive survey answer leads to the store
  recreates the banned gate. This is the single failure mode.
- **The prompt is unmeasurable by design.** Only `review_prompt_requested` against the Play
  Console rating delta proves anything.

## Still open (not locked)
1. Platform scope: 28 Aug said Android-only, App PRD v2 item 12 says both. iOS is live at
   build 40. Unreconciled.
2. Feedback surfaces A1–A4 are **not** in v2 scope — only the native prompt is, as item 12.
   Ranjith has not said whether they enter v2 or ship after.
3. Thresholds are chosen, not derived; nothing validates at the current user count.

**How to apply:** read the PRD tab before re-deriving any of this. Related:
[[project-inc42-app-story-card-redesign]] (the A1 UI fix),
[[project-inc42-app-v2-release]] (the 21 Aug scoping this supersedes on frequency),
[[reference-inc42-master-prd-skill]], [[reference-google-docs-html-clipboard-paste]].
