# Reproduction locale Windows-first du job "storybook / storybook-tests"

# Strict mode

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# Chemins

$repoRoot = Split-Path -Parent $PSScriptRoot
$frontendDir = Join-Path $repoRoot "frontend"

Write-Host "[INFO] Frontend: $frontendDir"

Push-Location $frontendDir
try {
  Write-Host "[INFO] npm ci"
  npm ci

  Write-Host "[INFO] Build Storybook (static)"
  npm run build:storybook -- --quiet

  Write-Host "[INFO] Serve storybook-static on :6006"
  $httpServer = Start-Process -FilePath "npx" -ArgumentList @("http-server", "storybook-static", "-p", "6006") -PassThru

  Start-Sleep -Seconds 3

  Write-Host "[INFO] Run Storybook test-runner against http://127.0.0.1:6006"
  npx storybook@latest test --url http://127.0.0.1:6006 --ci
}
finally {
  if ($httpServer -and !$httpServer.HasExited) {
    Write-Host "[INFO] Stopping http-server (PID: $($httpServer.Id))"
    Stop-Process -Id $httpServer.Id -Force
  }
  Pop-Location
}
