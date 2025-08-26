Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

Write-Host "[test_all] Lints + Tests..." -ForegroundColor Cyan

$venv = Join-Path "backend" ".venv"
$py = Join-Path $venv "Scripts\python.exe"

& $py -m ruff check backend
& $py -m mypy --config-file backend\mypy.ini backend

# Ensure PYTHONPATH=backend for app imports
$Env:PYTHONPATH = "backend"
& $py -m pytest -q --maxfail=1 --disable-warnings --cov=backend --cov-report=xml:coverage.xml

Push-Location "frontend"
npm run lint
Pop-Location

Write-Host "[test_all] OK" -ForegroundColor Green
exit 0
