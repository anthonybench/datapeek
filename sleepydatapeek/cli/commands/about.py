"""``about`` command: print the project's public links."""

from __future__ import annotations

import typer

from sleepydatapeek.core.about import printAbout


def register(app: typer.Typer) -> None:
    """Register the ``about`` command.

    Args:
        app: Root Typer application instance.

    Returns:
        None.
    """

    @app.command("about")
    def about() -> None:
        """Print the project's public PyPI and GitHub links."""

        printAbout()
