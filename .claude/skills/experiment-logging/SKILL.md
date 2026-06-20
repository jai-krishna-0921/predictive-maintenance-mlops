---
name: experiment-logging
description: The logging contract every training run must follow so results are reproducible and comparable. Use when writing or reviewing training code, or when a run cannot be reproduced.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Experiment logging contract

An unlogged run did not happen. Every training run logs the following or it does not
get to claim a result.

## Must log

- Data version (the DVC hash). Not "the latest data". The exact version.
- Code version (git SHA, and whether the tree was dirty).
- All hyperparameters, including the ones you think do not matter.
- The random seed.
- Every metric you care about, plus the ones you will wish you had logged later.
- The evaluation set identifier, so two runs are actually comparable.

## Why this is not optional

Three weeks from now you will have a folder full of runs and a vague memory that one
of them was good. Without this contract, that memory is all you have, and it is
wrong. With it, you query the tracker and reproduce the winner in one command.

When reviewing training code, reject anything that trains without logging this. It is
a missing seatbelt, not a style preference.
