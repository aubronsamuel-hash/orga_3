Param(
    [switch]$Json
)
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

$py = "backend\.venv\Scripts\python.exe"
$results = [ordered]@{}

Write-Host "[warnings-scan] Ruff..." -ForegroundColor Cyan
& $py -m ruff check backend | Tee-Object -Variable ruffOut | Out-Null
$results["ruff_ok"] = $LASTEXITCODE -eq 0
$results["ruff_lines"] = ($ruffOut | Measure-Object -Line).Lines

Write-Host "[warnings-scan] Mypy..." -ForegroundColor Cyan
& $py -m mypy --config-file backend\mypy.ini backend | Tee-Object -Variable mypyOut | Out-Null
$results["mypy_ok"] = $LASTEXITCODE -eq 0
$results["mypy_lines"] = ($mypyOut | Measure-Object -Line).Lines

Write-Host "[warnings-scan] Pytest..." -ForegroundColor Cyan
$Env:PYTHONPATH="backend"
& $py -m pytest -q --disable-warnings --maxfail=1 | Tee-Object -Variable pyOut | Out-Null
$results["pytest_ok"] = $LASTEXITCODE -eq 0

if ($Json) {
    $results | ConvertTo-Json -Compress
} else {
    Write-Host "[warnings-scan] ruff_ok=$($results["ruff_ok"]) mypy_ok=$($results["mypy_ok"]) pytest_ok=$($results["pytest_ok"])" -ForegroundColor Green
}

