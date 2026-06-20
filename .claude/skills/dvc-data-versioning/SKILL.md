---
name: dvc-data-versioning
description: Procedure for versioning datasets with DVC on a GCS remote so every model traces to its exact training data. Use when adding a dataset, updating one, or wiring the DVC remote.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Versioning data with DVC

Git tracks the code, DVC tracks the data, the GCS remote stores the bytes. The point
is that any model is reproducible from a commit SHA plus a DVC version.

## Procedure

1. The GCS remote is configured once in .dvc/config (committed). Credentials come
   from the environment or a service account, never from this file.
2. Add a dataset with the DVC add flow. This creates a small .dvc pointer file that
   Git tracks. The data itself goes to the remote, not into Git.
3. Commit the .dvc pointer alongside the code change that uses the data, in the same
   logical change, so the link between code and data is in one place.
4. To reproduce, check out the commit and pull the matching data version. If that
   round trip does not give you byte-identical data, the versioning is broken and
   nothing downstream can be trusted.

## Rules

- Raw data is immutable. New data is a new version, never an in-place edit.
- The .dvc files are reviewed like code. A silent data swap is a silent model
  change.
- Document the remote setup in docs/ so a new contributor can pull data on day one
  without a scavenger hunt.
