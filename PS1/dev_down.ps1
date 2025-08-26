Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

Write-Host "[dev_down] Arret des processus uvicorn/npm..." -ForegroundColor Cyan
Get-Process | Where-Object { $_.Path -like "*uvicorn.exe" -or $_.ProcessName -like "node" } | ForEach-Object { Stop-Process -Id $_.Id -Force }
Write-Host "[dev_down] OK" -ForegroundColor Green
exit 0
