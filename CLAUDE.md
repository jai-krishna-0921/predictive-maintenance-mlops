# CLAUDE.md

This is the constitution for this repository. Read it, follow it, and do not get
creative about the parts that say "never". If something here is wrong or outdated,
fix the file, do not quietly ignore it.

## What this project is

A predictive maintenance platform for industrial turbofan engines. It ingests
streaming sensor data, flags anomalies before failure, predicts Remaining Useful
Life (RUL), classifies the developing fault, and surfaces all of it to an engineer
on a dashboard. Three cooperating models, a streaming pipeline, real-time serving,
drift monitoring. It is a system, not a notebook.

Stack: Python, GCP (Pub/Sub, Dataflow, Vertex AI Pipelines, Endpoints, Model
Registry, Model Monitoring), DVC on GCS, Cloud Build, Cloud Run, BigQuery.

For the actual architecture, read `docs/architecture.md`. Do not infer it from
vibes.

## Golden rules (the non-negotiable kind)

1. **No co-authors on commits.** Ever. Do not add `Co-Authored-By:` trailers. Do
   not append "Generated with Claude Code", "Co-authored-by: Claude", or any other
   tool attribution to commit messages, PR descriptions, or issue bodies. The
   author of record is the human. A hook enforces this, but do not make the hook
   do your job.

2. **Every change traces to an issue.** No orphan commits. If you are about to do
   work that does not have a GitHub issue, create one first using the issue
   templates in `.github/ISSUE_TEMPLATE/`. Reference it in the branch name and the
   PR. "Misc fixes" is not an issue.

3. **Never commit secrets.** No keys, no service account JSON, no `.env` contents,
   no tokens. A hook scans for this, but if you are pasting a private key into a
   file you have already made a mistake the hook is just cleaning up after.

4. **Never push straight to `main`.** Branch, PR, review, merge. A hook blocks
   direct pushes to `main` and `master`. This is not negotiable even for a
   one-line README typo.

5. **Tests ship with the code that needs them.** A model training change without a
   test is an incomplete change, not a fast one.

## Commit conventions

Conventional Commits, lowercase, imperative, scoped:

    feat(rul): add lstm baseline for remaining useful life
    fix(serving): handle empty sensor batch without 500
    docs(readme): document the dvc remote setup
    chore(ci): cache pip wheels in cloud build

Small, atomic commits. One logical change each. If the commit message needs the
word "and", it is probably two commits.

## Issue-driven workflow

- One issue per unit of work. Use the templates: bug, feature, experiment, chore.
- Label everything: `area/data`, `area/training`, `area/serving`,
  `area/monitoring`, `area/infra`, plus `type/*` and `priority/*`.
- Experiments get an experiment issue that records the hypothesis, the metric, and
  the result. A failed experiment is still a closed issue with a write-up, not a
  ghost.
- Branch names: `<type>/<issue-number>-<slug>`, for example
  `feat/42-rul-lstm-baseline`.
- PRs reference the issue with `Closes #42` and explain what and why, not just
  what. The diff already says what.

## Code conventions

- Python 3.11+. Type hints on every public function. No bare `except`.
- Formatting and linting: `ruff format` and `ruff check --fix`. A hook runs these
  after edits, so do not hand-align anything; the tool wins.
- Docstrings on every module, class, and public function. Say what it does and why
  it exists, not "this is a function".
- No notebooks in `src/`. Exploration lives in `notebooks/` and never imports the
  other way around.
- Config over hardcoding. Paths, bucket names, and hyperparameters live in config
  files, not buried in a training script as a magic number on line 217.

## Documentation standards

The repo should make a stranger think "this person knows what they are doing"
within thirty seconds of landing on it. That means:

- A root `README.md` that explains the problem, the architecture, how to run it,
  and what good looks like. With a diagram.
- A `README.md` in every meaningful directory explaining what lives there and why.
- An `examples/` directory with runnable examples, not snippets that assume six
  undocumented environment variables.
- A `scripts/` directory with setup, teardown, and common-task scripts, each with
  a `--help`.
- `docs/` with architecture, data dictionary, model cards, and runbooks.
- Every model gets a model card. No exceptions. An unexplained model in production
  is a liability wearing a lab coat.

## Markdown voice (this matters more than you think)

Every Markdown file you generate follows this voice. The README is the first
impression and most of them read like a microwave manual. Do better.

- **No em dashes.** None. Use a comma, a colon, parentheses, or just two sentences.
  If you find yourself reaching for one, restructure the sentence. A hook strips
  them after the fact, but write without them in the first place.
- **No emojis.** Not in headings, not as bullet points, not as a cute little
  rocket next to "Getting Started". This is engineering documentation, not a
  birthday card.
- **Sarcastic but useful.** Dry, a little wry, human. The reader is a competent
  adult. You can have a sense of humor as long as the information is correct and
  complete. Wit is not a substitute for accuracy, it is a garnish.
- **No corporate sludge.** Ban "leverage", "utilize" (the word is "use"),
  "seamless", "robust solution", "in today's fast-paced world", and anything that
  sounds like it was written to hit a word count.
- **No AI throat-clearing.** No "As an AI", no "I hope this helps", no "Certainly!".
  Write like a senior engineer who is mildly annoyed but fundamentally helpful.
- Write for someone smart who is new to this repo, not for someone who already
  knows the answer.

## Repository structure (keep it this way)

    .
    ├── README.md
    ├── CLAUDE.md
    ├── docs/                 architecture, data dictionary, model cards, runbooks
    ├── src/
    │   ├── ingestion/        pub/sub + dataflow streaming
    │   ├── features/         feature engineering, shared by train and serve
    │   ├── models/           anomaly, rul, fault classifier
    │   ├── pipelines/        vertex ai pipeline definitions
    │   ├── serving/          endpoint + batch prediction
    │   └── monitoring/       drift detection, alerting
    ├── tests/                mirrors src/
    ├── examples/             runnable end-to-end examples
    ├── scripts/              setup, deploy, common tasks (each with --help)
    ├── notebooks/            exploration only, never imported by src
    ├── configs/              hyperparameters, paths, env configs
    ├── .github/              issue templates, PR template, workflows
    └── .claude/              the harness that built all of the above

## Definition of done

A change is done when: it closes an issue, it has tests that pass, it is formatted
and linted clean, it has docs or a docstring update, the PR explains the why, and
nothing secret or co-authored snuck into the history. Not before.

## The harness

This repo ships its own Claude Code harness in `.claude/`. Subagents for the
specialist roles, skills for the repeatable MLOps procedures, commands for the
common verbs, hooks for the guardrails. Use them. The index lives in
`.claude/README.md`. If you are doing something repeatable by hand for the third
time, it should have been a skill the first time.
