"""Report command for sleepydatapeek."""

from pathlib import Path

import typer

from sleepydatapeek.core.inspectors import (
    DataFileSummary,
    buildFileSummary,
    renderReportCreatedMessage,
)
from sleepydatapeek.core.reporting import writeReport
from sleepydatapeek.utils.clipboard import copyFileToClipboard


def register(app: typer.Typer) -> None:
    """Register the report command.

    Args:
        app: Root Typer application instance.

    Returns:
        None.
    """

    @app.command("report")
    def reportCommand(
        input_path: Path = typer.Argument(..., exists=True, readable=True, resolve_path=True),
        output_dir: Path | None = typer.Argument(
            None,
            resolve_path=True,
            help="Folder for the report artifacts. Defaults to '<file>_report' in the working directory.",
        ),
        groupby: str | None = typer.Option(
            None,
            "--groupby",
            help="Optional column used to include a grouped row-count table.",
        ),
    ) -> None:
        """Generate a markdown + PDF report for a supported data file.

        Args:
            input_path: Path to the input data file.
            output_dir: Folder to write the markdown, PDF, and chart images into.
                Defaults to ``<file>_report`` in the current working directory.
            groupby: Optional column name used for grouped counts.

        Returns:
            None.
        """

        file_summary = buildFileSummary(input_path)
        if not isinstance(file_summary, DataFileSummary):
            typer.echo(
                "The report command only supports data files: csv, parquet, json, pkl, and xlsx."
            )
            raise typer.Exit(code=1)

        if output_dir is None:
            output_dir = Path.cwd() / f"{input_path.stem}_report"

        try:
            markdown_path, pdf_path = writeReport(file_summary, output_dir, groupby)
        except ValueError as error:
            raise typer.BadParameter(str(error)) from error

        clipboard_copied = copyFileToClipboard(pdf_path)
        typer.echo(
            renderReportCreatedMessage(output_dir, markdown_path, pdf_path, clipboard_copied)
        )
