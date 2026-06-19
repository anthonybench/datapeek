#!/bin/zsh

# Test tool usage, expects `_ephemeral/test_data/*`, either `test.*` or `test_wide.*` for supported input formats.
#
# Usage:
#   ./tools/test.sh

set -euo pipefail

REPO_ROOT="${0:A:h}/.."
REPO_ROOT="$(cd "$REPO_ROOT" && pwd)"
DATA_DIR="$REPO_ROOT/_ephemeral/test_data"
OUT_DIR="$REPO_ROOT/_ephemeral/test_output"
SUMMARY_OUT_DIR="$OUT_DIR/summary"

# Prefer the installed console script; fall back to running the module.
if command -v sleepydatapeek >/dev/null 2>&1; then
    DATAPEEK=(sleepydatapeek)
else
    DATAPEEK=(python -m sleepydatapeek.main)
fi

mkdir -p "$SUMMARY_OUT_DIR"

# Map each supported format to its sample file. `summary` accepts both tabular
# data files (csv/parquet use the wide variants) and metadata-only files
# (pdf/png/jpg), so exercise all of them.
SUMMARY_FILES=(
    "test_wide.csv"
    "test.json"
    "test_wide.parquet"
    "test.pkl"
    "test.xlsx"
    "resume.pdf"
    "img.png"
    "img.jpg"
)

echo "==> summary"
for sample in "${SUMMARY_FILES[@]}"; do
    out="$SUMMARY_OUT_DIR/${sample}.txt"
    echo "  - $sample -> ${out#"$REPO_ROOT/"}"
    "${DATAPEEK[@]}" summary "$DATA_DIR/$sample" >"$out"
done

echo "==> report"
"${DATAPEEK[@]}" report "$DATA_DIR/pokemon.csv" "$OUT_DIR/pokemon_report"
"${DATAPEEK[@]}" report --groupby="Type 1" "$DATA_DIR/pokemon.csv" "$OUT_DIR/pokemon_report_grouped"

echo "==> done; output under ${OUT_DIR#"$REPO_ROOT/"}"
