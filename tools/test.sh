#!/bin/zsh

# Runs `summary` for every supported data format (using the wide variants for
# csv and parquet) and `report` for pokemon.csv both with and without
# --groupby. All output lands under _ephemeral/test_output/.
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

# Map each supported format to its sample file (csv/parquet use the wide variants).
SUMMARY_FILES=(
	"test_wide.csv"
	"test.json"
	"test_wide.parquet"
	"test.pkl"
	"test.xlsx"
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
