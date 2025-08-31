Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

Write-Host "[e2e] Lancement Playwright (conflits)..."

# Frontend suppose lance sur 5173, Backend sur 8000

$env:PLAYWRIGHT_BASE_URL = $env:FE_BASE_URL
if (-not $env:PLAYWRIGHT_BASE_URL) { $env:PLAYWRIGHT_BASE_URL = "http://localhost:5173" }

pushd frontend
if (Test-Path package.json) {
  if (-not (Test-Path node_modules)) { npm ci }
  npx playwright install --with-deps
  npx playwright test tests/e2e/conflicts.spec.ts --reporter=line
} else {
  Write-Error "Frontend manquant" ; exit 2
}
popd
