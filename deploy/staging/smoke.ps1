Param(
    [Parameter(Mandatory=$true)][string]$BaseUrl
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
function Test-Url($u) {
    try { (Invoke-WebRequest -Uri $u -UseBasicParsing -TimeoutSec 10).StatusCode } catch { -1 }
}
$fe = Test-Url "$BaseUrl/"
$hz = Test-Url "$BaseUrl/healthz"
$be = Test-Url "$BaseUrl/api/v1/health"
Write-Host "FE: $fe | /healthz: $hz | API: $be"
if ($fe -ne 200 -or $hz -ne 200 -or $be -ne 200) { Write-Error "Smoke KO" ; exit 4 }
Write-Host "Smoke OK"
exit 0
