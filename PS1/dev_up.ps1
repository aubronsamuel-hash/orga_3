Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

function Fail($code, $msg) { Write-Host $msg -ForegroundColor Red; exit $code }

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Fail 2 "Prerequis manquants: Docker n est pas installe (EXIT 2 PREREQUIS_MANQUANTS)."
}

$compose = Join-Path (Get-Location) "deploy/dev/compose.yaml"
if (-not (Test-Path $compose)) { Fail 1 "Usage invalide: fichier compose introuvable: $compose" }

Write-Host "[dev_up] Lancement docker compose..." -ForegroundColor Cyan
docker compose -f $compose up -d

Write-Host "[dev_up] Attente backend..." -ForegroundColor Cyan
$max = 60
for ($i=0; $i -lt $max; $i++) {
    try {
        $res = Invoke-WebRequest -Uri "http://localhost:8000/healthz" -UseBasicParsing -TimeoutSec 2
        if ($res.StatusCode -eq 200) { Write-Host "[dev_up] OK /healthz=200" -ForegroundColor Green; break }
    } catch {}
    Start-Sleep -Seconds 2
    if ($i -eq ($max-1)) { Fail 3 "Timeout: backend non pret (EXIT 3 TIMEOUT)." }
}

Write-Host "[dev_up] Stack dev up. URLs: BE http://localhost:8000 ; Prom http://localhost:9090 ; Grafana http://localhost:3000 ; Loki 3100 ; Redis 6379 ; PG 5432 ; Mailpit http://localhost:8025 ; Adminer http://localhost:8080" -ForegroundColor Green
exit 0
