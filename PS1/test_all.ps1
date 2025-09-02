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
Write-Host "== Pytest backend =="
& $py -m pytest -q --disable-warnings --maxfail=1

Push-Location "frontend"
npm run lint
Write-Host "== E2E FE smoke =="
npm run e2e:smoke
Pop-Location

Write-Host "[test_all] OK" -ForegroundColor Green
exit 0
