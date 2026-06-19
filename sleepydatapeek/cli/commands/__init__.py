"""Command registration helpers for sleepydatapeek."""

from importlib import import_module
from pathlib import Path
from typing import Protocol, cast

import typer


class CommandModule(Protocol):
    """Protocol describing a CLI command module."""

    def register(self, app: typer.Typer) -> None:
        """Register the module's command(s) with the root app."""


def discoverCommandModules() -> list[CommandModule]:
    """Import command modules in this package and return registrable ones.

    Returns:
        A list of imported command modules that expose a ``register`` function.
    """

    command_modules: list[CommandModule] = []
    commands_dir = Path(__file__).resolve().parent

    for module_path in sorted(commands_dir.glob("*.py")):
        if module_path.stem == "__init__":
            continue

        module = import_module(f"{__name__}.{module_path.stem}")
        if hasattr(module, "register"):
            command_modules.append(cast(CommandModule, module))

    return command_modules


def registerCommands(app: typer.Typer) -> None:
    """Register all command modules with the provided Typer app.

    Args:
        app: Root Typer application instance.

    Returns:
        None.
    """

    for command_module in discoverCommandModules():
        command_module.register(app)
