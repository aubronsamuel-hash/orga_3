$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
Write-Host "== Ruff =="
backend.venv\Scripts\python -m ruff check backend
Write-Host "== mypy =="
python tools/mypy_backend.py
Write-Host "== pytest ciblé =="
backend.venv\Scripts\python -m pytest -q --disable-warnings --maxfail=1 -k "reports_monthly_users or exports_ics"
