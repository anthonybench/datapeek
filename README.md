<div align="center">

# 🔎 sleepydatapeek

**Peek at local data files fast — instant summaries and pretty markdown/PDF reports.**

[![PyPI](https://img.shields.io/pypi/v/sleepydatapeek.svg)](https://pypi.org/project/sleepydatapeek/)
[![Python](https://img.shields.io/pypi/pyversions/sleepydatapeek.svg)](https://pypi.org/project/sleepydatapeek/)
[![License](https://img.shields.io/badge/license-GPL--3.0--or--later-blue.svg)](LICENSE)

</div>

`sleepydatapeek` is a [Typer](https://typer.tiangolo.com/) CLI for taking a quick look at tabular data files — print a tidy overview + schema + sample of any `csv`/`parquet`/`json`/`pkl`/`xlsx` (and metadata for `pdf`/images), or generate a shareable markdown + PDF report with charts.

## Install

```sh
uv tool install sleepydatapeek     # or: pipx install sleepydatapeek
```

> `-v` / `--version` prints the version and best-effort checks PyPI for a newer release — it works even when placed within another command.

**Native libraries:** PDF reports use [WeasyPrint](https://weasyprint.org/), which needs pango/cairo/gdk-pixbuf. On macOS: `brew install pango`. On Debian/Ubuntu: `apt install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0`. See the [WeasyPrint docs](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html) for other platforms.

## Configure

`sleepydatapeek` is a _sleepy util_ and reads its settings from the shared `~/sleepyconfig/params.yml`, using the `datapeek_` key prefix. If the file is absent it writes **only its own section** (below) and says so; if a value it needs is missing it prints this snippet and asks you to verify your config.

```yaml
# sleepydatapeek
datapeek_sample_size: 5              # rows shown in the sample table
datapeek_table_style: rounded_grid   # any tabulate style (simple, github, …)
```

## Supported files

| Kind | Extensions |
| --- | --- |
| **Data** (schema + sample) | `csv`, `parquet`, `json`, `pkl`, `xlsx` |
| **Metadata** (file facts) | `pdf`, `png`, `jpg`, `jpeg` |

## Commands

| Command | What it does |
| --- | --- |
| [`summary`](#summary) | Print an overview, schema, and sample of a file |
| [`report`](#report) | Write a markdown + PDF report with charts |
| [`about`](#about) | Print the project's PyPI + GitHub links |

---

## `summary`

Print a concise overview, schema, and sample of a data file. Table style + sample size come from your [config](#configure).

```console
$ sleepydatapeek summary sales.csv

╭─────────────┬───────────╮
│ File        │ sales.csv │
├─────────────┼───────────┤
│ File size   │ 1.02 MB   │
├─────────────┼───────────┤
│ Rows        │ 15230     │
├─────────────┼───────────┤
│ Columns     │ 6         │
├─────────────┼───────────┤
│ Index       │ index     │
├─────────────┼───────────┤
│ Index dtype │ int64     │
╰─────────────┴───────────╯

Schema
╭────────────┬─────────╮
│ order_id   │ int64   │
├────────────┼─────────┤
│ region     │ object  │
├────────────┼─────────┤
│ product    │ object  │
├────────────┼─────────┤
│ quantity   │ int64   │
├────────────┼─────────┤
│ revenue    │ float64 │
├────────────┼─────────┤
│ ordered_at │ object  │
╰────────────┴─────────╯

Sample (5 rows)
╭────┬────────────┬────────────┬───────────┬────────────┬───────────┬──────────────╮
│    │   order_id │ region     │ product   │   quantity │   revenue │ ordered_at   │
├────┼────────────┼────────────┼───────────┼────────────┼───────────┼──────────────┤
│  0 │       1001 │ us-west-2  │ Widget    │          3 │     59.97 │ 2026-01-04   │
├────┼────────────┼────────────┼───────────┼────────────┼───────────┼──────────────┤
│  1 │       1002 │ eu-west-1  │ Gizmo     │          1 │     12.5  │ 2026-01-04   │
├────┼────────────┼────────────┼───────────┼────────────┼───────────┼──────────────┤
│  2 │       1003 │ us-west-2  │ Sprocket  │          5 │    210    │ 2026-01-05   │
├────┼────────────┼────────────┼───────────┼────────────┼───────────┼──────────────┤
│  3 │       1004 │ ap-south-1 │ Widget    │          2 │     39.98 │ 2026-01-05   │
├────┼────────────┼────────────┼───────────┼────────────┼───────────┼──────────────┤
│  4 │       1005 │ eu-west-1  │ Cog       │          4 │      8    │ 2026-01-06   │
╰────┴────────────┴────────────┴───────────┴────────────┴───────────┴──────────────╯
```

Point it at a `pdf` or image instead and it prints that file's metadata (dimensions, page count, EXIF, …) in the same style. When a table is too wide, extra columns are elided with a `⚠️ too wide` note.

## `report`

Generate a markdown report + rendered PDF + summary charts for a data file. The PDF is copied to your clipboard (macOS) so it's ready to paste. `--groupby <column>` adds a grouped row-count table; the output folder defaults to `<file>_report`.

```console
$ sleepydatapeek report sales.csv --groupby region

Report folder: /Users/dingus/work/sales_report
Relative path: sales_report
  markdown: sales.md
  pdf:      sales.pdf
PDF copied to clipboard — ready to paste.
Open with Zed: zed /Users/dingus/work/sales_report
Open with VS Code: code /Users/dingus/work/sales_report
Open PDF: open /Users/dingus/work/sales_report/sales.pdf
Reveal in Finder: open -R /Users/dingus/work/sales_report/sales.pdf
```

The folder gets the markdown, the PDF, and chart PNGs (null-counts and distinct-counts per column). `report` only accepts data files.

## `about`

Print the installed version alongside the project's public PyPI and GitHub links.

```console
$ sleepydatapeek about

sleepydatapeek 2.3.1
PyPI:   https://pypi.org/project/sleepydatapeek/
GitHub: https://github.com/anthonybench/datapeek
```

## Development

```sh
uv venv
uv pip install -e ".[dev]"
uv run pytest          # or ./tools/test.sh
```

## Documentation

- [Specification](docs/SPEC.md) — what the tool does
- [Project outline](docs/OUTLINE.md) — repository layout
- [Test drive](docs/test_drive.md) — setup, testing, and CLI usage
- [Adding a command](docs/new_command.md) — how to extend the CLI
- [Publishing](docs/publish.md) — release to PyPI
