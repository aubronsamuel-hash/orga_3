#Requires -Version 7
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Test-Http {
param([string]$Url)
try { (Invoke-WebRequest -UseBasicParsing -Uri $Url -TimeoutSec 5).StatusCode -eq 200 } catch { $false }
}

Write-Host "[smoke] Backend /healthz"
if (-not (Test-Http -Url "http://localhost:8000/healthz")) { Write-Error "Backend KO" ; exit 4 }

Write-Host "[smoke] MailPit UI"
if (-not (Test-Http -Url "http://localhost:8025")) { Write-Warning "MailPit UI non joignable (dev)" }

Write-Host "[smoke] Notifications test-email"
$payload = '{"to":"dev@example.test","subject":"Ping","template":"invite","context":{"user_name":"Sam","mission":"Demo","accept_url":"http://x","decline_url":"http://y"}}'
try {
$resp = Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:8000/api/v1/notifications/test-email" -Method POST -Body $payload -ContentType "application/json" -TimeoutSec 10
Write-Host "[smoke] test-email status $($resp.StatusCode)"
} catch {
Write-Warning "[smoke] test-email KO: $($_.Exception.Message)"
}
