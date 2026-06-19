#!/bin/zsh

# Format shell, Python, and Markdown files in the repository.
#
# Usage:
#     ./tools/format.sh

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SHELL_FILES=("${REPO_ROOT}"/tools/*.sh)

shfmt -w "${SHELL_FILES[@]}"
black "${REPO_ROOT}"
prettier --write "${REPO_ROOT}/README.md" "${REPO_ROOT}/docs/**/*.md"
