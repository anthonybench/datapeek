"""Application configuration for sleepydatapeek."""

from dataclasses import dataclass

from sleepydatapeek.core.sleepy_params import DEFAULT_PARAMS, loadSleepyParams


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
    summary_table_format: str = "rounded_grid"
    report_table_format: str = "github"
    data_suffixes: tuple[str, ...] = (".csv", ".parquet", ".json", ".pkl", ".xlsx")
    metadata_suffixes: tuple[str, ...] = (".pdf", ".png", ".jpg", ".jpeg")


def getConfig() -> AppConfig:
    """Return application configuration sourced from the shared sleepy config.

    Reads ``~/sleepyconfig/params.yml`` (creating it with defaults on first
    run) and applies the sleepydatapeek-owned parameters. The ``sample size``
    drives how many sample rows are shown, and the ``table style`` selects the
    tabulate format used for the sampled detail tables.

    Returns:
        The immutable application configuration instance.
    """

    params = loadSleepyParams()
    sample_size = params.get("datapeek_sample_size", DEFAULT_PARAMS["datapeek_sample_size"])
    table_style = params.get("datapeek_table_style", DEFAULT_PARAMS["datapeek_table_style"])

    return AppConfig(
        sample_rows=int(sample_size),
        summary_table_format=str(table_style),
    )
