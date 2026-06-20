---
description: Deploy a registered model to a Vertex AI Endpoint. Asks for confirmation because this touches production.
argument-hint: "[model-version]"
allowed-tools: Read, Grep, Glob, Bash
---

## Task

Deploy model version "$ARGUMENTS" to serving.

1. Confirm the model is registered and passed the gate. Do not deploy a model that
   skipped evaluation.
2. Confirm monitoring is wired for this model before it serves traffic, not after.
   A model in production with no drift monitoring is an outage scheduled for later.
3. Deploy. The permission rules will ask before any gcloud deploy command runs;
   that prompt is intentional, do not try to route around it.
4. Report the endpoint, the rollback command, and how to confirm it is healthy.

If anything is missing (no gate result, no monitoring, no rollback plan), stop and
say so. Shipping fast is not the same as shipping blind.
