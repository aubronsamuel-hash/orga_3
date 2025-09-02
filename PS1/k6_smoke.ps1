$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$base = if ($Env:K6_BASE_URL) { $Env:K6_BASE_URL } else { "http://localhost:8000" }
$vus = if ($Env:K6_VUS) { $Env:K6_VUS } else { "5" }
$dur = if ($Env:K6_DURATION) { $Env:K6_DURATION } else { "30s" }

$script = (Join-Path $PSScriptRoot "..\deploy\k6\smoke_health.js")

Write-Host "k6 run $script (BASE=$base, VUs=$vus, DUR=$dur)"

# Degrade propre si k6 non installe

$k6 = Get-Command k6 -ErrorAction SilentlyContinue
if (-not $k6) {
  Write-Warning "k6 non installe. Mode degrade: simple ping /healthz."
  $u = "$base/healthz"
  for ($i=0; $i -lt 5; $i++) {
    try {
      Invoke-WebRequest -Uri $u -TimeoutSec 5 -UseBasicParsing | Out-Null
      Write-Host "OK /healthz (mode degrade)"; exit 0
    } catch { Start-Sleep -Seconds 1 }
  }
  Write-Error "Echec ping /healthz (mode degrade)"; exit 4
}

# k6 present

$env:K6_BASE_URL = $base
$env:K6_VUS = $vus
$env:K6_DURATION = $dur
k6 run $script
