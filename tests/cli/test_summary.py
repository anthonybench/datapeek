"""CLI tests for the summary command."""

from pathlib import Path

import pandas as pd
from PIL import Image
from typer.testing import CliRunner

from sleepydatapeek.main import app


def testSummaryCommandForCsv(tmp_path: Path) -> None:
    """Ensure the summary command renders expected details for CSV files.

    Args:
        tmp_path: Pytest temporary directory fixture.

    Returns:
        None.
    """

    dataframe = pd.DataFrame(
        {
            "name": ["Ada", "Grace", "Katherine"],
            "score": [99, 98, 100],
        }
    )
    input_path = tmp_path / "scores.csv"
    dataframe.to_csv(input_path, index=False)

    runner = CliRunner()
    result = runner.invoke(app, ["summary", str(input_path)])

    assert result.exit_code == 0
    assert "Schema" in result.stdout
    assert "score" in result.stdout
    assert "Rows" in result.stdout


def testSummaryCommandForImage(tmp_path: Path) -> None:
    """Ensure the summary command renders metadata for image files.

    Args:
        tmp_path: Pytest temporary directory fixture.

    Returns:
        None.
    """

    input_path = tmp_path / "sample.png"
    image = Image.new("RGB", (16, 8), color="red")
    image.save(input_path)

    runner = CliRunner()
    result = runner.invoke(app, ["summary", str(input_path)])

    assert result.exit_code == 0
    assert "Metadata" in result.stdout
    assert "Dimensions" in result.stdout
    assert "16 x 8" in result.stdout
