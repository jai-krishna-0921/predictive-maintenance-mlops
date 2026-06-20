---
description: Run a thorough review of the current diff using the code-reviewer subagent, with extra attention to data leakage.
allowed-tools: Read, Grep, Glob, Bash(git*)
---

## Current diff
!`git diff HEAD`

## Task

Review the changes above. Delegate to the code-reviewer subagent for depth.

Priorities, in order: correctness, data leakage (the silent project-killer in any ML
repo), security and secrets, test coverage, and maintainability.

Give specific, actionable feedback tied to file and line. If it is clean, say what
you checked so the verdict is credible. Do not invent problems to look thorough and
do not soften a real one to be polite.
