# ClaudeSync — shared Claude Code memory across Macs

## What's shared

| Path in this folder | Symlinked from | What it is |
|---|---|---|
| `memory/` | `~/.claude/projects/<home-slug>/memory` | 49 memory files + MEMORY.md index |
| `skills/` | `~/.claude/skills` | cybersecurity, fitness-nutrition, marketing, ui-ux-pro-max |
| `settings/settings.json` | `~/.claude/settings.json` | effort level, theme, TUI, hooks |
| `settings/settings.local.json` | `~/.claude/settings.local.json` | permission allowlist |

**Not** shared, on purpose: session transcripts, `history.jsonl`, caches, `file-history`, daemon logs. That's ~529 MB of machine-local junk.

## Setup on the second Mac

1. Sign into the same iCloud account. Open Finder → iCloud Drive → wait for `ClaudeSync` to finish downloading.
2. Install Claude Code and log in.
3. Run:

   ```
   bash ~/Library/Mobile\ Documents/com~apple~CloudDocs/ClaudeSync/bin/claude-sync-link.sh
   ```

4. Restart Claude Code.

The script auto-detects the username, so a different home dir on Mac 2 is fine. Anything it replaces is parked in `~/.claude/pre-sync-backup-<timestamp>/` — nothing is deleted.

## How it stays in sync

- **iCloud** syncs the files continuously. No command to run.
- **SessionStart hook** (`claude-sync-guard.sh`) forces iCloud to download any evicted file and repairs a symlink if an app replaced it with a real file — preserving the newer content, not overwriting it.
- **Stop hook** (`claude-sync-backup.sh`) commits a snapshot to `~/ClaudeSyncBackup` (a git repo, local to each Mac). Runs backgrounded; commits only when something changed.

Manual snapshot any time:

```
bash ~/Library/Mobile\ Documents/com~apple~CloudDocs/ClaudeSync/bin/claude-sync-backup.sh
```

## The one rule

**Don't run Claude Code on both Macs at the same time.** iCloud resolves simultaneous edits to the same file by creating a "conflicted copy" instead of merging. One Mac at a time and this never happens.

If a conflicted copy does appear in `memory/`, the git history in `~/ClaudeSyncBackup` tells you which version is which:

```
git -C ~/ClaudeSyncBackup log --oneline -- memory/<file>.md
git -C ~/ClaudeSyncBackup show <commit>:memory/<file>.md
```

## Why git isn't inside this folder

iCloud evicts and re-materialises files on its own schedule, which corrupts git pack files. The repo lives at `~/ClaudeSyncBackup`, outside iCloud, and rsyncs from here.

## Optional: off-machine backup

The backup script pushes automatically if a remote exists. To add a **private** GitHub repo (this content is INC42-confidential — private only):

```
git -C ~/ClaudeSyncBackup remote add origin git@github.com:<you>/claude-memory.git
git -C ~/ClaudeSyncBackup push -u origin main
```

## Undo

```
rm ~/.claude/settings.json ~/.claude/settings.local.json ~/.claude/skills
rm ~/.claude/projects/<home-slug>/memory
mv ~/.claude/pre-sync-backup-<timestamp>/* ~/.claude/
```
