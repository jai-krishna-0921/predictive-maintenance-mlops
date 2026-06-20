---
description: Evaluate a candidate model against the production gate and report whether it should be promoted.
argument-hint: "[model-name]"
allowed-tools: Read, Grep, Glob, Bash
---

## Task

Evaluate the candidate model "$ARGUMENTS" against the promotion gate.

1. Run evaluation on the fixed held-out set. Confirm the split has no leakage.
2. Compare against the current production model on the metric that matters.
3. State the result plainly: promote or do not promote, and by what margin.
4. If it should be promoted, generate the model card via the model-card skill before
   anything is registered.

Do not promote on a tie or a rounding error. The gate exists to keep marginally
worse models out of production, not to wave them through.
