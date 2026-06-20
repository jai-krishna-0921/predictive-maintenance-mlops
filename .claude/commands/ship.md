---
description: Stage, commit with a conventional message, and open a PR that references the issue. Enforces no co-author trailers.
argument-hint: "[issue-number]"
allowed-tools: Read, Grep, Glob, Bash(git*), Bash(gh*)
---

## Current state
- Branch: !`git rev-parse --abbrev-ref HEAD`
- Status: !`git status --short`
- Diff: !`git diff --stat`

## Task

Ship the current work for issue #$ARGUMENTS.

1. Confirm we are not on main or master. If we are, stop and tell the user to branch.
2. Stage the relevant changes. Do not blindly `git add .` if there is junk in the
   tree; stage what belongs to this change.
3. Write a Conventional Commit message: lowercase, imperative, scoped. One logical
   change. No "and" smuggling two changes into one commit.
4. The commit message has NO co-author trailer, NO "Generated with Claude Code", and
   NO tool attribution of any kind. The author is the human. The hook will block you
   if you forget, but do not make it.
5. Push the branch and open a PR with `gh`. The PR body explains what changed and
   why, and ends with `Closes #$ARGUMENTS`. No AI credit in the PR body either.
