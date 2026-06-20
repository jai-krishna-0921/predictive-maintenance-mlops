# configs

Configuration that should not be buried as a magic number on line 217 of a training
script. Paths, bucket names, and hyperparameters live here so changing them is a
config edit, not a code change.

## What is here now

- `data.yaml`: where the C-MAPSS files live. The loader resolves every path against
  `data_dir`, so pointing at a different location (a laptop, a bucket mount, a CI
  fixture) is a one-line change.

## Conventions

- One file per concern. Data paths, model hyperparameters, and serving settings do
  not belong in the same file.
- No secrets. Tokens, keys, and service-account JSON never go in a config file. They
  come from environment variables or a secret manager.
