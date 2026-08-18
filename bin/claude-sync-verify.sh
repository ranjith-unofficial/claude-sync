#!/bin/bash
# claude-sync-verify.sh — confirm this Mac is correctly wired to the shared store.
ICLOUD="$HOME/Library/Mobile Documents/com~apple~CloudDocs/ClaudeSync"
CLAUDE="$HOME/.claude"
SLUG="$(echo "$HOME" | tr '/' '-')"
fail=0

check() {
  local live="$1" target="$2" label="$3"
  if [ -L "$live" ] && [ "$(readlink "$live")" = "$target" ] && [ -e "$live" ]; then
    printf '  OK    %s\n' "$label"
  else
    printf '  FAIL  %s\n' "$label"; fail=1
  fi
}

echo "Shared store: $ICLOUD"
[ -d "$ICLOUD/memory" ] || { echo "  FAIL  store not present — iCloud still downloading?"; exit 1; }
echo
echo "Links:"
check "$CLAUDE/projects/$SLUG/memory" "$ICLOUD/memory"                    "memory"
check "$CLAUDE/skills"                "$ICLOUD/skills"                    "skills"
check "$CLAUDE/settings.json"         "$ICLOUD/settings/settings.json"    "settings.json"
check "$CLAUDE/settings.local.json"   "$ICLOUD/settings/settings.local.json" "settings.local.json"
check "$CLAUDE/CLAUDE.md"             "$ICLOUD/CLAUDE.md"                 "CLAUDE.md"
check "$HOME/ClaudeDocs"              "$ICLOUD/outputs"                   "ClaudeDocs"

echo
echo "Contents:"
printf '  %s memory files\n'  "$(ls -1 "$ICLOUD/memory"/*.md 2>/dev/null | wc -l | tr -d ' ')"
printf '  %s skills\n'        "$(ls -1 "$ICLOUD/skills" 2>/dev/null | wc -l | tr -d ' ')"
printf '  %s output files\n'  "$(find "$ICLOUD/outputs" -type f 2>/dev/null | wc -l | tr -d ' ')"
stubs=$(find "$ICLOUD" -name '*.icloud' 2>/dev/null | wc -l | tr -d ' ')
printf '  %s files still downloading from iCloud\n' "$stubs"

echo
echo "Hooks:"
if command -v jq >/dev/null 2>&1 && jq -e '.hooks.SessionStart and .hooks.Stop' "$CLAUDE/settings.json" >/dev/null 2>&1; then
  echo "  OK    SessionStart + Stop configured"
else
  echo "  FAIL  hooks missing from settings.json"; fail=1
fi

echo
[ "$fail" -eq 0 ] && [ "$stubs" -eq 0 ] && echo "All good." || echo "Issues above — re-run claude-sync-link.sh, or wait for iCloud to finish."
