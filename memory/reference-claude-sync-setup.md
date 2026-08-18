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

**Git backup:** `~/ClaudeSyncBackup`, deliberately OUTSIDE iCloud because iCloud corrupts `.git` pack files. No GitHub remote configured yet; the content is INC42-confidential so any remote must be private.

**The one failure mode:** running Claude Code on both Macs simultaneously makes iCloud write "conflicted copy" files instead of merging. One Mac at a time.

Related: [[reference-tools-stack]], [[feedback-shared-system-safety]]
