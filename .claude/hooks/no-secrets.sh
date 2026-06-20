#!/usr/bin/env bash
# Scans content being written for things that look like secrets. Better paranoid than leaked.
set -euo pipefail
input=$(cat)
content=$(echo "$input" | jq -r '(.tool_input.content // .tool_input.new_string // "")')

# Common secret shapes: private keys, GCP SA keys, generic API tokens, AWS keys.
patterns='-----BEGIN [A-Z ]*PRIVATE KEY-----|"type":[[:space:]]*"service_account"|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|ghp_[0-9A-Za-z]{36}|sk-[0-9A-Za-z]{32,}'

if echo "$content" | grep -qE "$patterns"; then
  echo "Blocked: this write looks like it contains a secret (private key, service account, or API token). Use an env var or a secret manager." >&2
  exit 2
fi
exit 0
