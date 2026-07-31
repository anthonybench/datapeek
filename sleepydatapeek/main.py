"""CLI entrypoint for the sleepydatapeek application."""

import sys

import typer

from sleepydatapeek.cli.commands import registerCommands
from sleepydatapeek.core.logging import configureLogging
from sleepydatapeek.core.version import printVersion, wantsVersion

app = typer.Typer(
    add_completion=False,
    help=(
        "Inspect tabular data files and generate concise markdown reports. "
        "Pass -v/--version anywhere to print the version."
    ),
)

configureLogging()
registerCommands(app)


def main() -> None:
    """Run the sleepydatapeek CLI application.

    ``-v``/``--version`` is honored before Typer parses, so it works even when it
    appears among a subcommand's arguments; the rest of the command is ignored.
    """

    if wantsVersion(sys.argv[1:]):
        printVersion()
        return
    app()


if __name__ == "__main__":
    main()
