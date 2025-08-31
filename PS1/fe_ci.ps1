$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$fe = Join-Path $here "..\frontend"
Set-Location $fe

# Install
npm ci --no-audit --no-fund
# Browsers (local smoke)
npx playwright install

# Lints + tests
npm run lint
npm run test

# Smoke e2e
$env:E2E_BASE_URL = "http://localhost:5173"
npm run e2e:smoke
