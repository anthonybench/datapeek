"""sleepydatapeek's slice of the shared "sleepy utils" configuration.

All sleepy utilities read their parameters from a single shared file at
``~/sleepyconfig/params.yml``, but each tool owns only its own
``<tool_shorthand>_<name>`` keys and never references another tool's keys. For
sleepydatapeek the shorthand is ``datapeek``.

Behavior:
- When the file does not exist, this tool writes ONLY its own section (and says
  so on the console).
- When the file exists but a value this tool needs is absent, the tool prints
  its config snippet and asks the user to verify their sleepyconfig.
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

# Human-facing tool name used in console messages.
TOOL_NAME = "sleepydatapeek"

# In-memory defaults for this tool's own parameters.
DEFAULT_PARAMS: dict[str, Any] = {
    "datapeek_sample_size": 5,
    "datapeek_table_style": "rounded_grid",
}

# This tool's own section of ``~/sleepyconfig/params.yml``. Written verbatim when
# the file is absent, and printed when a required value is missing.
DEFAULT_PARAMS_SNIPPET = """# sleepydatapeek
datapeek_sample_size: 5
datapeek_table_style: rounded_grid
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
    """Load parameters from the shared sleepy config.

    Writes only this tool's own section when the file is absent.

    Args:
        echo: Callable used to report that defaults were written. Defaults to
            ``typer.echo``.

    Returns:
        The parameters present in the file (or this tool's defaults when the
        file was just created). Values are not merged with defaults; missing
        keys are surfaced lazily by :func:`requireParam`.
    """

    params_path = getParamsPath()

    if not params_path.exists():
        params_path.parent.mkdir(parents=True, exist_ok=True)
        params_path.write_text(DEFAULT_PARAMS_SNIPPET, encoding="utf-8")
        echo(f"No sleepy config found; wrote {TOOL_NAME} defaults to {params_path}")
        return dict(DEFAULT_PARAMS)

    loaded = yaml.safe_load(params_path.read_text(encoding="utf-8")) or {}
    return loaded if isinstance(loaded, dict) else {}


def requireParam(params: dict[str, Any], key: str, echo: Callable[..., None] = typer.echo) -> Any:
    """Return a required parameter, or guide the user to fix their config.

    When the key is absent, prints this tool's config snippet and exits so the
    user can verify their sleepyconfig.

    Args:
        params: The loaded parameters.
        key: The required parameter key.
        echo: Callable used to print the guidance. Defaults to ``typer.echo``.

    Returns:
        The parameter value.

    Raises:
        typer.Exit: With code 1 when the key is missing.
    """

    if key not in params:
        echo(
            f"Missing '{key}' in {getParamsPath()}.\n"
            f"Please verify your sleepyconfig is correct — the {TOOL_NAME} section "
            f"should look like:\n\n{DEFAULT_PARAMS_SNIPPET}",
            err=True,
        )
        raise typer.Exit(1)
    return params[key]
