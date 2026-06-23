"""Shared pytest fixtures for sleepydatapeek tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from sleepydatapeek.core.sleepy_params import (
    DEFAULT_PARAMS_TEMPLATE,
    PARAMS_PATH_ENV_VAR,
)


@pytest.fixture(autouse=True)
def isolatedSleepyConfig(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point the shared sleepy config at a throwaway file for every test.

    Pre-seeding the file keeps tests from writing to the real
    ``~/sleepyconfig`` and avoids the first-run "wrote defaults" message in
    command output.

    Args:
        tmp_path: Pytest temporary directory fixture.
        monkeypatch: Pytest monkeypatch fixture.

    Returns:
        The path to the isolated params file.
    """

    params_path = tmp_path / "sleepyconfig" / "params.yml"
    params_path.parent.mkdir(parents=True, exist_ok=True)
    params_path.write_text(DEFAULT_PARAMS_TEMPLATE, encoding="utf-8")
    monkeypatch.setenv(PARAMS_PATH_ENV_VAR, str(params_path))
    return params_path
