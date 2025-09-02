# Repro locale du job "storybook / storybook-tests"

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$repoRoot   = Split-Path -Parent $PSScriptRoot
$frontendDir = Join-Path $repoRoot "frontend"

Write-Host "[INFO] Frontend: $frontendDir"
Push-Location $frontendDir
try {
Write-Host "[INFO] npm ci"
npm ci

Write-Host "[INFO] Lancer les tests Storybook en mode CI (build + http-server + runner)"
npm run test-storybook-ci
}
finally {

# http-server est termine par le runner a la fin; si besoin, tuer les reliquats

Get-Process -Name "http-server" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Pop-Location
}

