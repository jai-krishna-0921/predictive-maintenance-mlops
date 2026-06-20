---
name: release-notes
description: Generates release notes and a changelog entry from merged PRs and closed issues since the last tag. Use when cutting a release. Writes in the repo voice, groups by area, credits no AI.
argument-hint: "[version]"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Writing release notes

For version "$ARGUMENTS", build release notes from the issues and PRs closed since
the last tag.

## Procedure

1. Find the last tag and collect merged PRs and closed issues since then.
2. Group by area: data, training, serving, monitoring, infra, docs.
3. For each entry, write one line a human can understand. "Fixed bug" tells no one
   anything. "Serving no longer returns 500 on an empty sensor batch" tells them
   what changed and whether they care.
4. Call out breaking changes loudly at the top. A breaking change buried at the
   bottom is an ambush.
5. Write it in the repo voice: no em dashes, no emojis, dry and clear.

Do not credit Claude, do not add a tool attribution line, do not thank the AI. The
release was shipped by people. The notes read that way.
