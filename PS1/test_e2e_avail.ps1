Param(
    [string]$DB_URL = $Env:DATABASE_URL
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
Write-Host "[E2E] Disponibilites"
$Env:PYTHONPATH="backend"
backend.venv\Scripts\python -m pytest -q -k "availabilities" --disable-warnings --maxfail=1
