Param(
[int]$Port = 6006
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

Push-Location (Join-Path $PSScriptRoot "..")
try {
  if (-not (Test-Path "node_modules")) {
    Write-Host "[INFO] Installation des dependances NPM..."
    npm ci
  }

  Write-Host "[INFO] Build Storybook..."
  npm run build-storybook -- --quiet

  Write-Host "[INFO] Serve Storybook et lancer test-storybook..."
  $server = Start-Process -FilePath "npx" -ArgumentList @("http-server","storybook-static","-p",$Port) -PassThru
  Start-Sleep -Seconds 3

  npx test-storybook --url "http://127.0.0.1:$Port" --maxWorkers=2
}
catch {
  Write-Error "Echec E2E Storybook: $($_.Exception.Message)"
  exit 3
}
finally {
  if ($server -and -not $server.HasExited) {
    Stop-Process -Id $server.Id -Force
  }
  Pop-Location
}
