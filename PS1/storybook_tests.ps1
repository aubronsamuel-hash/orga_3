#requires -Version 7.2
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

Write-Host "[Storybook] Build + Test (Windows)" -ForegroundColor Cyan

$root = Split-Path -Parent $PSCommandPath | Split-Path -Parent
$frontend = Join-Path $root "frontend"

Push-Location $frontend
try {
  if (-Not (Test-Path "node_modules")) {
    Write-Host "npm ci..." -ForegroundColor Yellow
    npm ci
  }

  Write-Host "build-storybook..." -ForegroundColor Yellow
  npm run build-storybook -- --quiet

  Write-Host "serve static @6006..." -ForegroundColor Yellow

  # http-server en tache de fond
  Start-Process -FilePath "npx" -ArgumentList "http-server", "storybook-static", "-p", "6006" -NoNewWindow
  Start-Sleep -Seconds 3

  Write-Host "test-storybook (runner)..." -ForegroundColor Yellow
  npx test-storybook --url http://127.0.0.1:6006 --maxWorkers=2
  if ($LASTEXITCODE -ne 0) { exit 1 }
}
finally {
  Pop-Location
}
