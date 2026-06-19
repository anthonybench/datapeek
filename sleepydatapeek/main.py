"""CLI entrypoint for the sleepydatapeek application."""

import typer

from sleepydatapeek.cli.commands import registerCommands
from sleepydatapeek.core.logging import configureLogging

app = typer.Typer(
    add_completion=False,
    help="Inspect tabular data files and generate concise markdown reports.",
)

configureLogging()
registerCommands(app)


def main() -> None:
    """Run the sleepydatapeek CLI application."""

    app()


if __name__ == "__main__":
    main()
