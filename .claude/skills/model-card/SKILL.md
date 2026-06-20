---
name: model-card
description: Generates a model card for a trained model. Use after a model passes evaluation and before it is registered. Produces a standardized card in docs/model-cards/ in the repo voice.
argument-hint: "[model-name]"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Writing a model card

Every model that survives evaluation gets a card in docs/model-cards/. An
unexplained model in production is a liability wearing a lab coat. Write the card in
the repo voice: no em dashes, no emojis, dry and honest.

For model "$ARGUMENTS", produce a card with these sections:

1. What it does, in one paragraph a non-specialist can follow.
2. Intended use and, more importantly, the use it is NOT fit for.
3. Training data: source, DVC version, date range, known biases or gaps.
4. Architecture and key hyperparameters.
5. Evaluation: the metric, the number, the evaluation set, and how the split avoids
   leakage. Include the metric that reflects real cost, for example asymmetric RUL
   error.
6. Limitations and failure modes. Be honest. The sensor configurations it has never
   seen, the regimes where it degrades.
7. Monitoring: which drift signals are watched and what triggers a retrain.
8. Provenance: training run id, git SHA, data version.

A model card that only lists the good numbers is marketing. List the limitations or
do not bother.
