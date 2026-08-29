---
name: feedback-stakeholder-doc-writing
description: "How to write documents meant for external/stakeholder audiences (not internal team) — no em-dashes, no internal names, genuinely high-level summary tables, verified sourcing, verified doc pastes"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9108f882-accb-498a-b781-8d81145ba85e
  modified: 2026-08-29T07:42:00.141Z
---

When building a document meant for stakeholders (not the internal working team), several corrections came up repeatedly while building the INC42 app v2 scope doc ([[project-inc42-app-v2-stakeholder-doc]]):

- **Never use em-dashes (—).** Rewrite with periods, commas, or colons instead. Explicit instruction, applies to the whole document.
- **Never name internal team members** (designers, engineers, specific owners) in stakeholder-facing text. Genericize instead — "the design exploration," not a person's name. Reason given: "we are sharing this to stakeholders."
- **Keep any "at a glance" summary table genuinely high-level.** One plain sentence per cell, no jargon, no vendor/mechanism names (e.g. don't name specific SDKs or named design variants in the summary), no bare data-point citations like "a 30pt drop" without explanation. Push all technical/implementation detail into a separate "in detail" section below the table, never into the summary itself. Repeated correction: "they do not have any time or bandwidth to understand this."
- **Don't invent or infer a "problem statement" from analytics data unless it was actually the stated reason for a decision.** Check before presenting data-derived reasoning as the agreed justification for a change — caught multiple times in this session (a walkthrough migration justified by a drop-off stat that was never the actual reason; funnel jargon presented without plain-language explanation, e.g. "I have 0 clue what 30pt to 24pt means").
- **After any edit or rewrite to a Google Doc via select-all + paste, verify with an actual full scroll-through screenshot**, not just a status message. This session hit two silent failures (stale content mixed with new after an incomplete select-all, a delete that silently didn't register) that weren't caught until the user pointed them out from a screenshot. cmd+a's selection highlight doesn't always render on the first screenshot after the keypress — re-check before trusting it.

**Why:** these were each corrected more than once in the same session (building the INC42 app v2 stakeholder doc, 28–29 Aug 2026), and the user's tone escalated each time a category repeated ("what ever you have prepared is completely useless").

**How to apply:** apply proactively to any future document meant for people outside the immediate working team, not just app v2. Related: [[feedback-document-calibration]] (state decisions directly, don't narrate alternatives), [[feedback-artifact-design-minimal]] (visual minimalism, a parallel but separate lesson about design not language).
