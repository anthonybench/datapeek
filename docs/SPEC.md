# sleepydatapeek Specification

`sleepydatapeek` is a [Typer](https://typer.tiangolo.com/)-based CLI that quickly summarizes data files and glances metadata for document and image files. Tabular output is rendered with the [tabulate](https://pypi.org/project/tabulate/) module; table styles are centralized so they can be tweaked in one place.

## File Types

**Data files** (tabular, loaded into a pandas dataframe):

- `csv`
- `parquet`
- `json`
- `pkl`
- `xlsx`

**Metadata files** (inspected for interesting metadata only):

- `pdf`
- `png`
- `jpg` / `jpeg`

The commands accept either kind unless noted; the output differs by file kind but the command-line interface does not.

## `summary` Command

```sh
sleepydatapeek summary <input_file>
```

Prints a concise, human-readable summary to the terminal.

### Data file output

- **Overview** — file path, file size, row count, column count, and the index column's name and pandas dtype. Rendered as a key/value table with no title or header row.
- **Schema** — one row per column: column name and pandas dtype, with no header row. Shown above the sample.
- **Sample** — the first 5 rows. Only the first 7 columns are shown; when more columns exist, the remainder are elided and a `⚠️ too wide, n columns elided` warning is displayed under the `Sample (5 rows)` heading.

The 5-row and 7-column limits are configurable. All summary tables share a single tabulate style.

### Metadata file output

- **Overview** — file path, file size, and file type.
- **Metadata** — a succinct selection of interesting fields, not an exhaustive dump. For example:
  - PDFs: title, author, creator, producer, creation/modified dates, page count.
  - Images: format, dimensions, color mode, DPI, and a small subset of EXIF fields (make, model, capture/modify timestamps).

## `report` Command

```sh
sleepydatapeek report <input_file> [output_dir] [--groupby <column>]
```

Generates a full report for a **data file** and writes all artifacts into `output_dir`:

- a markdown report (`<file>.md`),
- a rendered PDF of that report (`<file>.pdf`),
- chart images in a `<file>_assets/` directory.

`output_dir` is optional; when omitted it defaults to `<file>_report` in the current working directory.

The report contains everything from the `summary` command plus seaborn charts:

- null-count comparison across columns,
- distinct-value-count comparison across columns,
- when `--groupby <column>` is provided, a grouped row-count table giving the number of rows for each distinct value of the column.

The PDF is produced by rendering the markdown to HTML and converting it with WeasyPrint; relative chart-image links are resolved against the report folder.

On macOS the generated PDF is copied to the clipboard so it is ready to paste. After writing, the command prints the report folder, the markdown and PDF filenames, the clipboard status, and convenience commands to open the output in Zed, VS Code, or Finder.

Metadata files are rejected with an error and a help message; only data files are supported.
