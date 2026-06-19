"""CLI tests for the report command."""

from pathlib import Path

import pandas as pd
from PIL import Image
from typer.testing import CliRunner

from sleepydatapeek.main import app


def testReportCommandCreatesMarkdownAndCharts(tmp_path: Path) -> None:
    """Ensure the report command writes the markdown report and chart assets.

    Args:
        tmp_path: Pytest temporary directory fixture.

    Returns:
        None.
    """

    dataframe = pd.DataFrame(
        {
            "ProductName": ["Widget", "Widget", "Gizmo"],
            "Quantity": [2, 5, 7],
            "Region": ["West", "East", "West"],
        }
    )
    input_path = tmp_path / "sales.csv"
    output_dir = tmp_path / "report_out"
    dataframe.to_csv(input_path, index=False)

    runner = CliRunner()
    result = runner.invoke(
        app,
        ["report", str(input_path), str(output_dir), "--groupby", "ProductName"],
    )

    assert result.exit_code == 0
    markdown_path = output_dir / "sales.md"
    pdf_path = output_dir / "sales.pdf"
    assert markdown_path.exists()
    assert pdf_path.exists()
    assert "Report folder:" in result.stdout
    assert "Relative path:" in result.stdout

    report_text = markdown_path.read_text(encoding="utf-8")
    assert "## Group Counts: ProductName" in report_text
    assert "null_counts.png" in report_text
    assert "distinct_counts.png" in report_text


def testReportCommandDefaultsOutputDirToWorkingDirectory(tmp_path: Path, monkeypatch) -> None:
    """Ensure the report command defaults the output folder to the working directory.

    Args:
        tmp_path: Pytest temporary directory fixture.
        monkeypatch: Pytest monkeypatch fixture used to set the working directory.

    Returns:
        None.
    """

    dataframe = pd.DataFrame({"Quantity": [1, 2, 3]})
    input_path = tmp_path / "sales.csv"
    dataframe.to_csv(input_path, index=False)
    monkeypatch.chdir(tmp_path)

    runner = CliRunner()
    result = runner.invoke(app, ["report", str(input_path)])

    assert result.exit_code == 0
    default_dir = tmp_path / "sales_report"
    assert (default_dir / "sales.md").exists()
    assert (default_dir / "sales.pdf").exists()


def testReportCommandRejectsMetadataFiles(tmp_path: Path) -> None:
    """Ensure the report command rejects metadata-only input files.

    Args:
        tmp_path: Pytest temporary directory fixture.

    Returns:
        None.
    """

    input_path = tmp_path / "photo.jpg"
    output_dir = tmp_path / "report_out"
    image = Image.new("RGB", (10, 10), color="blue")
    image.save(input_path)

    runner = CliRunner()
    result = runner.invoke(app, ["report", str(input_path), str(output_dir)])

    assert result.exit_code != 0
    assert "only supports data files" in result.stdout
