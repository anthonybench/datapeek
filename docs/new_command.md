# Adding a Command

Commands are auto-discovered: drop a module in `sleepydatapeek/cli/commands/`
that exposes a `register(app)` function and it is wired up automatically by
`cli/commands/__init__.py`. No central registry to edit.

## 1. Create the command module

`sleepydatapeek/cli/commands/<name>.py`:

```python
"""Schema command for sleepydatapeek."""

from pathlib import Path

import typer

from sleepydatapeek.core.inspectors import buildFileSummary


def register(app: typer.Typer) -> None:
    """Register the schema command."""

    @app.command("schema")
    def schemaCommand(
        input_path: Path = typer.Argument(..., exists=True, readable=True, resolve_path=True),
    ) -> None:
        """Print just the schema of a supported file."""

        file_summary = buildFileSummary(input_path)
        # ... render what you need from the summary ...
        typer.echo(file_summary.kind)
```

## Conventions

- **File input**: take the path as `typer.Argument(..., exists=True, readable=True,
  resolve_path=True)` so Typer validates it before your code runs.
- **Reuse the core, don't re-read files**: `core/inspectors.py` already loads any
  supported file into a typed summary (`buildFileSummary`) and renders it
  (`renderFileSummary`); `core/reporting.py` builds the markdown/PDF report
  (`writeReport`). Most commands are a thin shell over these.
- **Formatting** goes through `utils/formatting.py` (`renderTable`,
  `renderKeyValueTable`, `renderSection`) using the configured table style.
- **Config** comes from `getConfig()` in `core/config.py`. See step 3 before
  adding any new tunable.
- Follow `AGENTS.md`: `camelCase` functions, `lower_snake_case` variables, type
  hints and docstrings on everything, `case` over `if/elif` chains.

Good examples to copy: `summary.py` (read + render to the terminal) and
`report.py` (write artifacts to a folder, with an optional argument and option).

## 2. Supporting a new file format (different extension point)

To accept a new file *type* rather than add a verb:

1. Add the suffix to `data_suffixes` or `metadata_suffixes` in `core/config.py`.
2. Add a branch to load it: `loadDataFrame` (tabular) or `buildMetadataEntries`
   (metadata-only) in `core/inspectors.py`.

Everything downstream (summary, report) then works for the new type for free.

## 3. (Only if you need new config)

Config keys are owned per-tool and use the `datapeek_` prefix. To add one:

1. Add the key + default to `DEFAULT_PARAMS` **and** `DEFAULT_PARAMS_SNIPPET` in
   `core/sleepy_params.py` (keep them in sync).
2. Add a field to `AppConfig` and read it in `getConfig()` with
   `requireParam(params, "datapeek_<name>")` in `core/config.py`.

Missing values are surfaced automatically: `requireParam` prints the tool's
snippet and asks the user to verify their `~/sleepyconfig/params.yml`.

## 4. Add a test

`tests/cli/test_<name>.py`, driving the command through `CliRunner` against a
real file written into `tmp_path` (no mocks needed — datapeek operates on files):

```python
from pathlib import Path

import pandas as pd
from typer.testing import CliRunner

from sleepydatapeek.main import app


def testSchemaCommand(tmp_path: Path) -> None:
    input_path = tmp_path / "scores.csv"
    pd.DataFrame({"name": ["Ada"], "score": [99]}).to_csv(input_path, index=False)

    result = CliRunner().invoke(app, ["schema", str(input_path)])

    assert result.exit_code == 0
```

The autouse fixture in `tests/conftest.py` isolates the sleepy config to a temp
file, so tests never touch the real `~/sleepyconfig`.

## 5. Update docs

Add the command to `README.md`, `docs/SPEC.md`, the usage guide in
`docs/test_drive.md`, and the file tree in `docs/OUTLINE.md`.
