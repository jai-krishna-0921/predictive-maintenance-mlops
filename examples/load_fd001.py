"""Load the FD001 subset and print a quick summary.

This needs the data present (see configs/data.yaml and the DVC setup). With the
package installed in editable mode, run it from the repo root:

    python examples/load_fd001.py --config configs/data.yaml
"""

from __future__ import annotations

import argparse

from features.loader import load_config, load_fd001


def main() -> None:
    """Parse arguments, load FD001, and print a one-screen summary."""
    parser = argparse.ArgumentParser(description="Load and summarize C-MAPSS FD001.")
    parser.add_argument(
        "--config",
        default="configs/data.yaml",
        help="Path to the data config (default: configs/data.yaml).",
    )
    args = parser.parse_args()

    dataset = load_fd001(load_config(args.config))
    train, test = dataset.train, dataset.test

    print(f"train: {len(train):>6} rows, {train['unit_number'].nunique():>3} engines")
    print(f"test:  {len(test):>6} rows, {test['unit_number'].nunique():>3} engines")
    print(f"train RUL range: {train['RUL'].min()} to {train['RUL'].max()} cycles")
    print("\nfirst rows of train:")
    print(train.head().to_string(index=False))


if __name__ == "__main__":
    main()
