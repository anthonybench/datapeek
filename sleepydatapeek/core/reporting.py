"""Markdown report generation for sleepydatapeek."""

from __future__ import annotations

from pathlib import Path

import markdown
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from weasyprint import HTML

from sleepydatapeek.core.config import getConfig
from sleepydatapeek.core.inspectors import DataFileSummary
from sleepydatapeek.utils.formatting import formatBytes, renderKeyValueTable, renderTable

PDF_STYLESHEET = """
@page { size: A4; margin: 2cm; }
body { font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; font-size: 11pt; color: #1a1a1a; }
h1 { font-size: 22pt; }
h2 { font-size: 15pt; margin-top: 1.4em; border-bottom: 1px solid #ddd; padding-bottom: 0.2em; }
table { border-collapse: collapse; width: 100%; margin: 0.6em 0; }
th, td { border: 1px solid #ccc; padding: 4px 8px; text-align: left; }
th { background: #f2f2f2; }
img { max-width: 100%; }
"""


def writeReport(
    file_summary: DataFileSummary,
    output_dir: Path,
    groupby: str | None = None,
) -> tuple[Path, Path]:
    """Write the markdown report, chart images, and a rendered PDF into a folder.

    Args:
        file_summary: Data summary used to build the report.
        output_dir: Destination folder for all report artifacts.
        groupby: Optional column name used for grouped counts.

    Returns:
        A tuple of the markdown path and the PDF path.

    Raises:
        ValueError: If the groupby column is missing.
    """

    output_dir.mkdir(parents=True, exist_ok=True)
    stem = file_summary.file_path.stem
    markdown_path = output_dir / f"{stem}.md"
    pdf_path = output_dir / f"{stem}.pdf"

    writeMarkdownReport(file_summary, markdown_path, groupby)
    convertMarkdownToPdf(markdown_path, pdf_path)
    return markdown_path, pdf_path


def convertMarkdownToPdf(markdown_path: Path, pdf_path: Path) -> None:
    """Render a markdown report to PDF, resolving relative image links.

    Args:
        markdown_path: Path to the source markdown report.
        pdf_path: Destination path for the rendered PDF.

    Returns:
        None.
    """

    markdown_text = markdown_path.read_text(encoding="utf-8")
    html_body = markdown.markdown(markdown_text, extensions=["tables", "fenced_code"])
    html_document = (
        "<html><head><meta charset='utf-8'>"
        f"<style>{PDF_STYLESHEET}</style></head><body>{html_body}</body></html>"
    )
    HTML(string=html_document, base_url=str(markdown_path.parent)).write_pdf(pdf_path)


def writeMarkdownReport(
    file_summary: DataFileSummary,
    output_path: Path,
    groupby: str | None = None,
) -> None:
    """Write a markdown report and chart images for a data file.

    Args:
        file_summary: Data summary used to build the report.
        output_path: Destination markdown file path.
        groupby: Optional column name used for grouped counts.

    Returns:
        None.

    Raises:
        ValueError: If the groupby column is missing.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)
    assets_dir = output_path.parent / f"{output_path.stem}_assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    if groupby is not None and groupby not in file_summary.dataframe.columns:
        raise ValueError(f"Groupby column '{groupby}' was not found in the input data.")

    null_chart_path = assets_dir / "null_counts.png"
    distinct_chart_path = assets_dir / "distinct_counts.png"

    createComparisonChart(
        values=file_summary.dataframe.isna().sum().sort_values(ascending=False),
        title="Null Count by Column",
        x_label="Null rows",
        output_path=null_chart_path,
    )
    createComparisonChart(
        values=file_summary.dataframe.nunique(dropna=True).sort_values(ascending=False),
        title="Distinct Value Count by Column",
        x_label="Distinct values",
        output_path=distinct_chart_path,
    )

    markdown_content = buildMarkdownReport(
        file_summary, output_path, null_chart_path, distinct_chart_path, groupby
    )
    output_path.write_text(markdown_content, encoding="utf-8")


def buildMarkdownReport(
    file_summary: DataFileSummary,
    output_path: Path,
    null_chart_path: Path,
    distinct_chart_path: Path,
    groupby: str | None = None,
) -> str:
    """Build markdown report content.

    Args:
        file_summary: Data summary used to build the report.
        output_path: Destination markdown file path.
        null_chart_path: Saved chart path for null counts.
        distinct_chart_path: Saved chart path for distinct counts.
        groupby: Optional column name used for grouped counts.

    Returns:
        Markdown report text.
    """

    config = getConfig()
    overview_rows = [
        ("File", str(file_summary.file_path)),
        ("File size", formatBytes(file_summary.file_size_bytes)),
        ("Rows", str(file_summary.row_count)),
        ("Columns", str(file_summary.column_count)),
        ("Index", file_summary.index_details.name),
        ("Index dtype", file_summary.index_details.dtype),
    ]
    schema_rows = [(field.name, field.dtype) for field in file_summary.schema]

    sections = [
        "# Sleepysleepydatapeek Report",
        "",
        "## Overview",
        "",
        renderKeyValueTable(overview_rows, config.report_table_format),
        "",
        "## Sample",
        "",
        renderTable(
            headers="keys",
            rows=file_summary.sample_rows,
            table_format=config.report_table_format,
            show_index=True,
        ),
        "",
        "## Schema",
        "",
        renderTable(
            headers=["Column", "Pandas dtype"],
            rows=schema_rows,
            table_format=config.report_table_format,
        ),
        "",
        "## Charts",
        "",
        f"![Null count comparison]({null_chart_path.relative_to(output_path.parent)})",
        "",
        f"![Distinct count comparison]({distinct_chart_path.relative_to(output_path.parent)})",
    ]

    if groupby is not None:
        group_rows = (
            file_summary.dataframe.groupby(groupby, dropna=False)
            .size()
            .reset_index(name="row_count")
            .sort_values("row_count", ascending=False)
        )
        sections.extend(
            [
                "",
                f"## Group Counts: {groupby}",
                "",
                renderTable(
                    headers="keys",
                    rows=group_rows,
                    table_format=config.report_table_format,
                    show_index=False,
                ),
            ]
        )

    return "\n".join(sections) + "\n"


def createComparisonChart(
    values: pd.Series,
    title: str,
    x_label: str,
    output_path: Path,
) -> None:
    """Create a seaborn horizontal bar chart for the provided values.

    Args:
        values: Series of values indexed by column name.
        title: Chart title.
        x_label: X-axis label.
        output_path: Destination path for the chart image.

    Returns:
        None.
    """

    plot_frame = values.reset_index()
    plot_frame.columns = ["column_name", "value"]

    plt.figure(figsize=(10, max(4, len(plot_frame) * 0.45)))
    sns.set_theme(style="whitegrid")
    chart = sns.barplot(
        data=plot_frame,
        x="value",
        y="column_name",
        hue="column_name",
        palette="crest",
        legend=False,
    )
    chart.set_title(title)
    chart.set_xlabel(x_label)
    chart.set_ylabel("Column")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
