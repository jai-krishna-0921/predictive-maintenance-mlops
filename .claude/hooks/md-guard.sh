#!/usr/bin/env bash
# Strips em dashes from Markdown after it is written, because the style guide says so
# and because you will forget. Also flags emojis so a human can remove them.
set -euo pipefail
input=$(cat)
file=$(echo "$input" | jq -r '.tool_input.file_path // ""')

[ -z "$file" ] && exit 0
[ ! -f "$file" ] && exit 0
case "$file" in *.md) ;; *) exit 0 ;; esac

# Replace em dash and en dash with a comma-space. Crude but effective.
sed -i 's/[—–]/, /g' "$file" 2>/dev/null || true

# Warn (do not block) if emojis snuck in.
if grep -qP '[\x{1F000}-\x{1FAFF}\x{2600}-\x{27BF}]' "$file" 2>/dev/null; then
  echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUse\",\"additionalContext\":\"Emoji detected in $file. The style guide says no emojis. Remove them.\"}}"
fi
exit 0
