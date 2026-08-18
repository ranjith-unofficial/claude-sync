#!/bin/bash
# claude-sync-guard.sh — runs at SessionStart. Two jobs:
#   1. Force iCloud to materialise the store (defeats "Optimize Mac Storage" eviction).
#   2. Repair any symlink that an app replaced with a real file, WITHOUT losing the new content.
# Never blocks, never fails the session.

ICLOUD="$HOME/Library/Mobile Documents/com~apple~CloudDocs/ClaudeSync"
CLAUDE="$HOME/.claude"
SLUG="$(echo "$HOME" | tr '/' '-')"
PROJ="$CLAUDE/projects/$SLUG"
LOG="$ICLOUD/sync.log"

[ -d "$ICLOUD" ] || exit 0

# 1. pull down any evicted (.icloud placeholder) files
if command -v brctl >/dev/null 2>&1; then
  brctl download "$ICLOUD" >/dev/null 2>&1 &
fi

# 2. heal broken links
heal() {
  local live="$1" target="$2"
  # symlink pointing at the right place -> nothing to do
  if [ -L "$live" ] && [ "$(readlink "$live")" = "$target" ]; then return; fi
  # a real file/dir appeared where the link should be: its content is NEWER, keep it
  if [ -e "$live" ] && [ ! -L "$live" ]; then
    if [ -d "$live" ]; then rsync -a "$live/" "$target/"; else cp -f "$live" "$target"; fi
    rm -rf "$live"
    echo "$(date '+%F %T') healed (content preserved): $live" >> "$LOG"
  fi
  mkdir -p "$(dirname "$live")"
  ln -sfn "$target" "$live"
}

heal "$PROJ/memory"                "$ICLOUD/memory"
heal "$CLAUDE/skills"              "$ICLOUD/skills"
heal "$CLAUDE/settings.json"       "$ICLOUD/settings/settings.json"
heal "$CLAUDE/settings.local.json" "$ICLOUD/settings/settings.local.json"
heal "$CLAUDE/CLAUDE.md"           "$ICLOUD/CLAUDE.md"
heal "$HOME/ClaudeDocs"            "$ICLOUD/outputs"

exit 0
