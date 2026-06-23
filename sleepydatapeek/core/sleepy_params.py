"""Shared "sleepy utils" global configuration.

All sleepy utilities (sleepydatapeek, sleepyconvert, sleepybricks, and future
tools) read their user-tunable parameters from a single shared file at
``~/sleepyconfig/params.yml``. When the file is missing it is created with the
default template below and a message is printed to the console.

The schema in this module is intentionally duplicated across each sleepy
utility package: the tools ship as independent distributions and cannot share
an importable library, so each carries an identical copy of the shared
contract. Keep the template and defaults here in sync with the other tools.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable

import typer
import yaml

# Environment override for the params file location. Primarily used by tests to
# avoid touching the real home directory.
PARAMS_PATH_ENV_VAR = "SLEEPYCONFIG_PARAMS_PATH"

# In-memory fallbacks for every known sleepy-utils parameter.
DEFAULT_PARAMS: dict[str, Any] = {
    # sleepydatapeek
    "datapeek_sample_size": 5,
    "datapeek_table_style": "rounded_grid",
    # sleepyconvert
    "convert_output_archive_dir": None,
    # sleepybricks
    "bricks_table_style": "simple",
    "serverless_warehouse_name": "<env>_serverless_warehouse",
    "env_emojis": {"dev": "👩‍💻", "stg": "🔧", "us": "🇺🇸"},
    "display_names": {"dev": "Development", "stg": "Staging", "us": "United States"},
}

# Verbatim contents written when the params file does not yet exist. This is
# written by whichever sleepy utility runs first, seeding keys for all tools.
DEFAULT_PARAMS_TEMPLATE = """# sleepydatapeek
datapeek_sample_size: 5
datapeek_table_style: rounded_grid

# sleepyconvert
convert_output_archive_dir: null

# sleepybricks
bricks_table_style: simple
serverless_warehouse_name: <env>_serverless_warehouse
env_emojis:
  dev: "👩‍💻"
  stg: "🔧"
  us: "🇺🇸"
display_names:
  dev: "Development"
  stg: "Staging"
  us: "United States"
"""


def getParamsPath() -> Path:
    """Return the resolved path to the shared sleepy params file.

    Returns:
        The params file path, honoring the ``SLEEPYCONFIG_PARAMS_PATH``
        environment override when set.
    """

    override = os.getenv(PARAMS_PATH_ENV_VAR)
    if override:
        return Path(override).expanduser()
    return Path.home() / "sleepyconfig" / "params.yml"


def loadSleepyParams(echo: Callable[[str], None] = typer.echo) -> dict[str, Any]:
    """Load shared sleepy parameters, creating the file with defaults if absent.

    Args:
        echo: Callable used to report that defaults were written. Defaults to
            ``typer.echo``.

    Returns:
        A mapping of parameter names to values, with defaults filled in for any
        keys missing from the file.
    """

    params_path = getParamsPath()

    if not params_path.exists():
        params_path.parent.mkdir(parents=True, exist_ok=True)
        params_path.write_text(DEFAULT_PARAMS_TEMPLATE, encoding="utf-8")
        echo(f"No sleepy config found; wrote defaults to {params_path}")
        return dict(DEFAULT_PARAMS)

    loaded = yaml.safe_load(params_path.read_text(encoding="utf-8")) or {}
    merged = dict(DEFAULT_PARAMS)
    if isinstance(loaded, dict):
        merged.update(loaded)
    return merged
