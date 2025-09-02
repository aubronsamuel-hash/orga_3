$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
Write-Host "== Pytest backend (PDF optional) =="
backend.venv\Scripts\python -m pytest -q --disable-warnings --maxfail=1
