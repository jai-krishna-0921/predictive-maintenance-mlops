#!/usr/bin/env bash
# Blocks git commits that carry co-author trailers or tool attribution.
# The author of record is the human. No exceptions, no "Generated with".
set -euo pipefail
input=$(cat)
cmd=$(echo "$input" | jq -r '.tool_input.command // ""')

if echo "$cmd" | grep -qiE 'co-authored-by:|generated with claude|co-authored-by: claude|🤖'; then
  echo "Blocked: commit contains a co-author trailer or tool attribution. Strip it. This repo has no co-authors." >&2
  exit 2
fi
exit 0
