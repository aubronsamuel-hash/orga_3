$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

Push-Location (Join-Path $PSScriptRoot "..\frontend")
try {
  if (-not (Test-Path "node_modules")) {
    npm ci
  }

  npm run build-storybook -- --quiet

  # lancer un http-server simple
  npx http-server storybook-static -p 6006 | Out-Null &
  Start-Sleep -Seconds 3

  # runner
  npx test-storybook --url http://127.0.0.1:6006 --maxWorkers=2
  if ($LASTEXITCODE -ne 0) { exit 1 }
} finally {
  Pop-Location
}
exit 0

