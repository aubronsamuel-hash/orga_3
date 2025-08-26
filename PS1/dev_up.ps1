Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

Write-Host "[dev_up] Lancement BE/FE..." -ForegroundColor Cyan

# Backend

$env:ENV="dev"
$env:TZ="UTC"
$venv = Join-Path "backend" ".venv"
$uvicorn = Join-Path $venv "Scripts\uvicorn.exe"
Start-Process -FilePath $uvicorn -ArgumentList "app.main:app","--reload","--host",$Env:BACKEND_HOST,"--port",$Env:BACKEND_PORT -WorkingDirectory "backend" -WindowStyle Hidden

# Frontend

Push-Location "frontend"
Start-Process -FilePath "npm" -ArgumentList "run","dev" -WindowStyle Hidden
Pop-Location

Write-Host "[dev_up] Services demarres (BE 8000, FE 5173)" -ForegroundColor Green
exit 0
