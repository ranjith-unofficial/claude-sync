---
name: reference-figma-mcp-limits
description: Figma MCP tool calls are hard-capped by plan+seat — check whoami before planning any multi-call Figma build
metadata: 
  node_type: memory
  type: reference
  originSessionId: ef11cc53-5cf2-4546-8887-4d4fa24655b1
  modified: 2026-08-28T20:11:44.352Z
---

Figma MCP access is metered by **plan + seat**, and writes count against it. As of 2026-08-17, `ranjith.m@inc42.com` is on **Starter plan, View seat = 20 tool calls per MONTH**, and that quota was exhausted mid-task (the `get_figjam` read succeeded, the first `use_figma` write returned an upgrade paywall).

Limits: Starter View/Collab 20/month. Professional Full/Dev 200/day. Org Full/Dev 200/day. Enterprise Full/Dev 600/day. Org/Enterprise View/Collab only 6/month.

Exempt from the cap (always callable): `whoami`, `generate_figma_design`, `add_code_connect_map`. **`use_figma` is NOT exempt** despite being a write tool — the docs' "write tools are exempt" line is misleading, only the three listed tools are.

**Why:** a full FigJam board build takes 6-12 `use_figma` calls. On a 20/month cap that is one board per month, and running out mid-build leaves a half-drawn board on the canvas.

**How to apply:** call `whoami` (free) BEFORE starting any multi-call Figma build and budget the calls against the seat's cap. On a tight cap, batch aggressively — 5-6 large `use_figma` calls instead of the usual 10-op-per-call incremental pattern — and skip intermediate `get_screenshot` verification until the end. Figma also restricts MCP file access to plans the authenticated user belongs to, so a second free account generally cannot write into a file owned by another plan even when that file is shared with it. Related: [[project-inc42-unification]] (the One INC42 vision board lives in FigJam file `VKJwL4lhOHj1Gb5VJToYvZ`).

**Confirmed 29 Aug 2026:** a View seat is hard read-only for design files too, not just a call-count limit — `use_figma`'s `createFrame` throws `"Can't call 'createFrame' in read-only mode"` even for a brand-new, isolated test frame that touches nothing existing. This holds regardless of whether the file's Figma *sharing* permissions say "can edit" — the MCP session inherits the seat's plan-level access, not the file-level share setting. Read tools (`get_metadata`, `get_design_context`, `get_screenshot`) still work and count against the 20/month cap; that quota had refreshed by 29 Aug (2 read calls succeeded) after being exhausted on 17 Aug. To get real write access via Claude, the Figma team seat itself needs upgrading to Full/Dev — that's a Figma admin/billing action, not fixable from a session.

**Same-day follow-up:** Utkarsh approved a "full access" seat request for `ranjith.m@inc42.com` on the **Inc42** org team (confirmed by Figma's own "Seat request approved" email). Reconnecting Figma via Claude Code's `/mcp` command re-authenticated successfully ("Connected to claude.ai Figma") but `whoami` still only listed "Ranjith M's team" (Starter/View) and a fresh `createFrame` test on the `Inc42-App-2026` file still threw the same read-only error.

**Corrected finding:** the Chrome browser session on the same file (`vKuPUMuhLos0rC1AFR5cWq`, "Inc42-App-2026") is ALSO view-only, not edit — initially misread as edit-capable because the Share button and Properties/Layers panels render for viewers too. The real tell is Figma's bottom-toolbar **"Ask to edit"** button, which was present from the very first screenshot. Confirmed view-only by: right-click canvas menu has no "Paste"/"Paste here" option, and pressing `R` + dragging to draw a rectangle created nothing. So the org-level seat upgrade (Full/Dev) does not automatically grant edit on a specific file — file-level sharing is a separate permission layer, and this file still lists the account as Viewer. Fix has to happen in Figma itself: click "Ask to edit" in-app and have the file owner approve, or have an editor explicitly re-share the file as Editor. Neither an MCP reconnect nor browser automation can bypass this. Don't re-attempt writes on a file until the user confirms file-level edit access was actually granted (check for "Ask to edit" being GONE from the toolbar, not just seat/plan status).
