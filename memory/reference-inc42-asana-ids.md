---
name: reference-inc42-asana-ids
description: "Inc42 Media Asana workspace, project, and key user GIDs"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 330a8dfe-7753-415f-9b90-46619392f05d
  modified: 2026-08-29T07:43:44.478Z
---

Captured 2026-08-27 while filing Asana tickets via `mcp__asana__*` tools.

- Workspace: **Inc42 Media** — gid `176734136274`
- Project **Inc42 App** — gid `1216274779493698` — default home for app-specific tickets, see [[feedback-asana-ticket-project-tagging]]
- Project **Product | Backlog** — gid `1202454202198945` — general intake project, see [[project-inc42-ways-of-working]]
- User **Ritvik Sethi** — gid `1213487661750162`

This Asana MCP integration authenticates separately from Claude Code's own account — see [[reference-account-identities]]. Its `create_task` tool takes only one `project_id`; there's no tool to multi-home a task into a second project after creation.
