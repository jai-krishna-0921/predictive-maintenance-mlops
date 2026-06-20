# features

The feature path shared by training and serving. Whatever turns raw sensor rows
into model inputs lives here, and both the training pipeline and the serving code
import it, so the two cannot compute features differently and drift apart.

## What is here now

- `loader.py`: parses the C-MAPSS space-separated files into typed dataframes with
  the data-dictionary column names, derives per-row RUL for training trajectories,
  and attaches the provided ground-truth RUL for test trajectories. Paths come from
  `configs/data.yaml`, not from hardcoded strings.

## What is coming

The actual feature engineering from Phase 1: dropping the dead sensors, rolling
window statistics, and per-regime normalization. It will sit next to the loader and
consume its output.

## Usage

```python
from features.loader import load_config, load_fd001

dataset = load_fd001(load_config("configs/data.yaml"))
print(dataset.train.shape, dataset.test.shape)
```

The loader reads from `data/` (gitignored, pulled with DVC), so you need the data
present before the call returns anything. See the repo README for the data setup.
