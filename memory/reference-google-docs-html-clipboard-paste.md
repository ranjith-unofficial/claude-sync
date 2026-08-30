---
name: reference-google-docs-html-clipboard-paste
description: "Reliable technique to get real Google Docs Heading styles, bullet lists, and tables via browser automation — paste raw HTML from the macOS system clipboard instead of keystroke-simulated typing"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 03703bc3-38d6-46ae-89df-b20d1af00bb4
  modified: 2026-08-30T13:05:23.791Z
---

When building Google Docs content via Claude-in-Chrome browser automation, pasting
a semantic HTML fragment from the macOS system clipboard is far more reliable than
simulating keystrokes (cmd+alt+1/2/3 heading shortcuts + typed text) — the
keystroke approach is slow, drifts on coordinate-based sidebar clicks, and is prone
to Google Docs' autoformat mangling content (e.g. lines starting "1. " or "(a) "
get auto-converted into numbered/lettered lists mid-paste).

**The working method (verified during [[project-inc42-master-prd-rebuild]]):**

1. Write a plain semantic HTML fragment — `<h1>`/`<h2>`/`<h3>`, `<p>`, `<ul>/<li>`,
   `<table>/<tr>/<td>/<th>`, `<b>` — no `<html>/<head>/<body>` wrapper strictly
   required but harmless if included. No CSS needed.
2. Load it onto the real macOS clipboard as genuine HTML pasteboard data via Bash:
   `osascript -e 'set the clipboard to (read (POSIX file "/path/to/file.html") as «class HTML»)'`
3. Click once into a **genuinely empty** Google Docs tab, then `Cmd+V`.

This reliably produces real named paragraph styles — verified by clicking into the
pasted heading and checking the style dropdown actually reads "Heading 1" (not just
visually bold/large text) — plus real Google Docs bulleted lists and native tables.

**What does NOT work as well:**
- Converting HTML → RTF via `textutil -convert rtf` before pasting: lost heading
  style recognition entirely (headings pasted as plain bold text, no named style)
  and in one test added unwanted bold to body paragraphs.
- Building a `.docx` via `python-docx` (even using `doc.add_heading(level=1)`) then
  converting to RTF via `textutil`: worse than raw HTML — made body text bold too
  and still didn't produce real heading styles on paste.
- Pasting into a tab that isn't genuinely fresh: leftover cursor formatting state
  (e.g. right after a `cmd+a` + Delete on old bold content) can bleed bold
  formatting into the newly pasted text. Always test on a brand-new empty tab.

**Google Docs sidebar/tab-list automation notes learned in the same session:**
- Right-click a tab's treeitem (via an accessibility-tree `ref`, not raw x/y
  coordinates — raw coordinates drift unpredictably on this canvas-rendered app)
  to open its context menu, then click menu items (Add subtab / Rename / Delete)
  also via `ref`.
- Context-menu item refs (e.g. "Rename", "Add subtab", "Delete") stay stable and
  reusable across repeated openings of the *same* menu in one session — you can
  right-click a new tab's treeitem and click the previously-found "Rename" ref
  directly without re-querying it every time, which meaningfully speeds up
  repetitive tab creation.
- A newly created subtab is auto-named "Tab N" with a session-global incrementing
  counter — useful for predicting its name to search for directly instead of a
  fuzzy "find the newest tab" query, which is unreliable.
- Deleting a tab that has subtabs shows a "Delete this tab and all subtabs?"
  confirmation with a "Delete this tab but keep all subtabs" checkbox option.
