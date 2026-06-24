"""Tests for the shared sleepy params loading and datapeek config wiring."""

from __future__ import annotations

from pathlib import Path

import pytest

from sleepydatapeek.core.config import getConfig
from sleepydatapeek.core.sleepy_params import (
    PARAMS_PATH_ENV_VAR,
    loadSleepyParams,
)


def testLoadSleepyParamsWritesDefaultsWhenMissing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Ensure a missing params file is created with defaults and announced.

    Args:
        tmp_path: Pytest temporary directory fixture.
        monkeypatch: Pytest monkeypatch fixture.

    Returns:
        None.
    """

    params_path = tmp_path / "fresh" / "params.yml"
    monkeypatch.setenv(PARAMS_PATH_ENV_VAR, str(params_path))

    messages: list[str] = []
    params = loadSleepyParams(echo=messages.append)

    assert params_path.exists()
    assert params["datapeek_sample_size"] == 5
    assert params["datapeek_table_style"] == "rounded_grid"
    assert "convert_output_archive_dir" not in params
    assert any("defaults" in message for message in messages)


def testGetConfigReflectsCustomParams(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure getConfig applies user-provided sample size and table style.

    Args:
        tmp_path: Pytest temporary directory fixture.
        monkeypatch: Pytest monkeypatch fixture.

    Returns:
        None.
    """

    params_path = tmp_path / "custom" / "params.yml"
    params_path.parent.mkdir(parents=True, exist_ok=True)
    params_path.write_text(
        "datapeek_sample_size: 12\ndatapeek_table_style: github\n",
        encoding="utf-8",
    )
    monkeypatch.setenv(PARAMS_PATH_ENV_VAR, str(params_path))

    config = getConfig()

    assert config.sample_rows == 12
    assert config.summary_table_format == "github"
