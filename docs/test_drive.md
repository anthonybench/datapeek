# Test Drive Guide

## Setup

Create a virtual environment and install the package with dev dependencies using [uv](https://docs.astral.sh/uv/):

```bash
uv venv
uv pip install -e ".[dev]"
```

The `-e` flag installs in editable mode — changes to source files take effect immediately without reinstalling.

PDF report generation needs WeasyPrint's native libraries; see [`README.md`](../README.md) for the platform-specific install (`brew install pango` on macOS).

## Running Tests

```bash
uv run pytest tests/
```

To see verbose output:

```bash
uv run pytest tests/ -v
```

## Using the CLI

After setup, the `sleepydatapeek` command is available in your shell.

### `summary` — inspect a file

```bash
sleepydatapeek summary <file_path>
```

Prints an overview, schema, and a sample of rows to the terminal. When a table is too wide, columns beyond the configured limit are elided with a warning.

**Supported file types:** `.csv`, `.parquet`, `.json`, `.pkl`, `.xlsx`, `.pdf`, `.png`, `.jpg`, `.jpeg`

Example:

```bash
sleepydatapeek summary data/sales.csv
```

### `report` — generate a markdown + PDF report

```bash
sleepydatapeek report <input_file> [output_dir] [--groupby <column>]
```

Writes a markdown report, a rendered PDF, and chart PNGs into `output_dir`. Chart assets are saved in a `<file>_assets/` directory alongside the report. On macOS the generated PDF is copied to the clipboard, ready to paste.

`output_dir` is optional; when omitted it defaults to `<file>_report` in the current working directory.

Only data files are accepted (`.csv`, `.parquet`, `.json`, `.pkl`, `.xlsx`).

**Options:**

| Option               | Description                                            |
| -------------------- | ------------------------------------------------------ |
| `--groupby <column>` | Include a grouped row-count table for the given column |

Example:

```bash
sleepydatapeek report data/sales.csv reports/sales_report --groupby Region
```

After the report is written, the command prints the report folder, the markdown and PDF filenames, the clipboard status, and commands to open it in Zed, VS Code, or Finder.

## Quick Smoke Test

The repository ships a script that exercises both commands against the bundled sample data in `_ephemeral/test_data/`:

```bash
./tools/test.sh
```

It writes summaries to `_ephemeral/test_output/summary/` and reports to `_ephemeral/test_output/`.

To try it on your own data instead, create a file and run both commands:

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Carol"],
    "age": [30, 25, None],
    "city": ["NY", "LA", "NY"],
})
df.to_csv("sample.csv", index=False)
```

```bash
sleepydatapeek summary sample.csv
sleepydatapeek report sample.csv --groupby city
```

## Teardown

```bash
rm -rf .venv
```
