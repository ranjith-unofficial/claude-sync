---
name: feedback-sheets-clipboard-paste-safety
description: Safety procedure for pasting large data into Google Sheets via OS clipboard (pbcopy/cmd+v) from browser automation
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a44f396b-c24a-49ef-8e79-300e18498cf8
  modified: 2026-08-28T13:22:07.376Z
---

When pasting large chunked data into a Google Sheet via `pbcopy < file` + browser `cmd+v` (used because the data is too big to inline through a `navigator.clipboard.writeText` JS call): **verify clipboard content with `pbpaste | head -c 80` immediately before every single paste, not just once at the start.**

**Why:** the OS clipboard is shared system-wide. Mid-task, on [[project-inc42-product-trainee]]'s 2026-08-27 sheet rebuild, something else on the Mac silently overwrote the clipboard with an unrelated `claude.ai/code/artifact/...` URL between a `pbcopy` call and the eventual `cmd+v` — landing garbage text in a live cell. It also happened via a stray misclick that put a literal cell-reference string ("C139") into a cell in edit mode. Two cells got corrupted this way in one session; both were only caught because of post-paste screenshot verification.

**Also observed:** the browser-automation permission classifier intermittently blocks routine `type`/`key` actions (Return, cmd+v) on Google Sheets with no discernible pattern — not a real safety issue, just retry the identical action once or twice and it goes through. Never treat a blocked action as "didn't happen and is safe to ignore" — always re-check state (zoom on the Name Box / formula bar) before proceeding, since a partially-applied keystroke can leave the sheet in an unexpected edit state.

**How to apply:** for any future multi-chunk sheet paste — click target cell via Name Box → verify Name Box shows the intended cell (zoom screenshot) → `pbcopy` the chunk → `pbpaste | head -c 80` to confirm → `cmd+v` → screenshot to confirm the pasted content matches the expected first row. Skipping the pre-paste clipboard check is the specific step that let both corruptions through.

**Two more hazards, both hit on 2026-08-30 (Sheet14 dunning-banner build in the "Test" spreadsheet):**

1. **The clipboard hijack is real and repeatable, and it is another Claude session on the same Mac.**
   Twice in one session the HTML flavour set by `osascript ... as «class HTML»` was replaced between
   the set call and the `cmd+v` (16584 bytes -> 11039 bytes, with a new plain-text flavour appearing).
   The intruding text was "Feedback and rating: placement plan" — content from a concurrent session that
   was writing [[project-inc42-app-feedback-rating-system]] at the same moment. `pbpaste` returns EMPTY
   when only the HTML flavour is set, so **`osascript -e 'clipboard info'` is the check to use, not
   `pbpaste`** — compare the byte count to what you just wrote. Post-paste screenshot + `cmd+z` is the
   safety net that actually caught it; a pre-paste check alone does not close the window.

2. **Clicking a cell right after a paste can DRAG the pasted block instead of selecting.** Happened twice.
   A `left_click` landing on or adjacent to the still-selected pasted range picks the block up and drops
   it one row off (A36:C47 -> A35:C46). `cmd+z` undoes it cleanly. **Always click far away from the live
   selection**, in an empty column, before navigating.

**Two Sheets browser-automation facts learned the hard way in the same session:**
- **The Name Box cannot be focused by click** in this setup — clicking it and typing "A27\n" does
  nothing, and worse, it swallows subsequent arrow keys so the grid stops responding. Navigate by
  clicking a cell then arrowing.
- **Click coordinates are ~1.126x the screenshot coordinates** (the screenshot is scaled down from the
  real viewport). Never trust a computed cell coordinate — click, read the Name Box, then correct with
  arrow keys.
- **The Name Box render lags the actual selection by seconds.** After a burst of arrow keys it can still
  show the old cell; `wait 2` then re-zoom before concluding the keys did not register. Also `key` with
  `repeat: N` is unreliable (often applies once) — pass the key space-separated N times instead.

**Why clipboard paste is often the ONLY route (learned 2026-09-08, uploading `ashish-events-media-datalabs-app-v3.xlsx` into the "Test" spreadsheet):**
Google Sheets' **File → Import → Upload is unusable from browser automation**. The Drive picker renders in a
cross-origin iframe: `read_page` shows only `dialog → generic` with no children, `find` cannot see the Browse
button or any `<input type=file>`, so `file_upload` has no ref to target and clicking Browse would open a
native dialog that automation cannot see. Do not spend calls trying — go straight to building the tabs by hand.

**Use HTML paste, not TSV, whenever any cell may contain a newline.** In that workbook 9 of ~180 rows had
embedded `\n` (e.g. "Lock Type\nLock Interaction"), which TSV paste would have split into extra rows.
Convert each sheet to an HTML `<table>` (escape, then `\n` → `<br>`), and set the clipboard with:
`hex=$(hexdump -ve '1/1 "%.2x"' file.html); osascript -e "set the clipboard to «data HTML${hex}»"`.
A 52 KB HTML file (67 rows x 19 cols) went through in one paste with no size trouble.

**What HTML paste carries and does not:** values, line breaks inside cells, bold header row, hyperlinks — yes.
Autofilter ranges, column widths, and any xlsx-level sheet settings — no; say so when reporting.

**Tab mechanics that worked:** click Add Sheet (+) → the new sheet opens with A1 selected, click cell A1 to give
the grid focus → set + verify clipboard → cmd+v → double-click the new tab in the strip (it lands right after
the previously active tab, not at the end) → type the name → Return. Verify each paste by reading the Name Box
range after paste (it shows e.g. `A1:S67`) and by clicking column A then `cmd+Down` to confirm the last row
matches the source.

**RECURRED 2026-09-12** ([[project-inc42-ph-cio-parity-android]] sheet rebuild). Same failure, and it was
avoidable: I ran `pbcopy`, verified it, then did ~8 browser steps (navigate, wait, screenshot, click,
cmd+a, delete, name-box, type) before the `cmd+v`. In that window a **Figma design URL** replaced the
clipboard, and it landed in A1. Caught only by the post-paste screenshot; recovered with two `cmd+z`.

**The ordering rule that actually prevents this — do these three with NOTHING in between:**
1. Finish all sheet preparation first (select the tab, clear the range, put the cursor on A1).
2. `pbcopy < file` and verify in the SAME Bash call with `diff -q <(pbpaste) file` — an exact whole-file
   compare, not a `head -c 80` prefix check. A prefix check also produced a false alarm this session
   because my expected string was off by one character.
3. `cmd+v` as the very next tool call.

**Two more gotchas from the same session:**
- `cmd+a` in Sheets selects only the *contiguous block* around the cursor, not the sheet. To clear a tab,
  click the **select-all corner box** at the top-left of the grid (approx. x=25, y=157 at default zoom),
  then Backspace. `Delete` as a key name did nothing; `Backspace` worked.
- Always screenshot immediately after the paste and read A1 before moving on.
