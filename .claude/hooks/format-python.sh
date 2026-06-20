#!/usr/bin/env bash
# Formats and autofixes the Python file that was just written. The tool wins, not your indentation.
set -euo pipefail
input=$(cat)
file=$(echo "$input" | jq -r '.tool_input.file_path // ""')

[ -z "$file" ] && exit 0
[ ! -f "$file" ] && exit 0
case "$file" in *.py) ;; *) exit 0 ;; esac

if command -v ruff >/dev/null 2>&1; then
  ruff format "$file" >/dev/null 2>&1 || true
  ruff check --fix "$file" >/dev/null 2>&1 || true
fi
exit 0
