$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest
Write-Host "== Pytest backend (UTC py310 fix) =="
backend.venv\Scripts\python -m pytest -q --disable-warnings --maxfail=1
