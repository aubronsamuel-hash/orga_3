Param([switch]$Prune)
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker absent." -ForegroundColor Yellow
    exit 0
}

$compose = Join-Path (Get-Location) "deploy/dev/compose.yaml"
if (Test-Path $compose) {
    Write-Host "[dev_down] docker compose down..." -ForegroundColor Cyan
    docker compose -f $compose down
}

if ($Prune) {
    Write-Host "[dev_down] prune volumes nommes (pgdata/promdata/lokidata/grafdata)..." -ForegroundColor Yellow
    docker volume rm $(docker volume ls -q | Select-String -Pattern "pgdata|promdata|lokidata|grafdata") 2>$null | Out-Null
}
exit 0
