Param(
    [string]$BaseUrl = "http://localhost:8000",
    [string]$InvitationId,
    [string]$Token
)
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

function Check($name, $url) {
    try {
        $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5
        if ($r.StatusCode -ne 200) { throw "HTTP $($r.StatusCode)" }
        Write-Host "[smoke] $name OK" -ForegroundColor Green
    } catch {
        Write-Host "[smoke] $name KO: $_" -ForegroundColor Red
        exit 4
    }
}

Check "backend /healthz" "$BaseUrl/healthz"
Check "backend /metrics" "$BaseUrl/metrics"
if ($InvitationId -and $Token) {
    Check "invitation accept" "$BaseUrl/api/v1/invitations/$InvitationId/accept?token=$Token"
} else {
    Write-Host "[smoke] invitation accept skipped" -ForegroundColor Yellow
}
Write-Host "[smoke] Prometheus UI: http://localhost:9090  Grafana: http://localhost:3000  Mailpit: http://localhost:8025" -ForegroundColor Cyan
exit 0
