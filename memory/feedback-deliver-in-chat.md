---
name: feedback-deliver-in-chat
description: "Default to answering in chat with tables — don't publish an artifact unless Ranjith asks for a document"
metadata:
  type: feedback
---

When Ranjith asks for something "in tabular format" or asks a working question, **answer in the chat with markdown tables.** Do not build and publish an Artifact unless he explicitly asks for a doc, page, deck, or file.

He rejected an artifact publish on 2026-08-19 mid-flow with *"Share it here not in artifact"* — the content (an interview question bank) was what he wanted, the delivery vehicle was not.

**Why:** he reads and acts in the terminal. A link is an extra hop, and for something he uses live — mid-interview, mid-call — scrollback he can search beats a page he has to open.

**How to apply:**
- "give me X in tabular format" / "list of questions" / "break this down" → chat tables, no artifact.
- Build an artifact only on an explicit ask: "make me a doc / page / one-pager / deck", or when the deliverable is clearly for other people to read.
- Long output in chat is fine — [[feedback-communication-style]] rules the *shape* (crisp, bullets, tables, no paragraphs), not the length.
- Files that are genuine deliverables still go to `~/ClaudeDocs/` per the global instructions — that is separate from whether to publish an Artifact.

Related: [[feedback-communication-style]], [[feedback-document-calibration]].
