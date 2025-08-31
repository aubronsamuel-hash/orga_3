# Windows-first repro Storybook CI
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$frontend = Join-Path $PSScriptRoot "..\frontend"
Push-Location $frontend
try {
  npm ci --no-audit --no-fund
  npm run build-storybook -- --quiet

  # Lance un serveur local Storybook
  $proc = Start-Process -FilePath "npx" -ArgumentList @("--yes","http-server","storybook-static","-p","6006") -NoNewWindow -PassThru

  $ok = $false
  for ($i=0; $i -lt 30; $i++) {
    try {
      Invoke-WebRequest -Uri "http://127.0.0.1:6006/" -UseBasicParsing -TimeoutSec 2 | Out-Null
      $ok = $true
      break
    } catch {
      Start-Sleep -Seconds 1
    }
  }

  if (-not $ok) {
    Write-Error "storybook not ready"
    exit 3
  }

  Write-Host "OK: Storybook sert sur http://127.0.0.1:6006/"
  exit 0
}
finally {
  Pop-Location
}
