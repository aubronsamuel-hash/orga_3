$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# Smoke API CSV export (degrade propre si API down)

$base = if ($Env:API_BASE) { $Env:API_BASE } else { "http://localhost:8000" }
$from = "2025-08-01"
$to = "2025-08-31"
$org = "org-demo"

try {
  $url = "$base/api/v1/exports/csv?type=monthly-users&org_id=$org&date_from=$from&date_to=$to"
  Write-Host "GET $url"
  $r = Invoke-WebRequest -Uri $url -Method GET -TimeoutSec 20 -ErrorAction Stop
  if ($r.StatusCode -eq 200) {
    Write-Host "OK CSV export"
    exit 0
  } else {
    Write-Error "ERREUR_HTTP $($r.StatusCode)"
    exit 4
  }
} catch {
  Write-Error "ERREUR_RESEAU_API: $($_.Exception.Message)"
  exit 4
}
