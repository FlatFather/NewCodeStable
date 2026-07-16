#!/usr/bin/env bash
# Run the repository's deterministic workflow-quality gates.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-$REPO_ROOT/.venv/bin/python}"
TMPDIR_BASE="$REPO_ROOT/.tmp"
TMPDIR_ROOT=""

if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="${PYTHON_BIN_FALLBACK:-python3}"
fi

cleanup() {
  if [[ -n "$TMPDIR_ROOT" && -d "$TMPDIR_ROOT" ]]; then
    rm -rf "$TMPDIR_ROOT"
  fi
}
trap cleanup EXIT

mkdir -p "$TMPDIR_BASE"
TMPDIR_ROOT="$(mktemp -d "$TMPDIR_BASE/verify.XXXXXX")"
export TMPDIR="$TMPDIR_ROOT"

cd "$REPO_ROOT"
"$PYTHON_BIN" .codestable/tools/build-status.py --check --json
"$PYTHON_BIN" .codestable/tools/check-workflow-contracts.py
.codestable/tools/lint-exit-conditions.sh
"$PYTHON_BIN" -m unittest discover -s tests -v
