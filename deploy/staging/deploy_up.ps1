Param(
    [string]$EnvFile = ".env"
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $here
if (!(Test-Path $EnvFile)) { Write-Error "Fichier $EnvFile manquant" ; exit 2 }
Write-Host "[INFO] Chargement env depuis $EnvFile"
$envLines = Get-Content $EnvFile | Where-Object {$_ -and $_ -notmatch "^#"}
foreach ($line in $envLines) { $k,$v = $line -split "=",2 ; if ($k) { [Environment]::SetEnvironmentVariable($k,$v) } }
Write-Host "[INFO] Docker compose up -d"
docker compose -f compose.yaml --env-file $EnvFile up -d --remove-orphans
Write-Host "[INFO] Attente sante services..."
$retries = 60
while ($retries -gt 0) {
    $health = docker ps --format "{{.Names}} {{.Status}}" | Select-String "healthy"
    if ($health -and ($health.ToString() -match "backend") -and ($health.ToString() -match "frontend") -and ($health.ToString() -match "caddy")) { break }
    Start-Sleep -Seconds 5
    $retries--
}
if ($retries -le 0) { Write-Error "Services non healthy" ; exit 3 }
Write-Host "[OK] Staging demarre."
Pop-Location
exit 0
