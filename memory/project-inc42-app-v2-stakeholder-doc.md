---
name: project-inc42-app-v2-stakeholder-doc
description: "The authored, stakeholder-facing INC42 app v2 scope document (Google Doc V2 - Final tab + artifact) — 15-item scope as of 29 Aug 2026, includes several product decisions made directly during authoring that aren't captured anywhere else"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9108f882-accb-498a-b781-8d81145ba85e
  modified: 2026-08-29T07:42:21.386Z
---

Built 28–29 Aug 2026 as a stakeholder-readable version of the app v2 scope, going through several rounds of correction. This is a different artifact from [[project-inc42-app-v2-scope-full]] (which reconciles scattered meeting threads) — this one is the actual authored document, with Ranjith's own decisions layered on top during writing.

**Locations:**
- Google Doc: "Inc42 App Master PRD" → tab "V2 - Final" (`docs.google.com/document/d/1eT472QdzWOg_ChvvmoO3cX5CnL2sqToR5jU8-GvMxzw`)
- Artifact (same content, published version): `https://claude.ai/code/artifact/00608a57-4661-47b9-9071-27cd21c1cd46`

**Current scope, 15 items in journey order:** Walkthrough → Welcome screen → Brief card → Resuming an unfinished brief → Full-article return path → Completion moment → Explore (layout) → Explore › article → Explore (search) → Explore › Company → App-update prompt → Store review prompt → Heatmaps and session recordings → Bug fixes → Dark mode.

**Decisions made directly in this authoring session, not previously in any other memory:**
- **Full-article return path**: shipping approach is to remove the separate "read full article" button and simplify the card — tapping the center of the card opens the full article directly. This replaces an earlier "add a return path back into the brief" idea.
- **Explore split into two distinct problems**: (1) layout/space — the Articles/Companies tabs at the top of Explore take up too much room, leaving less space for the card view below, fix is to optimize/minimize that top section; (2) content/monotony — flat, same-order list, fix is signal-based cards (funding/hiring moves). These were one item before this session; now two.
- **New item — Heatmaps and session recordings**: no way today to see how people behave inside the app. Runs on the analytics tool already in the app stack, so it does not add a new vendor.
- **Dark mode** ships with an Appearance section added under Profile settings, so users can switch between dark and light themselves.
- **Notifications folded into Bug fixes** rather than kept as its own top-level item — push not delivering at all is being treated as a bug fix, not a feature line.
- **Store review prompt** explicitly covers both platforms: Android via Play's In-App Review API, iOS via `SKStoreReviewController` (capped at 3 prompts/365 days, no callback on whether the user rated).
- **Sector-based imagery** is explicitly flagged as a separate, unconfirmed track, not bundled into the brief card redesign.
- **Welcome screen** is a distinct item from the Walkthrough (which is purely a Customer.io migration for manageability, unrelated to the tour's drop-off numbers). Welcome screen's own problem: doesn't clearly convey the problem solved or the solution offered; fix is a more compelling visual redesign.

**Why:** repeated review cycles surfaced that early drafts conflated unrelated problems into one row, invented data-driven justifications that were never actually agreed, and used internal names/jargon inappropriate for a stakeholder audience — see [[feedback-stakeholder-doc-writing]] for the generalizable lessons from that process.

**How to apply:** treat this doc as the current authoritative source for "what's in the app v2 stakeholder-facing scope" — more current than piecing it together from the Thread 1–10 reconciliation in [[project-inc42-app-v2-scope-full]]. If asked to update it again, read the live doc/artifact first rather than reconstructing from memory, since further stakeholder review rounds are likely.
