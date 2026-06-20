---
description: Create a well-formed GitHub issue from a short description, using the right template and labels.
argument-hint: "[short description]"
allowed-tools: Read, Grep, Glob, Bash(gh*)
---

## Task

Turn this into a proper GitHub issue: $ARGUMENTS

1. Pick the right type: bug, feature, experiment, or chore.
2. Write a title that says what, not "stuff is broken".
3. Fill the body: context, the actual ask, and a definition of done. For an
   experiment issue, include the hypothesis and the metric up front.
4. Apply labels: one `area/*`, one `type/*`, one `priority/*`.
5. Create it with `gh issue create`. No AI attribution in the body.

"Misc fixes" is not an issue. If the description is too vague to write a definition
of done, ask one clarifying question first.
