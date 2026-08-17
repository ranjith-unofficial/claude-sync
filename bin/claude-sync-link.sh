#!/bin/bash
# claude-sync-link.sh — point this Mac's Claude Code at the shared iCloud store.
# Safe to re-run. Run once on each Mac. Auto-detects the username/home dir.
set -euo pipefail

ICLOUD="$HOME/Library/Mobile Documents/com~apple~CloudDocs/ClaudeSync"
CLAUDE="$HOME/.claude"
SLUG="$(echo "$HOME" | tr '/' '-')"            # /Users/foo -> -Users-foo
PROJ="$CLAUDE/projects/$SLUG"
STAMP="$(date +%Y%m%d-%H%M%S)"
PARK="$CLAUDE/pre-sync-backup-$STAMP"

if [ ! -d "$ICLOUD/memory" ]; then
  echo "ERROR: $ICLOUD/memory not found."
  echo "iCloud may still be downloading. Open the ClaudeSync folder in Finder, wait, then re-run."
  exit 1
fi

echo "Home:        $HOME"
echo "Project dir: $PROJ"
echo

# --- link one path into the shared store, parking whatever is already there ---
link() {
  local live="$1" target="$2"
  if [ -L "$live" ]; then
    if [ "$(readlink "$live")" = "$target" ]; then echo "ok   (already linked)  $live"; return; fi
    rm "$live"
  elif [ -e "$live" ]; then
    mkdir -p "$PARK/$(dirname "${live#$CLAUDE/}")"
    mv "$live" "$PARK/${live#$CLAUDE/}"
    echo "park (moved aside)    $live"
  fi
  mkdir -p "$(dirname "$live")"
  ln -s "$target" "$live"
  echo "link                  $live"
}

mkdir -p "$PROJ"
link "$PROJ/memory"                "$ICLOUD/memory"
link "$CLAUDE/skills"              "$ICLOUD/skills"
link "$CLAUDE/settings.json"       "$ICLOUD/settings/settings.json"
link "$CLAUDE/settings.local.json" "$ICLOUD/settings/settings.local.json"

echo
[ -d "$PARK" ] && echo "Previous local copies parked in: $PARK"
echo "Done. Restart Claude Code so it re-reads settings."
