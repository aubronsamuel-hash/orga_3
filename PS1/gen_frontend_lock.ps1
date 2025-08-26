Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest
Write-Host "[gen_frontend_lock] Generation package-lock.json..." -ForegroundColor Cyan
if (-not (Test-Path "frontend/package.json")) {
    Write-Error "frontend/package.json introuvable"; exit 2
}
Push-Location "frontend"

# Nettoyage minimal
if (Test-Path "node_modules") { Remove-Item "node_modules" -Recurse -Force }

# Genere uniquement le lockfile sans installer tous les paquets
npm install --package-lock-only
Pop-Location
if (-not (Test-Path "frontend/package-lock.json")) {
    Write-Error "Echec generation package-lock.json"; exit 1
}
Write-Host "[gen_frontend_lock] OK" -ForegroundColor Green
exit 0
