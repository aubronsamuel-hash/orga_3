$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$base = if ($Env:API_BASE) { $Env:API_BASE } else { "http://localhost:8000" }
$project = "project-demo"
$from = "2025-08-01"
$to = "2025-08-31"
$u = "$base/api/v1/exports/ics?project_id=$project&date_from=$from&date_to=$to"
Write-Host "GET $u"
$r = Invoke-WebRequest -Uri $u -Method GET -TimeoutSec 20 -ErrorAction Stop
if ($r.StatusCode -eq 200 -and $r.Content -match "BEGIN:VCALENDAR") {
  Write-Host "OK ICS"
  exit 0
} else {
  Write-Error "ERREUR ICS: $($r.StatusCode)"
  exit 4
}

