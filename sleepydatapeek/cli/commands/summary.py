"""Summary command for sleepydatapeek."""

from pathlib import Path

import typer

from sleepydatapeek.core.inspectors import buildFileSummary, renderFileSummary


def register(app: typer.Typer) -> None:
    """Register the summary command.

    Args:
        app: Root Typer application instance.

    Returns:
        None.
    """

    @app.command("summary")
    def summaryCommand(
        input_path: Path = typer.Argument(..., exists=True, readable=True, resolve_path=True),
    ) -> None:
        """Print a concise summary of a supported file.

        Args:
            input_path: Path to the file to inspect.

        Returns:
            None.
        """

        file_summary = buildFileSummary(input_path)
        typer.echo(renderFileSummary(file_summary))
