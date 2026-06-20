# The harness

This is the Claude Code setup that builds and maintains this repo. It exists so the
work is consistent, the guardrails are enforced by machines instead of memory, and
nobody has to re-explain the conventions every session.

## Subagents (.claude/agents/)

Specialists with their own context windows. The main session delegates to them.

- data-engineer: streaming, features, DVC, BigQuery
- ml-trainer: the three models, tuning, experiment logging
- mlops-pipeline-engineer: Vertex pipelines, registry, CI/CD, promotion gates
- gcp-architect: Terraform, IAM, service choices, cost (opus)
- code-reviewer: correctness, leakage, security, tests (opus)
- test-author: tests that actually catch regressions
- docs-writer: docs in the house voice
- monitoring-engineer: drift, alerting, dashboards
- experiment-analyst: reads results, tells the truth about them
- security-auditor: secrets, IAM, supply chain (opus)

## Skills (.claude/skills/)

Repeatable procedures. Invoke with /name or let Claude pick them up by description.

- vertex-pipeline: how to build a pipeline here
- dvc-data-versioning: how to version data here
- model-card: generate a model card after evaluation
- experiment-logging: the logging contract every run follows
- release-notes: changelog from issues and PRs

## Commands (.claude/commands/)

The common verbs.

- /ship [issue]: commit (conventional, no co-author) and open a PR
- /issue [desc]: create a well-formed GitHub issue
- /train [anomaly|rul|fault]: launch a logged training run
- /evaluate [model]: check a candidate against the promotion gate
- /deploy [version]: deploy to an endpoint, with confirmation
- /review: thorough diff review with leakage focus

## Hooks (.claude/hooks/), wired in settings.json

The guardrails. These run automatically.

- block-coauthor: blocks commits with co-author trailers or tool attribution
- protect-main: blocks direct pushes to main/master
- no-secrets: blocks writes that look like keys or service accounts
- format-python: runs ruff format and fix after Python edits
- md-guard: strips em dashes from Markdown, flags emojis
- done-checklist: end-of-turn reminder of the definition of done

## A note on the guardrails

The hooks are a safety net, not a substitute for doing it right. If you are relying
on the co-author hook to catch you every time, you have already half-internalized
the wrong habit. Write it correctly, let the hook catch the slip.
