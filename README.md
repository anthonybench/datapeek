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

Then set up the project with [uv](https://docs.astral.sh/uv/):

```sh
uv venv
uv pip install -e ".[dev]"
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
rm -rf .venv
```

## Configuration

`sleepydatapeek` is a *sleepy util* and reads its settings from the shared
`~/sleepyconfig/params.yml`. Each sleepy util owns only its own `<tool>_<name>`
keys; sleepydatapeek uses the `datapeek_` prefix. If the file is absent,
sleepydatapeek writes only its own section and prints a note. If a value it
needs is missing, it prints that section and asks you to verify your config.
Keys:

- `datapeek_sample_size` — number of rows shown in the sample table.
- `datapeek_table_style` — [tabulate](https://pypi.org/project/tabulate/) table
  style used for the sample/detail tables (e.g. `rounded_grid`, `github`).

```yaml
# sleepydatapeek
datapeek_sample_size: 5
datapeek_table_style: rounded_grid
```

## Documentation

- [Specification](docs/SPEC.md) — what the tool does
- [Project outline](docs/OUTLINE.md) — repository layout
- [Test drive](docs/test_drive.md) — setup, testing, and CLI usage
- [Adding a command](docs/new_command.md) — how to extend the CLI
- [Publishing](docs/publish.md) — release to PyPI with Poetry
