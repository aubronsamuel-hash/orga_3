param(
  [switch]$E2E
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location frontend
try {
  npm ci --no-audit --no-fund
  npm run -s test:unit
  if ($E2E) { npm run -s test:e2e }
} finally {
  Pop-Location
}
