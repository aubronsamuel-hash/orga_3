Param(
  [string]$ProjectToken = $Env:CHROMATIC_PROJECT_TOKEN
)
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest
if (-not $ProjectToken) {
  Write-Error "CHROMATIC_PROJECT_TOKEN manquant (env ou parametre)."
  exit 5
}
Push-Location (Join-Path $PSScriptRoot "..\frontend")
try {
  if (Test-Path "package-lock.json") {
    npm ci
  } else {
    Write-Host "ATTENTION: aucun package-lock.json trouve" -ForegroundColor Yellow
    npm install
  }
  $env:NODE_OPTIONS="--max-old-space-size=4096"
  npx chromatic --project-token $ProjectToken --ci --only-changed --exit-zero-on-changes --auto-accept-changes
} finally {
  Pop-Location
}
