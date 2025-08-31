#Requires -Version 7.0
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

Push-Location (Join-Path $PSScriptRoot "..\frontend")
try {
  if (Test-Path package-lock.json) {
    npm ci
  } else {
    npm install
  }
  npx playwright install --with-deps
  npm run test:e2e -- --project=chromium
} finally {
  Pop-Location
}

