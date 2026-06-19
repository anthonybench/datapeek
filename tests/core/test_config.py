"""Tests for application configuration."""

from pathlib import Path

from sleepydatapeek.core.config import getConfig
from sleepydatapeek.core.inspectors import determineFileKind


def testConfigContainsExpectedSuffixes() -> None:
    """Ensure the app config exposes the supported file suffixes.

    Returns:
        None.
    """

    config = getConfig()

    assert ".csv" in config.data_suffixes
    assert ".pdf" in config.metadata_suffixes
    assert config.sample_rows == 5
    assert config.sample_columns == 7


def testDetermineFileKindReturnsExpectedKinds() -> None:
    """Ensure supported suffixes map to their intended summary kinds.

    Returns:
        None.
    """

    config = getConfig()

    assert determineFileKind(Path("sample.csv"), config) == "data"
    assert determineFileKind(Path("sample.png"), config) == "metadata"
