---
name: project-inc42-posthog-review
description: "Utkarsh's PostHog review, CONFIRMED 2026-08-17 — full document found at ~/Downloads/Posthog Review 2026 08 17.md. Instrumentation audit (dark/off-spec events, property gaps, internal-user pollution, north-star redefinition) that directly fed Ranjith's 19 Aug v2 Scope doc"
metadata:
  node_type: memory
  type: project
  originSessionId: 878d7ed0-3fa4-4ffb-81e5-9a0f6d5bff08
  modified: 2026-08-25T03:52:26.441Z
---

✅ **RESOLVED 2026-08-25** — the date-ambiguity flag this file carried earlier is closed.
Found the actual document on disk: **`~/Downloads/Posthog Review 2026 08 17.md`**
("Inc42 App — PostHog Review, First Real-User Week (Aug 12–17)", dated **2026-08-17**,
project PostHog `Inc42 App` 146258 eu.posthog.com). This IS the same review
[[project-inc42-app-behaviour]] cited as the "17 Aug PostHog review" — confirmed by exact
number matches: Explore-beats-Brief 69% vs 31%, 7-second median completion, 41%
cover→brief entry (n=131 fresh installers, Aug 12–17; the 20 Aug app-behaviour deep-dive
later found some of these were partly measurement artifacts on a larger, cleaner cohort —
see that memory for the correction, not a reason to doubt this review's own methodology).

**Read the file directly for full detail — don't rely on memory paraphrase for exact
numbers.** Structure: §0 headline · §1 instrumentation audit (dark events, off-spec events,
property gaps, no internal-user exclusion, auth anomaly) · §2 activation funnel + completion
quality + retention + push + engagement depth data · §3 old-dashboard verdicts · §4 proposed
single dashboard (BUILT, PostHog dashboard 901039) · §5 ranked action list.

**Top-line findings:**
- **Push is entirely dark**: `push_delivered` has never fired, `push_opened` fired twice ever (both Jul 10) despite 67% opt-in grant. Highest-impact, zero-product-work fix if the Customer.io integration is actually finished — find out why it's dark.
- **`decode` (the AI explainer, the core product positioning) has ZERO telemetry** — verify whether it's unshipped or shipped-uninstrumented.
- **Cover→brief is the biggest funnel cliff**: 99 saw the cover, 41 tapped in (41%).
- **Explore beats Brief**: 69% vs 31% of fresh installers — inverted from the product thesis.
- **North-star flatters**: 41% nominal completion meets the PRD bar, but median duration is 7s — recommends redefining the north star as `completed_engaged` (≥60s).
- **No internal-user exclusion exists anywhere** — 34 of 168 "active" users are pre-Aug-12 beta/internal people with no property/cohort to filter them out.
- Full ranked action list (§5): turn on the morning push · fix Summit deep-link attribution before 19 Aug · fix the cover cliff · ship the watchlist onboarding step · adopt engaged-completion as north star · the instrumentation punch-list (this is what became the Asana events-fix ticket, 25 Aug) · watch whether Explore still wins once the cliff is fixed.

**This review is the stated source input for [[project-inc42-app-v2-scope-full]]'s Thread
10** (`~/Downloads/Inc42 App v2 Scope.md`, Ranjith's own 19 Aug scope doc, item #1 "Updated
events" is a direct synthesis of this review's §1).

**How to apply:** before quoting any PostHog number for the app, check whether internal
users are excluded (they aren't, by default, as of this review). Read the actual file for
exact figures rather than reconstructing from memory. Related:
[[reference-inc42-vendor-stack]], [[project-inc42-app-acquisition]], [[project-inc42-launch]],
[[project-inc42-app-behaviour]], [[project-inc42-app-v2-scope-full]].
