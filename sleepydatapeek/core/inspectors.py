"""File inspection helpers for sleepydatapeek."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Mapping

import pandas as pd
from PIL import Image
from pypdf import PdfReader

from sleepydatapeek.core.config import AppConfig, getConfig
from sleepydatapeek.utils.formatting import (
    formatBytes,
    renderKeyValueTable,
    renderSection,
    renderTable,
)


@dataclass(frozen=True)
class SchemaField:
    """Representation of a dataframe column in the schema output.

    Attributes:
        name: Column name.
        dtype: Pandas dtype string.
    """

    name: str
    dtype: str


@dataclass(frozen=True)
class IndexDetails:
    """Representation of dataframe index information.

    Attributes:
        name: Index display name.
        dtype: Pandas dtype string for the index.
    """

    name: str
    dtype: str


@dataclass(frozen=True)
class MetadataEntry:
    """A single metadata value to display.

    Attributes:
        label: Human-readable metadata label.
        value: Metadata value as concise text.
    """

    label: str
    value: str


@dataclass(frozen=True)
class FileSummary:
    """Base description of an inspected file.

    Attributes:
        file_path: Absolute path to the inspected file.
        file_size_bytes: File size in bytes.
        kind: Summary kind, such as ``data`` or ``metadata``.
    """

    file_path: Path
    file_size_bytes: int
    kind: str


@dataclass(frozen=True)
class DataFileSummary(FileSummary):
    """Summary details for a tabular data file.

    Attributes:
        dataframe: Loaded pandas dataframe.
        sample_rows: Sample rows for display.
        hidden_column_count: Number of columns omitted from the sample.
        schema: Schema rows for the dataframe.
        index_details: Index description for the dataframe.
        row_count: Number of rows.
        column_count: Number of columns.
    """

    dataframe: pd.DataFrame
    sample_rows: pd.DataFrame
    hidden_column_count: int
    schema: list[SchemaField]
    index_details: IndexDetails
    row_count: int
    column_count: int


@dataclass(frozen=True)
class MetadataFileSummary(FileSummary):
    """Summary details for a metadata-only file.

    Attributes:
        metadata_entries: Metadata rows for concise display.
    """

    metadata_entries: list[MetadataEntry]


def determineFileKind(file_path: Path, config: AppConfig | None = None) -> str:
    """Determine whether a file is a data file or metadata file.

    Args:
        file_path: File path to inspect.
        config: Optional application configuration.

    Returns:
        A string describing the file kind.

    Raises:
        ValueError: If the suffix is unsupported.
    """

    resolved_config = config or getConfig()
    suffix = file_path.suffix.lower()

    match suffix in resolved_config.data_suffixes, suffix in resolved_config.metadata_suffixes:
        case True, False:
            return "data"
        case False, True:
            return "metadata"
        case _:
            supported_suffixes = ", ".join(
                [*resolved_config.data_suffixes, *resolved_config.metadata_suffixes]
            )
            raise ValueError(
                f"Unsupported file type '{suffix}'. Supported types: {supported_suffixes}"
            )


def buildFileSummary(file_path: Path, config: AppConfig | None = None) -> FileSummary:
    """Build a file summary for the provided path.

    Args:
        file_path: File path to inspect.
        config: Optional application configuration.

    Returns:
        A typed file summary instance.
    """

    resolved_config = config or getConfig()
    file_kind = determineFileKind(file_path, resolved_config)
    file_size_bytes = file_path.stat().st_size

    match file_kind:
        case "data":
            dataframe = loadDataFrame(file_path)
            sample_rows = dataframe.iloc[
                : resolved_config.sample_rows, : resolved_config.sample_columns
            ]
            hidden_column_count = max(dataframe.shape[1] - resolved_config.sample_columns, 0)
            schema = [
                SchemaField(name=str(column_name), dtype=str(dataframe[column_name].dtype))
                for column_name in dataframe.columns
            ]
            index_details = getIndexDetails(dataframe)
            return DataFileSummary(
                file_path=file_path.resolve(),
                file_size_bytes=file_size_bytes,
                kind=file_kind,
                dataframe=dataframe,
                sample_rows=sample_rows,
                hidden_column_count=hidden_column_count,
                schema=schema,
                index_details=index_details,
                row_count=int(dataframe.shape[0]),
                column_count=int(dataframe.shape[1]),
            )
        case "metadata":
            return MetadataFileSummary(
                file_path=file_path.resolve(),
                file_size_bytes=file_size_bytes,
                kind=file_kind,
                metadata_entries=buildMetadataEntries(file_path),
            )
        case _:
            raise ValueError(f"Unsupported file kind '{file_kind}'.")


def loadDataFrame(file_path: Path) -> pd.DataFrame:
    """Load a supported data file into a dataframe.

    Args:
        file_path: Path to the input file.

    Returns:
        A pandas dataframe.

    Raises:
        ValueError: If the loaded object cannot be normalized to a dataframe.
    """

    suffix = file_path.suffix.lower()

    match suffix:
        case ".csv":
            dataframe = pd.read_csv(file_path)
        case ".parquet":
            dataframe = pd.read_parquet(file_path)
        case ".json":
            dataframe = loadJsonDataFrame(file_path)
        case ".pkl":
            dataframe = normalizePickleObject(pd.read_pickle(file_path))
        case ".xlsx":
            dataframe = pd.read_excel(file_path)
        case _:
            raise ValueError(f"Unsupported data file type '{suffix}'.")

    return dataframe


def loadJsonDataFrame(file_path: Path) -> pd.DataFrame:
    """Load a JSON file into a dataframe.

    Args:
        file_path: Path to the JSON file.

    Returns:
        A pandas dataframe.

    Raises:
        ValueError: If the JSON cannot be normalized to a dataframe.
    """

    with file_path.open("r", encoding="utf-8") as file_handle:
        payload = json.load(file_handle)

    if isinstance(payload, list):
        return pd.json_normalize(payload)
    if isinstance(payload, dict):
        if all(isinstance(value, list) for value in payload.values()):
            return pd.DataFrame(payload)
        return pd.json_normalize(payload)

    raise ValueError("JSON content must be an object or array that can be converted to a table.")


def normalizePickleObject(payload: object) -> pd.DataFrame:
    """Normalize a pickle payload to a dataframe.

    Args:
        payload: Object loaded from a pickle file.

    Returns:
        A pandas dataframe.

    Raises:
        ValueError: If the payload cannot be converted to a dataframe.
    """

    if isinstance(payload, pd.DataFrame):
        return payload
    if isinstance(payload, pd.Series):
        return payload.to_frame()
    if isinstance(payload, list):
        return pd.DataFrame(payload)
    if isinstance(payload, dict):
        return pd.DataFrame(payload)

    raise ValueError("Pickle payload must be a pandas object, list, or dict to build a table.")


def getIndexDetails(dataframe: pd.DataFrame) -> IndexDetails:
    """Return concise index information for a dataframe.

    Args:
        dataframe: Dataframe to inspect.

    Returns:
        Index details for display.
    """

    index_name = dataframe.index.name or "index"
    return IndexDetails(name=str(index_name), dtype=str(dataframe.index.dtype))


def buildMetadataEntries(file_path: Path) -> list[MetadataEntry]:
    """Build succinct metadata entries for a supported metadata file.

    Args:
        file_path: Path to the metadata file.

    Returns:
        A list of metadata entries.
    """

    suffix = file_path.suffix.lower()

    match suffix:
        case ".pdf":
            return buildPdfMetadataEntries(file_path)
        case ".png" | ".jpg" | ".jpeg":
            return buildImageMetadataEntries(file_path)
        case _:
            raise ValueError(f"Unsupported metadata file type '{suffix}'.")


def buildPdfMetadataEntries(file_path: Path) -> list[MetadataEntry]:
    """Extract concise PDF metadata.

    Args:
        file_path: Path to the PDF file.

    Returns:
        A list of metadata entries.
    """

    reader = PdfReader(str(file_path))
    raw_metadata = reader.metadata or {}
    selected_fields: list[tuple[str, str | None]] = [
        ("Title", raw_metadata.get("/Title")),
        ("Author", raw_metadata.get("/Author")),
        ("Creator", raw_metadata.get("/Creator")),
        ("Producer", raw_metadata.get("/Producer")),
        ("Created", normalizePdfDate(raw_metadata.get("/CreationDate"))),
        ("Modified", normalizePdfDate(raw_metadata.get("/ModDate"))),
        ("Pages", str(len(reader.pages))),
    ]

    entries = [
        MetadataEntry(label=label, value=value)
        for label, value in selected_fields
        if value not in (None, "")
    ]
    return entries


def normalizePdfDate(raw_value: str | None) -> str | None:
    """Convert a PDF date string into a friendlier format.

    Args:
        raw_value: Raw PDF date string.

    Returns:
        A normalized ISO-like date string, or ``None`` when unavailable.
    """

    if raw_value is None:
        return None

    normalized_value = raw_value.removeprefix("D:")
    if len(normalized_value) < 14:
        return raw_value

    try:
        parsed_datetime = datetime.strptime(normalized_value[:14], "%Y%m%d%H%M%S")
    except ValueError:
        return raw_value

    return parsed_datetime.isoformat(sep=" ")


def buildImageMetadataEntries(file_path: Path) -> list[MetadataEntry]:
    """Extract concise image metadata.

    Args:
        file_path: Path to the image file.

    Returns:
        A list of metadata entries.
    """

    with Image.open(file_path) as image:
        exif_data = image.getexif()
        dpi_value = image.info.get("dpi")

        entries: list[MetadataEntry] = [
            MetadataEntry(label="Format", value=str(image.format or "unknown")),
            MetadataEntry(label="Dimensions", value=f"{image.width} x {image.height}"),
            MetadataEntry(label="Mode", value=str(image.mode)),
        ]

        if dpi_value is not None:
            entries.append(MetadataEntry(label="DPI", value=str(dpi_value)))
        if exif_data:
            selected_exif = extractInterestingExif(exif_data)
            entries.extend(selected_exif)

        return entries


def extractInterestingExif(exif_data: Mapping[int, object]) -> list[MetadataEntry]:
    """Extract a small subset of interesting EXIF fields.

    Args:
        exif_data: Mapping of EXIF tag ids to values.

    Returns:
        A concise list of metadata entries.
    """

    interesting_tags: dict[int, str] = {
        271: "Make",
        272: "Model",
        306: "Modified",
        36867: "Captured",
    }
    entries: list[MetadataEntry] = []

    for tag_id, label in interesting_tags.items():
        tag_value = exif_data.get(tag_id)
        if tag_value is not None:
            entries.append(MetadataEntry(label=label, value=str(tag_value)))

    return entries


def renderFileSummary(file_summary: FileSummary, config: AppConfig | None = None) -> str:
    """Render a human-readable summary for CLI output.

    Args:
        file_summary: Summary object to render.
        config: Optional application configuration.

    Returns:
        The rendered summary text.
    """

    resolved_config = config or getConfig()

    match file_summary:
        case DataFileSummary():
            return renderDataFileSummary(file_summary, resolved_config)
        case MetadataFileSummary():
            return renderMetadataFileSummary(file_summary, resolved_config)
        case _:
            raise ValueError(f"Unsupported summary type '{type(file_summary).__name__}'.")


def renderDataFileSummary(file_summary: DataFileSummary, config: AppConfig) -> str:
    """Render CLI output for a data file summary.

    Args:
        file_summary: Data summary to render.
        config: Application configuration.

    Returns:
        Formatted CLI text.
    """

    overview_rows = [
        ("File", str(file_summary.file_path)),
        ("File size", formatBytes(file_summary.file_size_bytes)),
        ("Rows", str(file_summary.row_count)),
        ("Columns", str(file_summary.column_count)),
        ("Index", file_summary.index_details.name),
        ("Index dtype", file_summary.index_details.dtype),
    ]
    sample_title = f"Sample ({config.sample_rows} rows)"
    sample_warning = (
        f"⚠️ too wide, {file_summary.hidden_column_count} columns elided"
        if file_summary.hidden_column_count
        else None
    )

    schema_rows = [(field.name, field.dtype) for field in file_summary.schema]
    sample_text = renderTable(
        headers="keys",
        rows=file_summary.sample_rows,
        table_format=config.summary_table_format,
        show_index=True,
    )

    sections = [
        renderKeyValueTable(overview_rows, config.summary_table_format, show_headers=False),
        renderSection(
            "Schema",
            renderTable(
                headers=(),
                rows=schema_rows,
                table_format=config.summary_table_format,
            ),
        ),
        renderSection(sample_title, sample_text, sample_warning),
    ]
    return "\n\n".join(sections)


def renderMetadataFileSummary(file_summary: MetadataFileSummary, config: AppConfig) -> str:
    """Render CLI output for a metadata file summary.

    Args:
        file_summary: Metadata summary to render.
        config: Application configuration.

    Returns:
        Formatted CLI text.
    """

    overview_rows = [
        ("File", str(file_summary.file_path)),
        ("File size", formatBytes(file_summary.file_size_bytes)),
        ("Type", file_summary.file_path.suffix.lower()),
    ]
    metadata_rows = [(entry.label, entry.value) for entry in file_summary.metadata_entries]

    sections = [
        renderKeyValueTable(overview_rows, config.summary_table_format, show_headers=False),
        renderSection(
            "Metadata",
            renderTable(
                headers=["Field", "Value"],
                rows=metadata_rows,
                table_format=config.summary_table_format,
            ),
        ),
    ]
    return "\n\n".join(sections)


def renderReportCreatedMessage(
    output_dir: Path,
    markdown_path: Path,
    pdf_path: Path,
    clipboard_copied: bool,
) -> str:
    """Render the report-created console message.

    Args:
        output_dir: Folder containing the generated report artifacts.
        markdown_path: Path to the generated markdown report.
        pdf_path: Path to the generated PDF report.
        clipboard_copied: Whether the PDF was copied to the clipboard.

    Returns:
        A concise message with useful open commands.
    """

    absolute_dir = output_dir.resolve()
    relative_dir = (
        absolute_dir.relative_to(Path.cwd())
        if absolute_dir.is_relative_to(Path.cwd())
        else absolute_dir
    )
    absolute_pdf = pdf_path.resolve()
    clipboard_line = (
        "PDF copied to clipboard — ready to paste."
        if clipboard_copied
        else "PDF could not be copied to clipboard."
    )
    lines = [
        f"Report folder: {absolute_dir}",
        f"Relative path: {relative_dir}",
        f"  markdown: {markdown_path.name}",
        f"  pdf:      {pdf_path.name}",
        clipboard_line,
        f"Open with Zed: zed {absolute_dir}",
        f"Open with VS Code: code {absolute_dir}",
        f"Open PDF: open {absolute_pdf}",
        f"Reveal in Finder: open -R {absolute_pdf}",
    ]
    return "\n".join(lines)
