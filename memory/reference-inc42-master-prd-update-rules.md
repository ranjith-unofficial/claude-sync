---
name: reference-inc42-master-prd-update-rules
description: "Rules that must be followed before editing the Inc42 App Master PRD Google Doc — read this before adding, moving or writing any tab in that document"
metadata:
  node_type: memory
  type: reference
---

**Document:** "Copy of Inc42 App Master PRD" — `docs.google.com/document/d/13vNB88le_0-mOGv3nueRJEQOUfrLVYIujBWLGAj6qow`
Original (team-facing): `1eT472QdzWOg_ChvvmoO3cX5CnL2sqToR5jU8-GvMxzw`

Read this before touching that document. These rules exist because the doc reached 46 flat tabs with three generations of the same PRD and five overlapping AskInc42 documents, none of which anyone had noticed.

## Before adding any new document
1. **Supersede check first.** Search the existing tabs for the same subject. If one exists, decide explicitly: does the new document replace it, extend it, or is it an annex? Never add a second document on a subject without recording that decision. This is the single check that would have prevented the AskInc42 pile-up.
2. **One PRD per thing.** A feature has one PRD. Engineering detail becomes an annex section inside that PRD, or a sub-tab beneath it, never a sibling PRD with its own problem statement.
3. **Conflicting numbers are a defect, not a variant.** If the new document states a target that contradicts an existing locked decision (the Ask latency target did: 3s versus the locked 5s/10s), resolve it before filing, and write the resolution into the surviving document.

## Structure rules
4. **Nothing loose at the top level.** Every document sits inside one of the numbered sections.
5. **A group needs 3+ documents to exist.** One or two items go directly under the parent. Never create a wrapper that holds a single document.
6. **Every container tab has its own content** — at minimum a short index of what is inside and what to know before opening it. A tab that opens blank is a defect.
7. **Google Docs caps nesting at 3 levels.** Plan for it; anything deeper becomes headings inside a tab.

## Content rules
8. **Archive, never delete.** Superseded documents move to section 6 with a note saying what replaced them. Empty tabs are kept too. The only things ever deleted are empty scaffolding tabs created during a restructure.
9. **Status travels with scope.** Any change to what is being built must update the status in the same pass. A scope edit that leaves the status stale is incomplete work.
10. **The decisions log is the record.** New locked decisions go into `0.1 Decisions log` with a date and the tab they came from, not only into the feature document.
11. **Say what is not built.** If a section specifies something that does not exist in the app, mark it. Decode is the standing example: fully specified, named in a locked decision, never built.

## Mechanics that work (browser automation)
- Tab options menu has **Move into**, which nests without drag-and-drop. Open the menu by clicking the row's "Tab options" button, then dispatch a mouseover on "Move into" to open the submenu.
- Docs renders to canvas, so tab **content cannot be read from the DOM**. Read headings from the outline widget (`.navigation-item-list`, one per tab, in tab order); read body text from screenshots.
- To paste formatted content, set the macOS clipboard with **both** an HTML flavour and a plain-text flavour via `osascript` (`set the clipboard to {«class HTML»:«data HTML…», string:"…"}`). HTML alone is ignored and Docs falls back to its own internal clipboard, which pastes the wrong thing.
- To append at the end of a tab: click into the body, `cmd+a`, then `Right` to collapse the cursor to the end. `cmd+End` does not work reliably.
- **Always screenshot after a paste.** A paste has already landed mid-paragraph and split a sentence once. See [[feedback-sheets-clipboard-paste-safety]].
