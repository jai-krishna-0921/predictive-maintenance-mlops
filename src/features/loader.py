"""Load NASA C-MAPSS turbofan files into typed dataframes.

The C-MAPSS files are space separated, carry no header, and hold 26 columns: the
engine unit number, the cycle counter, three operational settings, and 21 sensor
channels. This module parses them into pandas dataframes with the names from the
data dictionary, derives remaining useful life (RUL) for training trajectories,
and attaches the provided ground-truth RUL for test trajectories.

It exists so every downstream consumer reads the data the same way, instead of
reinventing the parsing and letting the column names quietly drift apart.

Example:
    from features.loader import load_config, load_fd001

    dataset = load_fd001(load_config("configs/data.yaml"))
    print(dataset.train.shape, dataset.test.shape)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import yaml

# Column schema from the data dictionary. This is the data spec, not a tunable, so
# it lives in code rather than in a config file.
INDEX_COLUMNS: tuple[str, ...] = ("unit_number", "time_cycles")
SETTING_COLUMNS: tuple[str, ...] = ("op_setting_1", "op_setting_2", "op_setting_3")
SENSOR_COLUMNS: tuple[str, ...] = tuple(f"sensor_{i}" for i in range(1, 22))
COLUMN_NAMES: tuple[str, ...] = INDEX_COLUMNS + SETTING_COLUMNS + SENSOR_COLUMNS

EXPECTED_COLUMN_COUNT = 26  # 2 index + 3 settings + 21 sensors

RUL_COLUMN = "RUL"


@dataclass(frozen=True)
class DataConfig:
    """Filesystem paths for one C-MAPSS subset.

    Attributes:
        train_path: Run-to-failure training trajectories.
        test_path: Test trajectories that stop before failure.
        rul_path: Ground-truth remaining useful life, one value per test unit.
    """

    train_path: Path
    test_path: Path
    rul_path: Path


@dataclass
class CmapssDataset:
    """A loaded C-MAPSS subset, ready for feature engineering.

    Attributes:
        train: Training trajectories with a derived per-row ``RUL`` column.
        test: Test trajectories with a per-row ``RUL`` column derived from the
            provided ground truth.
    """

    train: pd.DataFrame
    test: pd.DataFrame


def load_config(path: str | Path) -> DataConfig:
    """Read a YAML data config into a :class:`DataConfig`.

    The YAML names a base directory and the three file names for the FD001
    subset. Paths are resolved against the base directory so the config can move
    between a laptop and a bucket mount without edits.

    Args:
        path: Path to the YAML config file.

    Returns:
        The resolved paths for the FD001 subset.

    Raises:
        KeyError: If a required key is missing from the config.
    """
    raw = yaml.safe_load(Path(path).read_text())
    base = Path(raw.get("data_dir", "."))
    fd001 = raw["fd001"]
    return DataConfig(
        train_path=base / fd001["train"],
        test_path=base / fd001["test"],
        rul_path=base / fd001["rul"],
    )


def read_cmapss_frame(path: str | Path) -> pd.DataFrame:
    """Parse a single C-MAPSS trajectory file into a typed dataframe.

    Args:
        path: Path to a ``train_FD00X.txt`` or ``test_FD00X.txt`` file.

    Returns:
        A dataframe with the 26 data-dictionary columns, integer index columns,
        and float sensor and setting columns.

    Raises:
        ValueError: If the file does not have exactly 26 usable columns, or if
            any value is missing (a sign of a malformed or ragged row).
    """
    path = Path(path)
    raw = pd.read_csv(path, sep=r"\s+", header=None)
    # Trailing whitespace in the source files can produce empty trailing columns.
    raw = raw.dropna(axis=1, how="all")
    if raw.shape[1] != EXPECTED_COLUMN_COUNT:
        raise ValueError(f"{path}: expected {EXPECTED_COLUMN_COUNT} columns, got {raw.shape[1]}")
    raw.columns = list(COLUMN_NAMES)
    if raw.isna().to_numpy().any():
        raise ValueError(f"{path}: found missing values, the file has a malformed row")
    return raw.astype({"unit_number": "int64", "time_cycles": "int64"})


def load_rul_targets(path: str | Path) -> pd.Series:
    """Read a ``RUL_FD00X.txt`` file into a series of per-unit RUL values.

    Args:
        path: Path to the ground-truth RUL file. One integer per line, in unit
            order, giving the RUL at each test unit's last recorded cycle.

    Returns:
        A series of integer RUL values, indexed from zero in file order.

    Raises:
        ValueError: If the file is empty or has more than one value per line.
    """
    path = Path(path)
    raw = pd.read_csv(path, sep=r"\s+", header=None).dropna(axis=1, how="all")
    if raw.shape[1] != 1:
        raise ValueError(f"{path}: expected one RUL value per line, got {raw.shape[1]}")
    if raw.empty:
        raise ValueError(f"{path}: no RUL values found")
    return raw.iloc[:, 0].astype("int64").reset_index(drop=True)


def add_training_rul(frame: pd.DataFrame) -> pd.DataFrame:
    """Derive per-row RUL for run-to-failure training trajectories.

    A training trajectory runs until failure, so the last recorded cycle for a
    unit is the failure point and its RUL is zero. Every earlier cycle has a RUL
    equal to the number of cycles left before that failure.

    Args:
        frame: A training dataframe from :func:`read_cmapss_frame`.

    Returns:
        A copy of the frame with an added integer ``RUL`` column.
    """
    last_cycle = frame.groupby("unit_number")["time_cycles"].transform("max")
    out = frame.copy()
    out[RUL_COLUMN] = (last_cycle - out["time_cycles"]).astype("int64")
    return out


def add_test_rul(frame: pd.DataFrame, targets: pd.Series) -> pd.DataFrame:
    """Derive per-row RUL for test trajectories from the provided ground truth.

    Test trajectories stop some cycles before failure. The RUL file gives the RUL
    at each unit's last recorded cycle, so a row at cycle ``t`` has a RUL of that
    provided value plus the number of cycles between ``t`` and the last recorded
    cycle.

    Args:
        frame: A test dataframe from :func:`read_cmapss_frame`.
        targets: Per-unit RUL values in unit order, from :func:`load_rul_targets`.

    Returns:
        A copy of the frame with an added integer ``RUL`` column.

    Raises:
        ValueError: If the number of targets does not match the number of units.
    """
    units = sorted(frame["unit_number"].unique())
    if len(units) != len(targets):
        raise ValueError(
            f"RUL target count ({len(targets)}) does not match unit count ({len(units)})"
        )
    final_rul = dict(zip(units, targets.to_list(), strict=True))
    last_cycle = frame.groupby("unit_number")["time_cycles"].transform("max")
    out = frame.copy()
    out[RUL_COLUMN] = (
        out["unit_number"].map(final_rul) + (last_cycle - out["time_cycles"])
    ).astype("int64")
    return out


def load_fd001(config: DataConfig) -> CmapssDataset:
    """Load the FD001 subset into typed train and test frames with RUL.

    Args:
        config: Resolved paths for the FD001 files.

    Returns:
        The loaded dataset, with a derived ``RUL`` column on both frames.
    """
    train = add_training_rul(read_cmapss_frame(config.train_path))
    test = add_test_rul(read_cmapss_frame(config.test_path), load_rul_targets(config.rul_path))
    return CmapssDataset(train=train, test=test)
