Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

Write-Host "[test_all] Lints + Tests..." -ForegroundColor Cyan

$venv = Join-Path "backend" ".venv"
& (Join-Path $venv "Scripts\python.exe") -m ruff check backend
& (Join-Path $venv "Scripts\python.exe") -m mypy backend
& (Join-Path $venv "Scripts\pytest.exe") -q --maxfail=1 --disable-warnings --cov=backend --cov-report=xml:coverage.xml

Push-Location "frontend"
npm run lint
Pop-Location

Write-Host "[test_all] OK" -ForegroundColor Green
exit 0
