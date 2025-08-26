#!/usr/bin/env bash
set -euo pipefail
py="backend/.venv/bin/python"
echo "[warnings-scan] Ruff..."
$py -m ruff check backend || true
echo "[warnings-scan] Mypy..."
$py -m mypy --config-file backend/mypy.ini backend || true
echo "[warnings-scan] Pytest..."
PYTHONPATH=backend $py -m pytest -q --disable-warnings --maxfail=1 || true
echo "[warnings-scan] done"

