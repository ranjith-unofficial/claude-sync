---
name: inc42-master-prd
description: How to update the Inc42 App Master PRD Google Doc without breaking it — the section structure, the supersede check that must run before any new document is added, every other place that has to change in the same pass, and the browser mechanics that actually work on this canvas-rendered doc. Load before adding, moving, renaming or rewriting any tab in that document, before recording a feature as live or not built, and before filing a decision that came out of an app review.
---

# Inc42 App Master PRD — update procedure

**The document:** "Copy of Inc42 App Master PRD" — `docs.google.com/document/d/13vNB88le_0-mOGv3nueRJEQOUfrLVYIujBWLGAj6qow`

⚠️ **There are two copies and they have diverged.** The restructure lives only in the Copy above. The original, "Inc42 App Master PRD" (`1eT472QdzWOg_ChvvmoO3cX5CnL2sqToR5jU8-GvMxzw`), still has the old flat 47-tab layout and is the one the team has historically opened. Confirm which one you are editing, and say so in your report.

## The structure

Seven top-level sections, ordered by state, not by document type:

```
0. Start Here          doc map + the supersede rule + one misleading name
   0.1 Decisions log   every locked decision, consolidated, with dates and source tab
1. The app today       App PRD (current) + per-surface detail
   1.1 Brief           the only group here, because it holds 5 documents
2. What is coming next App PRD v2 · rating prompt · 2.1 AskInc42 · 2.2 Backlog
3. Platform & Measurement
4. Governance
5. Reference & Research
6. Archive             6.1 superseded v1 PRDs · loose superseded specs · 6.2 pre-app research · 6.3 empty
```

**Nesting rules, learned the hard way:**
- Nothing loose at the top level. Every document sits inside a numbered section.
- **A group needs 3+ documents to exist.** One or two go directly under the parent. Never create a wrapper holding a single document.
- **Every container tab must have its own content** — a short index of what is inside and what to know before opening it. A tab that opens blank is a defect.
- Google Docs caps nesting at 3 levels.
- Mixed depth is fine: a document and a group can be siblings.

## Before adding any new document

1. **Supersede check.** Search existing tabs for the subject. If one exists, decide explicitly: does yours replace it, extend it, or annex it? Record that decision. Skipping this is how three generations of the v1 PRD and five overlapping AskInc42 documents accumulated unnoticed.
2. **One PRD per thing.** Engineering detail becomes a section inside that PRD, or a clearly-labelled annex tab beneath it. Never a sibling document with its own problem statement — that is what made "two Ask PRDs" appear.
3. **Conflicting numbers are a defect, not a variant.** Ask latency was stated as "under 3s" in one doc and locked at 5s/10s in another. Resolve before filing, and write the resolution into the surviving document.
4. **Name it the way the team says it.** Not the way the spec says it. See the naming trap below.

## The naming trap — this has caused two wrong entries

The document uses internal names nobody says out loud. Twice this led to a live feature being recorded as missing:

| Document says | Team says | What happened |
|---|---|---|
| Decode | **30 sec summary** | Recorded as "not built" because the name was unrecognised. It was live all along |
| "Rate" control | **like and dislike on a story** | Nearly deleted from the inventory as a feature that does not exist. It is live and fires `brief_story_rated` |

**Rule:** a zero-fire event plus an unfamiliar name is a naming question first, an instrumentation gap second. Never infer that a feature exists because the spec describes it, or that it is absent because you do not recognise the name. Ask.

## When something changes, update all of these in the same pass

| What changed | Also update |
|---|---|
| A feature went live, or turned out not to exist | The **feature inventory table** at the top of `App PRD (current)` — status column *and* the detail cell |
| Scope moved in or out of v2 | `App PRD v2` item list, and the section 2 index page if the framing changed |
| A decision got locked | `0.1 Decisions log` with date + the tab it came from. Do not leave it only in the feature doc |
| A new event, property or rename | `Analytics PRD and event dictionary` (section 3), and the event change lists in 2.2 Backlog |
| A document was superseded | Move it to section 6, and add a line to the section 6 index saying what replaced it |
| Anything at all | The relevant memory file, so the next session does not re-derive it |

**Outside the document:** Asana (Inc42 App project `1216274779493698`; Product | Backlog `1202454202198945`) · the Open Ledger sheet and the App V2 Roadmap tab in the "Test" spreadsheet · the tracking master sheet for event changes.

## Content rules

- **Archive, never delete.** Superseded documents move to section 6 with a note on what replaced them. Empty original tabs are kept too. The only things ever deleted are empty scaffolding tabs created during a restructure.
- **Status travels with scope.** A scope edit that leaves the status table stale is incomplete work.
- **Say what is not built.** If a section specifies something absent from the app, mark it in the inventory rather than letting the spec imply it ships.
- **No em dashes** in stakeholder-facing tabs.

## Browser mechanics that actually work

Google Docs renders to **canvas**. Content cannot be read from the DOM and coordinate clicking is unreliable — the page scrolls between the screenshot and the click.

- **Read headings:** `document.querySelectorAll('.navigation-item-list')` — one per tab, in tab order. Read body text from screenshots, or from a Drive markdown export.
- **Move a tab:** Tab options → **Move into**. Open the menu by clicking the row's `[aria-label="Tab options"]` button, then dispatch `mouseover` on the "Move into" item to open the submenu. No drag-and-drop needed. The row must be hovered first or the button does not exist.
- **Paste formatted content:** set the macOS clipboard with **both** flavours via osascript — `set the clipboard to {«class HTML»:«data HTML…», string:"…"}`. HTML alone is ignored and Docs silently falls back to its own internal clipboard, which pastes something else entirely.
- **Paste position:** click into the body, `cmd+a`, then `Right` to collapse to the end or `Left` for the start. `cmd+End` does not work reliably.
- **Paste inherits the style of the paragraph it lands in.** Landing on an H1 makes the whole block H1; landing on bold text makes it all bold. Put the cursor on a Normal-style paragraph first (`cmd+alt+0` sets Normal).
- **Replacing a table:** right-click inside it → **Delete table**, then paste. Editing individual cells by coordinate fails repeatedly.
- **Find and replace:** open via the Edit menu, then focus the field with `[aria-label="Find"]` and type with real keystrokes. Verify `document.activeElement` is the input **before typing** — if focus silently fails the text goes into the document body. Turn **Match case** on for anything where a lowercase variant is an event name.
- **Always screenshot after a paste or replace.** Pastes have landed mid-sentence and mid-heading. Undo works cleanly; verify before moving on.
