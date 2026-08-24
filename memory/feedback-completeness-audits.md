---
name: feedback-completeness-audits
description: "When Ranjith hands over a reviewed doc, audit it line-by-line and report every miss, including my own"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1b85df8c-b255-4a10-9994-1dbcc66c6987
  modified: 2026-08-24T09:54:05.544Z
---

When Ranjith gives me a document someone has reviewed (e.g. Utkarsh's compliance review) and asks whether the changes are incorporated, he wants a **line-by-line audit against every single item** — not a summary.

**What he expects:**
- Walk each numbered change (P-1…P-17, T-1…T-7) and state incorporated / deviation / missing.
- **Surface my own errors first and plainly.** He reacted badly ("you are doing a poor job", "I'd have been better off with Gemini") when I summarized instead of auditing and missed items the reviewer had raised.
- Flag inconsistencies *inside the source document itself* — reviewers contradict themselves too.
- Do NOT silently "improve" wording beyond what a decision authorised. Utkarsh caught me broadening a clause and rightly asked "which decision authorised this?" If evidence justifies a change, **present the evidence and get the call** rather than shipping it.
- Never restate a question he has already answered. He calls out repetition sharply.

**Why:** these are legal/compliance documents where a single missed clause causes a store rejection. He is accountable for them and cannot verify every line himself, so a falsely confident "all done" is worse than a slow, honest audit.

**How to apply:** before answering "is it all in?", actually re-read the source, grep the target, and produce a status table. If the PDF/DOCX exports are stale relative to the source, say so — don't imply they're current. Pairs with [[feedback-validation-approach]] and [[feedback-communication-style]].

**Self-inflicted miss, not just a review miss (2026-08-24), [[project-inc42-datalabs-winback]]:** this applies to restructuring my own output, not only auditing someone else's. Collapsing seven narrative "problem cards" into one summary table silently dropped a nested reference table (exact message copy per mandate state) that lived inside one of the cards — it didn't fit the new column layout and got left out without noticing. Only caught because Ranjith kept probing the doc and I re-diffed old content against new. **How to apply:** any time I restructure/reformat a doc (reorganizing sections, collapsing cards into a table, merging content), grep the old version for named facts/tables/copy and confirm each one still appears in the new version before calling it done — reformatting is exactly the moment detail silently disappears, not just review of external material.
