# Project Outline

How the repository is laid out and what each area is responsible for.

```txt
sleepydatapeek/
├── sleepydatapeek/                     # Application package
│   ├── __init__.py
│   ├── main.py                   # Entrypoint: assembles the root Typer app
│   ├── cli/
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py       # Auto-registers all command modules
│   │       ├── summary.py        # `sleepydatapeek summary <file>`
│   │       └── report.py         # `sleepydatapeek report <file> [output_dir]`
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py             # App config (file suffixes, table styles, sample limits)
│   │   ├── logging.py            # Shared logging setup
│   │   ├── inspectors.py         # File loading, summary building, summary rendering
│   │   └── reporting.py          # Markdown report, charts, and PDF rendering
│   └── utils/
│       ├── __init__.py
│       ├── formatting.py         # Shared tabulate/table helpers
│       └── clipboard.py          # Copy a file onto the macOS clipboard
├── tests/
│   ├── cli/
│   │   ├── test_summary.py
│   │   └── test_report.py
│   └── core/
│       └── test_config.py
├── tools/                        # Scripts for humans to run
│   ├── format.sh                 # Format shell, Python, and Markdown
│   └── test.sh                   # Smoke-test both commands against bundled sample data
├── docs/                         # Single-purpose documentation files
│   ├── SPEC.md                   # Application specification
│   ├── OUTLINE.md                # This file
│   ├── test_drive.md             # Setup, testing, and CLI usage guide
│   ├── new_command.md            # How to add a new command
│   └── publish.md                # Release to PyPI
├── _ephemeral/                   # Scratch space (sample data, generated output)
├── AGENTS.md                     # Conventions for code, scripts, docs, and tooling
├── README.md                     # Project overview, deploy, and teardown
└── pyproject.toml                # Package metadata and dependencies
```

## Responsibilities

- **`cli/commands/`** — one module per command. Each exposes a `register(app)` function; `commands/__init__.py` discovers and registers them so new commands can be dropped in freely.
- **`core/inspectors.py`** — loads supported files into dataframes, builds typed summary objects, and renders the terminal summary output.
- **`core/reporting.py`** — builds the markdown report and seaborn charts, then renders the markdown to PDF via WeasyPrint.
- **`core/config.py`** — the single place to change supported file suffixes, tabulate table styles, and sample row/column limits.
- **`utils/`** — cross-cutting helpers with no command-specific logic (table formatting, clipboard).
