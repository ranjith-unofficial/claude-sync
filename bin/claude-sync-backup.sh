#!/bin/bash
# claude-sync-backup.sh — versioned snapshot of the iCloud store into a local git repo.
# The git repo deliberately lives OUTSIDE iCloud: iCloud corrupts .git pack files.
# Runs at session end (backgrounded) and/or manually. Commits only when something changed.
set -uo pipefail

ICLOUD="$HOME/Library/Mobile Documents/com~apple~CloudDocs/ClaudeSync"
REPO="$HOME/ClaudeSyncBackup"

[ -d "$ICLOUD/memory" ] || exit 0

if [ ! -d "$REPO/.git" ]; then
  mkdir -p "$REPO"
  git -C "$REPO" init -q -b main
  printf '.DS_Store\nsync.log\n*.icloud\n' > "$REPO/.gitignore"
fi

rsync -a --delete \
  --exclude '.DS_Store' --exclude 'sync.log' --exclude '*.icloud' --exclude '.git' --exclude 'node_modules' \
  "$ICLOUD/" "$REPO/"

git -C "$REPO" add -A
if ! git -C "$REPO" diff --cached --quiet; then
  n=$(git -C "$REPO" diff --cached --name-only | wc -l | tr -d ' ')
  git -C "$REPO" -c user.name='Claude Sync' -c user.email='datalabs@inc42.com' \
      commit -q -m "sync: $n file(s) changed — $(date '+%Y-%m-%d %H:%M')"
  echo "committed $n file(s)"
  # push only if a remote is configured
  if git -C "$REPO" remote | grep -q origin; then
    git -C "$REPO" push -q origin main 2>/dev/null && echo "pushed to origin"
  fi
else
  echo "no changes"
fi
