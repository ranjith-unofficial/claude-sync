---
name: feedback-document-calibration
description: "How much reasoning/detail to put in a doc for Ranjith — state decisions directly, explain only what would otherwise be confused, never narrate rejected alternatives or invent unrequested sections"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9859d45d-f58a-4c8b-b439-1562f2def0be
---

Calibrating a working document (PRD, strategy memo) for Ranjith took three passes on the AskInc42 PRD before landing right — useful as a standing rule, not just for that doc.

**The oscillation, concretely:**
1. First pass: terse conclusions only ("D9: brief-end conditional on completion data") — he called it exaggerated-sounding but under-argued: "simple one-liners... I have no pointers on... you added your own choices."
2. Second pass: restored full reasoning for *every* decision, including narrating rejected alternatives (e.g. explaining the "peak-end rule" idea that was considered and dropped) and inventing unrequested infrastructure (a URL/deep-link routing scheme, a Free/Plus tier table for a feature with no monetization decision).
3. Correction: "these are our brainstorming topics and are not finalized, such things are not to be covered here because it is unnecessary." He also corrected a real factual error I'd invented along the way — an "editorial approval queue" — when he'd actually described something simpler (editor sees the AI-drafted title at publish time, edits if needed, done).

**Why:** he needs to present these docs to Utkarsh and needs conviction in them — a doc that reads as padded with the model's own speculative additions undermines that, but a doc that's just conclusions with no argument is equally useless because he can't defend it either.

**How to apply, the landed calibration:**
- State locked decisions directly and plainly.
- Add reasoning *only* where it prevents a real, likely confusion (e.g. why two similarly-named surfaces are actually different jobs) — not as narrative color for every decision.
- Never narrate alternatives that were considered and rejected mid-conversation. If it didn't ship, it doesn't belong in the doc, even briefly.
- Never add a section, mechanism, or speculative table (URL schemes, tier boundaries, kill-criteria numbers) he didn't ask for, even if it seems like good PRD practice — ask, or leave it out, don't invent it to seem thorough.
- When relaying back something he described, use his actual words/mechanism, don't substitute a more "proper-sounding" process (e.g. don't turn "editor sees the title at publish" into "editorial approval queue") — that's adding a decision, not documenting one.
- If genuinely uncertain what he meant, a short inline flag is fine; a whole ceremonial "pending questions" section is not — he asked to remove that pattern outright.

Related: [[project-inc42-askinc42]], [[feedback-ask-before-assuming]] (same root cause — stating uncertain things as settled — this is the mirror case of settled things getting over-explained).
