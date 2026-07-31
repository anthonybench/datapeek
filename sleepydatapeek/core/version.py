"""Version reporting and a best-effort PyPI update check.

The ``-v``/``--version`` flag is handled by a pre-scan of ``sys.argv`` in the CLI
entrypoint (see ``main``), so it works even when buried in a subcommand's args
(e.g. ``sleepydatapeek summary data.csv --version``) — the rest of the command is
ignored. The update check is best-effort and never fails the CLI.
"""

from __future__ import annotations

import json
import urllib.request
from importlib.metadata import PackageNotFoundError, version
from typing import Callable, Optional, Sequence

DIST_NAME = "sleepydatapeek"
_PYPI_JSON_URL = f"https://pypi.org/pypi/{DIST_NAME}/json"
_UPDATE_CHECK_TIMEOUT_SECONDS = 2.0


def getVersion() -> str:
    """Return the installed distribution version, or ``"unknown"`` if unavailable."""

    try:
        return version(DIST_NAME)
    except PackageNotFoundError:
        return "unknown"


def latestVersion() -> Optional[str]:
    """Best-effort fetch of the latest version on PyPI; ``None`` on any failure."""

    try:
        with urllib.request.urlopen(
            _PYPI_JSON_URL, timeout=_UPDATE_CHECK_TIMEOUT_SECONDS
        ) as response:
            payload = json.load(response)
        return str(payload["info"]["version"])
    except Exception:  # noqa: BLE001 - the check is best-effort; never fail the CLI
        return None


def _asTuple(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.split(".") if part.isdigit())


def isNewer(candidate: str, current: str) -> bool:
    """Return whether ``candidate`` is a newer release than ``current``."""

    candidate_parts, current_parts = _asTuple(candidate), _asTuple(current)
    if candidate_parts and current_parts:
        return candidate_parts > current_parts
    return candidate != current  # fall back to inequality if unparseable


def wantsVersion(args: Sequence[str]) -> bool:
    """Return whether ``-v``/``--version`` appears anywhere in the given args."""

    return any(arg in ("-v", "--version") for arg in args)


def printVersion(fetch_latest: Callable[[], Optional[str]] = latestVersion) -> None:
    """Print the current version and, best-effort, whether a newer one exists.

    Args:
        fetch_latest: Callable returning the latest published version (or ``None``
            when it can't be determined). Injectable for tests.

    Returns:
        None.
    """

    current = getVersion()
    print(f"{DIST_NAME} {current}")

    latest = fetch_latest()
    if latest is None:
        return  # offline / lookup failed — stay quiet
    if current == "unknown":
        print(f"latest on PyPI: {latest}")
    elif isNewer(latest, current):
        print(f"⬆️  a newer version is available: {latest}  (upgrade: uv tool upgrade {DIST_NAME})")
    else:
        print("✅ you're on the latest version")
