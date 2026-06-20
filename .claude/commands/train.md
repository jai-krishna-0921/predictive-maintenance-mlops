---
description: Launch a training run for one of the three models with the full logging contract enforced.
argument-hint: "[anomaly|rul|fault]"
allowed-tools: Read, Grep, Glob, Bash
---

## Task

Run training for the $ARGUMENTS model.

1. Read the experiment-logging skill and confirm the run will log data version, code
   version, hyperparameters, seed, and metrics. If the training code does not log
   all of it, fix that first. An unlogged run is wasted compute.
2. Confirm the DVC data version is pinned and clean.
3. Launch the run.
4. When it finishes, report the metric that reflects real cost (for RUL, the
   asymmetric error), the experiment run id, and an honest call on whether this is
   register-worthy or just another data point.

Delegate the actual modeling decisions to the ml-trainer subagent if the task needs
real depth.
