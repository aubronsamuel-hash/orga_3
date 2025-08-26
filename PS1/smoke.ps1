Param()
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

Check "backend /healthz" "http://localhost:8000/healthz"
Check "backend /metrics" "http://localhost:8000/metrics"
Write-Host "[smoke] Prometheus UI: http://localhost:9090  Grafana: http://localhost:3000  Mailpit: http://localhost:8025" -ForegroundColor Cyan
exit 0
