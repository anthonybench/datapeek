# sleepydatapeek

`sleepydatapeek` is a small Typer-based CLI for quickly inspecting tabular data files and generating markdown + PDF reports with summary charts.

## Supported files

- Data files: `csv`, `parquet`, `json`, `pkl`, `xlsx`
- Metadata files: `pdf`, `png`, `jpg`, `jpeg`

## Deploy

PDF report generation uses [WeasyPrint](https://weasyprint.org/), which depends on
native libraries (pango, cairo, gdk-pixbuf). On macOS install them with Homebrew first:

```sh
brew install pango
```

On Debian/Ubuntu the equivalent is `apt install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0`.
See the [WeasyPrint install docs](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html) for other platforms.

Then set up the project:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

```sh
sleepydatapeek summary path/to/data.csv
sleepydatapeek summary path/to/resume.pdf
sleepydatapeek report path/to/data.csv path/to/output_dir --groupby ProductName
sleepydatapeek report path/to/data.csv  # output folder defaults to ./<file>_report
```

The `report` command writes the markdown, rendered PDF, and chart images into the
output folder, and copies the generated PDF onto the clipboard (macOS) so it is
ready to paste. The output folder is optional; when omitted it defaults to
`<file>_report` in the current working directory.

## Teardown

```sh
deactivate
rm -rf .venv
```

## Configuration

`sleepydatapeek` is a *sleepy util* and reads shared settings from
`~/sleepyconfig/params.yml`. On first run the file is created with defaults and
a note is printed to the console. Relevant keys:

- `datapeek_sample_size` — number of rows shown in the sample table.
- `datapeek_table_style` — [tabulate](https://pypi.org/project/tabulate/) table
  style used for the sample/detail tables (e.g. `rounded_grid`, `github`).

## Documentation

- [Specification](docs/SPEC.md) — what the tool does
- [Project outline](docs/OUTLINE.md) — repository layout
- [Test drive](docs/test_drive.md) — setup, testing, and CLI usage
- [Publishing](docs/publish.md) — release to PyPI with Poetry
