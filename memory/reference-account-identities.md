---
name: reference-account-identities
description: "Which email/account each tool and MCP connection actually runs as — they are NOT all the same, and it changes who owns artifacts and who shows in audit logs"
metadata: 
  node_type: memory
  type: reference
  originSessionId: b2024af5-d7ba-4821-944c-c16a524e5e85
  modified: 2026-08-29T17:30:00.000Z
---

Verified 2026-08-20 by reading `~/.claude.json` and calling each connection's identity endpoint. **Do not assume the session email from context — check.**

| Surface | Identity |
|---|---|
| **Claude Code login** | **CHANGED 2026-08-29: now `datalabs@inc42.com`** (accountUuid `4f28d046-e8d7-476e-a0bb-0422208cd6cd`, org `datalabs@inc42.com's Organization`, organizationRole **admin**). Was `ranjith@ranjith.tech` (accountUuid `c0857c0a-...`) on 20 Aug. **This is the SHARED Inc42 Max account** — Ranjith flagged 29 Aug that it is shared across multiple teams. |
| Asana | `ranjith.m@ink42.com` — gid `1216274906880251` |
| Fathom | `ranjith.m@inc42.com` |
| PostHog | `prapti@inc42.com` (Prapti Rastogi) |
| Wispr Flow | "Ranjith M", no email exposed |
| Figma | `ranjith@ranjith.tech` for the v2 vision board; `ranjith.m@inc42.com` is quota-exhausted — see [[reference-figma-mcp-limits]] |

**As of 2026-08-29 the context block and the login AGREE: both are `datalabs@inc42.com`.** This reversed since 20 Aug, when context said datalabs and the login was ranjith@ranjith.tech. The lesson stands either way: read `~/.claude.json`, don't infer.

**Consequence (29 Aug):** every claude.ai MCP connector on this account — Wispr Flow (all meetings incl. interviews and 1:1s), Google Drive, Asana, Figma, PostHog — is reachable by anyone using the shared login. Only `mobbin` is configured as a LOCAL mcpServer in `~/.claude.json`; locally-configured servers are single-tenant, cloud connectors are not. The `Inc42 Morning Tape` cloud routine (`trig_01TivYHQj3K7XSj2xA2JADxe`) was created by this shared account.

**Three consequences that have already bitten:**

1. **Artifacts are owned by the publishing account.** Two artifacts published in the 20 Aug session (the open ledger and the app behaviour report) later returned "artifact not found" and could not be updated — republishing the same file path failed with "the artifact you're updating was deleted, or you no longer have write access to it." Fix was to copy to a NEW filename and publish fresh, which mints a new URL. If artifact links go dead, suspect account mismatch first.
2. **PostHog work is logged as Prapti, not Ranjith.** Every query runs under her account and appears in PostHog's activity log as her activity. Don't say "I pulled this" in a way the audit trail contradicts.
3. **The Asana domain is `ink42.com`, not `inc42.com`** — on both Ranjith's account and Ritvik Sethi's (`ritvik.sethi@ink42.com`). Consistent across two users, so likely a real alternate domain rather than a typo, but UNCONFIRMED. Anything keyed on email (notifications, integrations, automations) will miss if that mailbox is not live. Assign Asana tasks by **user GID**, not email.

**How to apply:** before claiming which account did something, verify it. `~/.claude.json` → `oauthAccount.emailAddress` for Claude Code; `asana_get_user {"user_id":"me"}`; Fathom `get_identity`; PostHog reports its user in the active-environment block.
