Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

Write-Host "[smoke] Ping API..." -ForegroundColor Cyan
try {
    $resp = Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:8000/api/v1/ping" -TimeoutSec 5
    if ($resp.StatusCode -ne 200) { Write-Error "Code HTTP inattendu: $( $resp.StatusCode)"; exit 4 }
    Write-Host $resp.Content
} catch {
    Write-Error "Echec ping API: $($_.Exception.Message)"; exit 4
}
Write-Host "[smoke] OK" -ForegroundColor Green
exit 0
