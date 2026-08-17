---
name: reference-figma-mcp-limits
description: Figma MCP tool calls are hard-capped by plan+seat — check whoami before planning any multi-call Figma build
metadata: 
  node_type: memory
  type: reference
  originSessionId: ef11cc53-5cf2-4546-8887-4d4fa24655b1
  modified: 2026-08-17T09:17:17.539Z
---

Figma MCP access is metered by **plan + seat**, and writes count against it. As of 2026-08-17, `ranjith.m@inc42.com` is on **Starter plan, View seat = 20 tool calls per MONTH**, and that quota was exhausted mid-task (the `get_figjam` read succeeded, the first `use_figma` write returned an upgrade paywall).

Limits: Starter View/Collab 20/month. Professional Full/Dev 200/day. Org Full/Dev 200/day. Enterprise Full/Dev 600/day. Org/Enterprise View/Collab only 6/month.

Exempt from the cap (always callable): `whoami`, `generate_figma_design`, `add_code_connect_map`. **`use_figma` is NOT exempt** despite being a write tool — the docs' "write tools are exempt" line is misleading, only the three listed tools are.

**Why:** a full FigJam board build takes 6-12 `use_figma` calls. On a 20/month cap that is one board per month, and running out mid-build leaves a half-drawn board on the canvas.

**How to apply:** call `whoami` (free) BEFORE starting any multi-call Figma build and budget the calls against the seat's cap. On a tight cap, batch aggressively — 5-6 large `use_figma` calls instead of the usual 10-op-per-call incremental pattern — and skip intermediate `get_screenshot` verification until the end. Figma also restricts MCP file access to plans the authenticated user belongs to, so a second free account generally cannot write into a file owned by another plan even when that file is shared with it. Related: [[project-inc42-unification]] (the One INC42 vision board lives in FigJam file `VKJwL4lhOHj1Gb5VJToYvZ`).
