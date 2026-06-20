"""Tests for the C-MAPSS FD001 loader.

The fixtures are tiny synthetic files written to a temp directory, not the real
dataset, so these run anywhere without DVC or a download.
"""

from pathlib import Path

import pytest

from features.loader import (
    COLUMN_NAMES,
    add_test_rul,
    add_training_rul,
    load_config,
    load_fd001,
    load_rul_targets,
    read_cmapss_frame,
)


def _row(unit: int, cycle: int) -> str:
    """Build one well-formed 26-field C-MAPSS row."""
    settings = [0.0, 0.0, 0.0]
    sensors = [float(i) for i in range(21)]
    return " ".join(str(v) for v in [unit, cycle, *settings, *sensors])


def _write(path: Path, lines: list[str]) -> Path:
    path.write_text("\n".join(lines) + "\n")
    return path


def _train_file(path: Path) -> Path:
    # Unit 1 fails at cycle 3, unit 2 fails at cycle 2.
    return _write(path, [_row(1, 1), _row(1, 2), _row(1, 3), _row(2, 1), _row(2, 2)])


def test_read_parses_columns_and_types(tmp_path):
    frame = read_cmapss_frame(_train_file(tmp_path / "train.txt"))
    assert list(frame.columns) == list(COLUMN_NAMES)
    assert frame.shape == (5, 26)
    assert frame["unit_number"].dtype == "int64"
    assert frame["time_cycles"].dtype == "int64"
    assert frame["sensor_1"].dtype == "float64"


def test_training_rul_counts_down_to_zero(tmp_path):
    frame = add_training_rul(read_cmapss_frame(_train_file(tmp_path / "train.txt")))
    unit1 = frame[frame["unit_number"] == 1].sort_values("time_cycles")
    assert unit1["RUL"].tolist() == [2, 1, 0]
    unit2 = frame[frame["unit_number"] == 2].sort_values("time_cycles")
    assert unit2["RUL"].tolist() == [1, 0]


def test_load_rul_targets(tmp_path):
    targets = load_rul_targets(_write(tmp_path / "rul.txt", ["10", "5"]))
    assert targets.tolist() == [10, 5]
    assert targets.dtype == "int64"


def test_test_rul_adds_offset_to_ground_truth(tmp_path):
    test_path = _write(
        tmp_path / "test.txt",
        [_row(1, 1), _row(1, 2), _row(2, 1), _row(2, 2), _row(2, 3)],
    )
    frame = read_cmapss_frame(test_path)
    targets = load_rul_targets(_write(tmp_path / "rul.txt", ["10", "5"]))
    out = add_test_rul(frame, targets)
    unit1 = out[out["unit_number"] == 1].sort_values("time_cycles")
    assert unit1["RUL"].tolist() == [11, 10]  # last recorded cycle carries the provided 10
    unit2 = out[out["unit_number"] == 2].sort_values("time_cycles")
    assert unit2["RUL"].tolist() == [7, 6, 5]  # last recorded cycle carries the provided 5


def test_malformed_row_raises(tmp_path):
    short = " ".join(str(v) for v in [1, 4, 0.0, 0.0, 0.0, *[float(i) for i in range(20)]])
    path = _write(tmp_path / "train.txt", [_row(1, 1), _row(1, 2), _row(1, 3), short])
    with pytest.raises(ValueError, match="malformed"):
        read_cmapss_frame(path)


def test_mismatched_rul_count_raises(tmp_path):
    frame = read_cmapss_frame(_train_file(tmp_path / "test.txt"))
    targets = load_rul_targets(_write(tmp_path / "rul.txt", ["10"]))  # one target, two units
    with pytest.raises(ValueError, match="does not match"):
        add_test_rul(frame, targets)


def test_load_fd001_end_to_end(tmp_path):
    data_dir = tmp_path / "cmapss"
    data_dir.mkdir()
    _train_file(data_dir / "train_FD001.txt")
    _write(
        data_dir / "test_FD001.txt",
        [_row(1, 1), _row(1, 2), _row(2, 1), _row(2, 2), _row(2, 3)],
    )
    _write(data_dir / "RUL_FD001.txt", ["10", "5"])
    config_path = _write(
        tmp_path / "data.yaml",
        [
            f"data_dir: {data_dir}",
            "fd001:",
            "  train: train_FD001.txt",
            "  test: test_FD001.txt",
            "  rul: RUL_FD001.txt",
        ],
    )
    dataset = load_fd001(load_config(config_path))
    assert "RUL" in dataset.train.columns
    assert "RUL" in dataset.test.columns
    assert dataset.train.shape == (5, 27)
    assert dataset.test.shape == (5, 27)
    unit2_last = dataset.test[
        (dataset.test["unit_number"] == 2) & (dataset.test["time_cycles"] == 3)
    ]
    assert unit2_last["RUL"].item() == 5
