"""Application configuration for sleepydatapeek."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Application configuration values.

    Attributes:
        sample_rows: Number of sample rows shown in summaries.
        sample_columns: Maximum number of columns shown in sample tables.
        summary_table_format: Default tabulate format for detail tables.
        report_table_format: Default tabulate format for markdown reports.
        data_suffixes: Supported suffixes for tabular data files.
        metadata_suffixes: Supported suffixes for metadata-only files.
    """

    sample_rows: int = 5
    sample_columns: int = 7
    summary_table_format: str = "rounded_outline"
    report_table_format: str = "github"
    data_suffixes: tuple[str, ...] = (".csv", ".parquet", ".json", ".pkl", ".xlsx")
    metadata_suffixes: tuple[str, ...] = (".pdf", ".png", ".jpg", ".jpeg")


def getConfig() -> AppConfig:
    """Return application configuration.

    Returns:
        The immutable application configuration instance.
    """

    return AppConfig()
