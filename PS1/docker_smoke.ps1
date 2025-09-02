$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

docker build -t cc-backend .
docker run -d --rm -p 8000:8000 --name cc-backend cc-backend | Out-Null
try {
    for ($i=0; $i -lt 30; $i++) {
        try {
            Invoke-WebRequest -Uri "http://localhost:8000/healthz" -UseBasicParsing -TimeoutSec 2 | Out-Null
            Write-Host "OK /healthz"
            exit 0
        } catch { Start-Sleep -Seconds 2 }
    }
    Write-Error "backend not ready"
    exit 3
} finally {
    docker rm -f cc-backend | Out-Null
}
