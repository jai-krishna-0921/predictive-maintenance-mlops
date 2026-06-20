---
name: vertex-pipeline
description: Procedure for defining, compiling, and running a Vertex AI Pipeline in this repo. Use when adding or changing a training, evaluation, or registration pipeline. Covers component structure, containerization, and the promotion gate.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Building a Vertex AI Pipeline

Pipelines live in src/pipelines/. Each is a Kubeflow pipeline compiled to JSON and
submitted to Vertex AI. Follow this exactly so every pipeline looks the same and the
next person does not have to reverse-engineer your style.

## Steps

1. One component per logical step: ingest, validate-data, train, evaluate,
   register. Each component is a containerized function with pinned inputs and
   outputs. No giant do-everything step.
2. Pin the base image and dependencies per component. Reproducibility is the whole
   point. A floating `latest` tag defeats it.
3. Pass artifacts between steps as typed pipeline artifacts, not by writing to a
   hardcoded bucket path and hoping.
4. The evaluate step emits the metric. The register step has a conditional: register
   and stage the model only if it beats the current production metric. That
   conditional is the promotion gate and it is not optional.
5. Compile the pipeline, commit the compiled spec, and submit via the run command.
6. Tag every pipeline run with the git SHA and the DVC data version.

## Definition of done for a pipeline change

It compiles, it runs end to end on a small sample, the promotion gate works (test it
by feeding it a deliberately worse model and confirming it refuses to promote), and
src/pipelines/README.md documents the DAG.
