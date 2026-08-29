---
name: feedback-asana-ticket-project-tagging
description: "Inc42 app Asana tickets must have \"Inc42 App\" as their project, not just Product | Backlog"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 330a8dfe-7753-415f-9b90-46619392f05d
  modified: 2026-08-29T07:43:37.669Z
---

When filing Asana tickets for Inc42 app bugs/work, always set the project to **Inc42 App** — not (only) Product | Backlog.

**Why:** Ranjith corrected this on 2026-08-27 after 3 tickets (Android deep-link-opens-Brief bug, deep linking path config, Customer.io push not delivered — all assigned Ritvik Sethi) were created in Product | Backlog by default. He then moved all 3 into Inc42 App himself. Inc42 App is the team's actual working project for app-specific tickets; Product | Backlog is general intake, not where app work should live. See [[project-inc42-ways-of-working]] for how Backlog vs Master vs project-specific homes fit together.

**How to apply:** When creating a new Asana task for Inc42 app work via the `mcp__asana__asana_create_task` tool, pass `project_id` = the Inc42 App project gid (see [[reference-inc42-asana-ids]]), not Product | Backlog's gid. This MCP Asana integration's `create_task` only accepts a single `project_id` and there is no tool to add a second project to an already-created task — if a ticket also needs to be multi-homed into Product | Backlog (or elsewhere) after creation, tell Ranjith to add it manually from the task's Asana UI ("Projects" field, "+" button); don't try to fake it by recreating or duplicating the task.

Also carried from the same request: when a ticket's description is written on Ranjith's behalf, do not mention that it was reported/sourced by Ranjith — write it as a neutral bug report.
