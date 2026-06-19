"""Clipboard helpers for sleepydatapeek."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def copyFileToClipboard(file_path: Path) -> bool:
    """Copy a file itself onto the system clipboard.

    Places the file on the clipboard the same way a Finder copy does, so it can
    be pasted as a file into other applications. Only supported on macOS.

    Args:
        file_path: Path to the file to copy.

    Returns:
        ``True`` if the file was copied, ``False`` if unsupported or it failed.
    """

    if sys.platform != "darwin":
        return False

    script = f"set the clipboard to (POSIX file {_quoteAppleScript(str(file_path))})"
    try:
        subprocess.run(["osascript", "-e", script], check=True, capture_output=True)
    except (OSError, subprocess.CalledProcessError):
        return False
    return True


def _quoteAppleScript(value: str) -> str:
    """Quote a string as an AppleScript string literal.

    Args:
        value: Raw string value.

    Returns:
        A double-quoted, escaped AppleScript string literal.
    """

    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'
