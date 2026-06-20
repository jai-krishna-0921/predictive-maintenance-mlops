#!/usr/bin/env bash
# Blocks direct pushes to main or master. Branch, PR, review, merge. That is the deal.
set -euo pipefail
input=$(cat)
cmd=$(echo "$input" | jq -r '.tool_input.command // ""')

if echo "$cmd" | grep -qiE 'git push[^&|]*\b(origin[[:space:]]+)?(main|master)\b'; then
  echo "Blocked: no direct pushes to main/master. Open a branch and a PR like a civilized person." >&2
  exit 2
fi
# Catch a plain 'git push' while HEAD is on main.
if echo "$cmd" | grep -qE 'git push([[:space:]]+origin)?[[:space:]]*$'; then
  branch=$(git -C "${CLAUDE_PROJECT_DIR:-.}" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
  if [ "$branch" = "main" ] || [ "$branch" = "master" ]; then
    echo "Blocked: you are on $branch and trying to push. Branch first." >&2
    exit 2
  fi
fi
exit 0
