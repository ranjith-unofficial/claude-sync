---
name: reference-claude-sync-setup
description: Claude Code memory/skills/settings are symlinked into iCloud ClaudeSync and shared across two Macs; git backup at ~/ClaudeSyncBackup
metadata: 
  node_type: memory
  type: reference
  originSessionId: 5bdb3b70-219f-44d8-b26b-6cadc2486226
  modified: 2026-08-17T18:31:44.829Z
---

Set up 18 Aug 2026 so Ranjith's two Macs share one Claude Code memory.

**Live store:** `~/Library/Mobile Documents/com~apple~CloudDocs/ClaudeSync/` — iCloud syncs it continuously.

Six symlinks point the local Claude install at it:
- `~/.claude/projects/<home-slug>/memory` → `ClaudeSync/memory`
- `~/.claude/skills` → `ClaudeSync/skills`
- `~/.claude/settings.json` → `ClaudeSync/settings/settings.json`
- `~/.claude/settings.local.json` → `ClaudeSync/settings/settings.local.json`
- `~/.claude/CLAUDE.md` → `ClaudeSync/CLAUDE.md`
- `~/ClaudeDocs` → `ClaudeSync/outputs`

So **editing a memory file edits the shared copy on both Macs**. Session transcripts, history, and caches are deliberately NOT shared.

**Generated deliverables (PDF/HTML/DOCX) go in `~/ClaudeDocs/<project>/`** — subfolders inc42, nexloid, personal, workshops. The synced `CLAUDE.md` instructs every session on both Macs to save there, so files sync by construction rather than by remembering. `~/Downloads` is deliberately excluded from sync: it holds invoices, Aadhaar, and bank PDFs that must not go into iCloud.

**Scripts** in `ClaudeSync/bin/`: `claude-sync-link.sh` (one-time per Mac, auto-detects username), `claude-sync-guard.sh` (SessionStart hook — un-evicts iCloud files, repairs symlinks an app replaced with real files), `claude-sync-backup.sh` (Stop hook — git snapshot).

**Git backup:** `~/ClaudeSyncBackup`, deliberately OUTSIDE iCloud because iCloud corrupts `.git` pack files. **Still NO GitHub remote as of 2026-09-06** — the Stop hook commits locally only. An attempt to create a private `ranjith-unofficial/claude-sync` repo from a session was blocked by the permission classifier; Ranjith has to create it and run `git -C ~/ClaudeSyncBackup remote add origin <url> && git -C ~/ClaudeSyncBackup push -u origin main` himself. The content is INC42-confidential so the repo must be private.

**The one failure mode:** running Claude Code on both Macs simultaneously makes iCloud write "conflicted copy" files instead of merging. One Mac at a time.

Related: [[reference-tools-stack]], [[feedback-shared-system-safety]]

**Source-document rule (added 2026-09-06, before Ranjith moved to another laptop).** Any file a memory cites must live inside the synced store, never in `~/Downloads`, `~/Documents`, or `~/.claude/plans`. On 6 Sep every still-existing cited file was copied in and the memory paths rewritten:
- `~/ClaudeDocs/inc42/sources/` — Utkarsh's 4 strategy docs, PostHog Review, App v2 Scope, Agent Platform Brief, FY27 Plan xlsx (`PMTD MOP 2026.xlsx`), Funnel State, Ashish release brief PDF, Master PRD exports, Website events xlsx, APM JD, platform comparisons, AskInc42 KB v1 files, Dhruv's resume.
- `~/ClaudeDocs/inc42/AskInc42_Knowledge/` — the 9-doc knowledge repo (was `~/Documents/AskInc42_Knowledge`).
- `~/ClaudeDocs/inc42/plans/` — Claude plan files (was `~/.claude/plans`).
- `~/ClaudeDocs/inc42/askinc42-variants/` — 7 AskInc42 entry-point PNGs from a job tmp dir.
- `~/ClaudeDocs/personal/` — fitness scale photos, workout program, health dashboard spec.

Cited files that no longer exist anywhere on the Mac (lost when a session ran `rm -f ~/Downloads/*.csv`, or never kept): `DPDP_Input Sheet - Inc42 FILLED.xlsx`, `Comparison - Sheet1.csv`, `42_posts (1).csv`, `p (4).csv`, `inc42_brief_scorer.py`. Deliberately NOT synced: `hiring-agent-workflow.json` (plaintext Keka OAuth secret — see [[reference-inc42-keka-api-access]]).

**Not covered by iCloud, must be redone on a new laptop:** Claude login; `~/.claude.json` MCP servers (mobbin global; figma, notion, asana are project-scoped to `/Users/thrillophilia`, so the username must match or they must be re-added); the `posthog` plugin; the Claude-in-Chrome extension; `git clone` of `~/inc42-context` (GitHub repo is actually `ranjith-unofficial/master-brain`, despite the skill saying `inc42-context`) because the SessionEnd hook calls `$HOME/inc42-context/bin/capture-session.sh`; a github.com credential in Keychain; then run `ClaudeSync/bin/claude-sync-link.sh`.
