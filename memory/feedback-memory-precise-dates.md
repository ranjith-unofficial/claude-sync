---
name: feedback-memory-precise-dates
description: "Every meeting/review-derived memory must carry a verified, unambiguous date in its own body (not just an approximate one in metadata), and must be cross-linked when it might describe the same event as another memory — prevents split records like the 17-vs-20-Aug PostHog review confusion"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 59cedaa8-a793-4cf6-9ab8-edd7339fa0a4
  modified: 2026-08-24T17:38:40.260Z
---

Give every meeting- or review-derived memory a **precise, sourced date in the body text itself**, not only an approximate one folded into the description (e.g. "~20 Aug 2026"). When a later memory references the same real-world event under a different date or name, flag the mismatch explicitly in both files rather than letting two records of one event drift apart silently.

**Why:** `project-inc42-posthog-review.md` recorded Utkarsh's PostHog review as "~20 Aug 2026" from an approximate guess. `project-inc42-app-behaviour.md` separately cited a "17 Aug PostHog review" three times with specific numbers, never cross-linked to the other file. Ranjith caught the connection ("don't you remember this one?") that I'd missed — two memories were quietly describing what looks like the same event, under different dates, and I nearly answered a question about "Utkarsh's fixes" without noticing they might be the same list already partly known to be wrong (three of its cited numbers turned out to be measurement artifacts).

**How to apply:**
- When writing a memory sourced from a specific call/review, state the date as verified fact if known, or explicitly flag it as unconfirmed/approximate if not — never let an approximation silently read as fact later.
- Before creating a new memory about a meeting/review, grep existing memory for the same reviewer + same subject matter, not just the same date — a review can get recorded twice under different labels if the date is fuzzy.
- If two memories may describe the same event, add an explicit `[[...]]` cross-link and a short reconciliation note in both, rather than merging blind or leaving them to drift.
- This applies broadly, not just to PostHog reviews — any recurring or informally-dated source (Slack threads, verbal reviews, "the doc someone shared") is at the same risk.
