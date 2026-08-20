---
name: reference-account-identities
description: "Which email/account each tool and MCP connection actually runs as — they are NOT all the same, and it changes who owns artifacts and who shows in audit logs"
metadata: 
  node_type: memory
  type: reference
  originSessionId: b2024af5-d7ba-4821-944c-c16a524e5e85
  modified: 2026-08-20T13:46:19.326Z
---

Verified 2026-08-20 by reading `~/.claude.json` and calling each connection's identity endpoint. **Do not assume the session email from context — check.**

| Surface | Identity |
|---|---|
| **Claude Code login** | **`ranjith@ranjith.tech`** (accountUuid `c0857c0a-6c64-400f-8d70-e37549e81597`, created 27 Jan 2026, google_play_subscription billing) |
| Asana | `ranjith.m@ink42.com` — gid `1216274906880251` |
| Fathom | `ranjith.m@inc42.com` |
| PostHog | `prapti@inc42.com` (Prapti Rastogi) |
| Wispr Flow | "Ranjith M", no email exposed |
| Figma | `ranjith@ranjith.tech` for the v2 vision board; `ranjith.m@inc42.com` is quota-exhausted — see [[reference-figma-mcp-limits]] |

**The session context block says `datalabs@inc42.com`. That is NOT the login.** The only email in `~/.claude.json` is `ranjith@ranjith.tech`. I asserted datalabs@inc42.com from context and Ranjith corrected it — read the config, don't trust the context line.

**Three consequences that have already bitten:**

1. **Artifacts are owned by the publishing account.** Two artifacts published in the 20 Aug session (the open ledger and the app behaviour report) later returned "artifact not found" and could not be updated — republishing the same file path failed with "the artifact you're updating was deleted, or you no longer have write access to it." Fix was to copy to a NEW filename and publish fresh, which mints a new URL. If artifact links go dead, suspect account mismatch first.
2. **PostHog work is logged as Prapti, not Ranjith.** Every query runs under her account and appears in PostHog's activity log as her activity. Don't say "I pulled this" in a way the audit trail contradicts.
3. **The Asana domain is `ink42.com`, not `inc42.com`** — on both Ranjith's account and Ritvik Sethi's (`ritvik.sethi@ink42.com`). Consistent across two users, so likely a real alternate domain rather than a typo, but UNCONFIRMED. Anything keyed on email (notifications, integrations, automations) will miss if that mailbox is not live. Assign Asana tasks by **user GID**, not email.

**How to apply:** before claiming which account did something, verify it. `~/.claude.json` → `oauthAccount.emailAddress` for Claude Code; `asana_get_user {"user_id":"me"}`; Fathom `get_identity`; PostHog reports its user in the active-environment block.
