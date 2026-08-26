# App v2 — experiments plan (27 Aug 2026)

This is the experiments layer sitting on top of the existing `inc42-app-v2-roadmap.xlsx` (item
#8: "PostHog feature flags + A/B testing infra"). That roadmap already commits to the
infrastructure; this file is the actual list of experiments to run on it, merging what Utkarsh
confirmed and what Ritvik separately proposed, so they don't get built as two disconnected plans.

**Gap flagged up front:** I found the Utkarsh-side confirmation only up to the point where it was
scheduled, not its outcome. The 26 Aug scoping call ends with "confirm one-card vs multi-card bet
with Utkarsh tomorrow" (i.e. today) — nothing from today is in Wispr Flow yet. If that
conversation already happened outside a recorded call, tell me what was decided and I'll update
the sequencing below.

---

## 1 · Experiments already confirmed (26 Aug sync, Ranjith + Ritvik)

Sequenced, not parallel:

1. **Brief card design** — two hero-card variants, A/B tested rather than locking one design as a
   single risky bet. Add 2–3 article thumbnails to the hero card so a brief reads as a curated
   list, not one article (directly answers Ravi Kumar's outside critique, "what is Brief?").
2. **Loader/completion animation** — with vs. without a personalized completion animation.
3. **Story strip above the brief** — with vs. without.

Explore page gets a **minimal** A/B only — standard layout, maybe a top-fold hero test — not a
full-section experiment. This is a deliberate scope-down: Explore's redesign logic (§ below) is
still being validated against real data, so it isn't ready for a full split test yet.

**New, not previously scoped:** an **in-app rating card** on brief completion — positive response
routes to the app store, negative routes to a feedback form. Doesn't exist today; needs to be
built, not just flagged behind a flag.

**Also decided:** onboarding copy moves to Customer.io's native virtual-tour feature, so future
copy edits skip app releases entirely — not an A/B test, but bundled into the same v2 push.

---

## 2 · Ritvik's own experiment — the company-data signaling hypothesis

This is the experiment behind the entire Explore-page logic in `inc42-explore-page-logic.md`, and
it's the "similar experiment discussed with Ritvik" — same shape as the Utkarsh brief-card bet,
just running on the Companies/Articles side instead of Brief:

- **Hypothesis:** letting each company's own data pick its card treatment (funding, hiring
  momentum, financials) reads as more "editorial and intelligence-driven" than the current flat
  list, and should lift engagement (Watchlist adds, taps per card type, scroll depth) without
  making the page feel random.
- **Current confidence: self-rated 30–40% baked.** Tested manually against only ~100 companies,
  against a real base of ~75,000.
- **Next step, matching the roadmap's Step 1:** ship the rules as a client-side, feature-flagged
  presentation layer only (2–3 weeks, no back-end work) — this is itself the first live
  experiment: does anyone tap these treated cards more than the plain ones today, on real traffic.
- **Before scaling it:** pull the full dataset via the paginated companies API (blocked on
  Prapti — ledger item P2), re-validate every threshold in the logic doc against the real base,
  then Ritvik + Ranjith + Utkarsh finalize together before Satya designs the next iteration.

---

## 3 · Where these two experiment tracks intersect

Both tracks share the same underlying infrastructure ask (#8 on the roadmap: PostHog feature
flags, fail-closed, proxied endpoint) and the same measurement discipline: don't ship a redesign
on belief, read it against the current version. Recommend running them as two flags under one
infra rollout, not two separate initiatives:

| | Brief-card track (Utkarsh) | Explore-signal track (Ritvik) |
|---|---|---|
| Status | Confirmed, sequenced, ready to build | Hypothesis stage, 30–40% baked |
| Scope | Full A/B on brief page | Presentation-layer flag only, no A/B yet |
| Blocked on | Nothing — can start now | Prapti's companies API (P2) + `signals_count` answer (P3) |
| Shared measurement | Completion rate, card-1→2 advance, session depth | Taps per card type, Watchlist adds, scroll depth |
| Owner | Ritvik builds, Ranjith confirms bet with Utkarsh | Ritvik + Ranjith, Utkarsh signs off before Satya designs |

---

## 4 · What's still missing from this plan

- Utkarsh's actual decision on the one-card vs multi-card bet (see gap flagged above).
- No confirmed sample-size or duration target for any of the three brief-page A/B tests — worth
  setting before they ship, so no one has to eyeball significance later.
- The Explore-page minimal A/B ("maybe top-fold hero only") isn't specified precisely enough to
  build from — needs one more decision on exactly what varies.
- Whether the in-app rating card's negative-feedback path routes anywhere actionable (a queue,
  a person) or just collects text with no owner.
