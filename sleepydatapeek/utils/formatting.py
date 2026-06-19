"""Shared output formatting helpers for sleepydatapeek."""

from __future__ import annotations

from typing import Literal, Sequence

import pandas as pd
from tabulate import tabulate

HeadersType = Literal["keys"] | Sequence[str]


def formatBytes(size_bytes: int) -> str:
    """Format a file size in bytes into a short human-readable string.

    Args:
        size_bytes: File size in bytes.

    Returns:
        Human-readable file size text.
    """

    units = ["B", "KB", "MB", "GB", "TB"]
    size_value = float(size_bytes)

    for unit in units:
        if size_value < 1024.0 or unit == units[-1]:
            return f"{size_value:.2f} {unit}"
        size_value /= 1024.0

    return f"{size_value:.2f} TB"


def renderTable(
    headers: HeadersType,
    rows: pd.DataFrame | Sequence[Sequence[object]],
    table_format: str,
    show_index: bool = False,
) -> str:
    """Render rows as a tabulate table.

    Args:
        headers: Tabulate headers configuration.
        rows: Dataframe or row sequence to render.
        table_format: Tabulate table format name.
        show_index: Whether to include dataframe indexes.

    Returns:
        Rendered table string.
    """

    if isinstance(rows, pd.DataFrame):
        return tabulate(rows, headers=headers, tablefmt=table_format, showindex=show_index)

    return tabulate(rows, headers=headers, tablefmt=table_format)


def renderKeyValueTable(
    rows: Sequence[tuple[str, str]], table_format: str, show_headers: bool = True
) -> str:
    """Render key-value rows using tabulate.

    Args:
        rows: Sequence of label-value pairs.
        table_format: Tabulate table format name.
        show_headers: Whether to include the ``Field``/``Value`` header row.

    Returns:
        Rendered key-value table string.
    """

    headers: HeadersType = ["Field", "Value"] if show_headers else ()
    return renderTable(headers=headers, rows=rows, table_format=table_format)


def renderSection(title: str, content: str, subtitle: str | None = None) -> str:
    """Render a CLI section with an optional subtitle.

    Args:
        title: Section title.
        content: Section body text.
        subtitle: Optional subtitle line.

    Returns:
        Formatted section text.
    """

    lines = [title]
    if subtitle is not None:
        lines.append(subtitle)
    lines.append(content)
    return "\n".join(lines)
