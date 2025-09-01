Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest
Push-Location (Join-Path $PSScriptRoot "..\frontend")
try {
if (Test-Path "package-lock.json") {
  npm ci
} else {
  Write-Host "ATTENTION: aucun package-lock.json trouve" -ForegroundColor Yellow
  npm install
}
$env:NODE_OPTIONS="--max-old-space-size=4096"
npx storybook build --ci
} finally {
  Pop-Location
}
