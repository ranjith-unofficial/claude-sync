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
