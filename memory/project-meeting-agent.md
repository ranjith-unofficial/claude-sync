---
name: project-meeting-agent
description: "Meeting-intelligence + task-execution agent design (27-28 Aug 2026) — architecture locked, access not yet granted"
metadata: 
  node_type: memory
  type: project
  originSessionId: 63dda3ee-db84-4a08-85de-71768f1a3516
  modified: 2026-08-28T13:23:30.545Z
---

Building an agent that (1) analyzes every meeting for exhaustiveness/what was missed/what he said wrong/better approach/outcomes+next actions, (2) handles Utkarsh's ad-hoc "update/create a sheet" asks, (3) runs start-of-day/end-of-day checklists against what should've happened, (4) sweeps Slack for missed follow-ups and unanswered questions.

**Why:** Ranjith wants this to run continuously without him having to remember to review each meeting or chase follow-ups manually — the acquisition/app-launch workload ([[project-inc42-launch]], [[project-inc42-fy27-plan]]) leaves no slack for manual meeting hygiene.

**How to apply:** This is still in architecture design as of 28 Aug 2026 — nothing built, no access granted yet. Don't assume any part of this is live; confirm current build status before referencing it as working.

## Capability audit (27 Aug 2026) — what's actually connected
- ✅ Fathom MCP — connected, **not yet authorized** (OAuth pending)
- ✅ Wispr Flow MCP — connected, **not yet authorized**
- ✅ Asana MCP — live
- ✅ Google Drive MCP — live
- ❌ **No Slack MCP at all** — can't read his messages or post today
- ❌ **No n8n API/MCP access** — despite [[reference-tools-stack]] listing n8n in his stack, this session has no credentials for it; he must supply base URL + API key (as env vars, not pasted in chat)

## Architecture — locked decisions

**Engine:** n8n (his call), but scoped down to a **Slack-adapter only** (2 workflows: listener + notifier). Everything else (meeting analysis, Asana writes, Sheet writes) runs natively through Claude's own MCP connections — no reason to re-implement reasoning inside an n8n LLM node when Claude already has direct tool access to Fathom/Wispr Flow/Asana/Drive.

**Meeting detection — manual trigger, not calendar-based.** Ranjith posts in Slack after each meeting: which meeting, when, where it's stored (Fathom link / "Wispr Flow" / inline notes if no recording). This replaced an earlier calendar-cross-reference design (calendar = truth for "did it happen," Fathom = truth for "what was said") — dropped because manual trigger is simpler, has no false positive/negative gap-detection, and removes the need for Calendar MCP access entirely. Branch on what he names as the storage location; if unrecognized, ask rather than guess.

**Execution model — ZERO auto-execute, current as of 28 Aug 2026 (supersedes an earlier looser tier model floated mid-design).** Every single action item, no matter how obvious, goes through a per-item approval loop:
- After a meeting, post a Slack summary; each pointer/action item gets its own thread (his term: "CTI").
- Message format per item — **exactly this structure, not generic**: Heading (the specific task, not "New Asana Task") → Execution (exact system action + params: which Asana project, assignee, due date) → Description (what goes in the ticket body).
- Reply "yes" → execute now, confirm in-thread with the created link.
- Reply "yes but X" → apply the amendment, then execute.
- Reply "no" → ask "what should I do instead?" → he answers → repost "Revised approach" in the same format → loop until yes.
- Self-critique content ("did I say something wrong in this meeting") never auto-posts anywhere and never goes in a shared/team-visible place — private to him only, separate from the action-item digest.
- Needs a **state store** — a "Pending Actions" Google Sheet (heading/execution/description/status/thread ID/revision history) since Slack threads alone aren't queryable. Not yet built.

**Utkarsh sheet-request flow:** fetch/create/share directly when the request has enough context (sheet named, columns/data clear); ping Ranjith on Slack (not Utkarsh) when context is missing — he does not want Utkarsh escalated to directly without his say-so. Note: this predates the "zero auto-execute" rule above — needs Ranjith to confirm whether this flow is now also gated behind the yes/no CTI loop, or still allowed to auto-execute on sufficient context as originally stated.

## Open / unresolved
- Slack credential scope: bot token (channels only, **cannot** read his DMs) vs user token (much bigger grant) — flagged to him, not decided
- n8n base URL + API key — not yet provided
- Whether n8n already has Google Sheets/Slack credentials configured, or need setting up
- Sensitive-meeting opt-out (interviews, HR/performance 1:1s) — named as needed, no mechanism designed yet
- Whether the Utkarsh sheet-request flow is exempt from the zero-auto-execute rule (see above)

Related: [[project-personal-ai-ops]] (separate phased daily-brief system), [[project-daily-signal]] (separate briefing artifact), [[project-inc42-ways-of-working]] (Asana Product Master/Backlog conventions this should slot into), [[reference-account-identities]], [[reference-tools-stack]].
