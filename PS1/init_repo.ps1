Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

Write-Host "[init_repo] Preparation du repo..." -ForegroundColor Cyan

# Ensurer encodage UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Require-Cmd($name) {
if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
Write-Error "Outil requis manquant: $name" ; exit 2
}
}
Require-Cmd "python"
Require-Cmd "npm"

# Python venv

$venv = Join-Path -Path "backend" -ChildPath ".venv"
if (-not (Test-Path $venv)) {
Write-Host "[init_repo] Creation venv..." -ForegroundColor Cyan
python -m venv $venv
}
& (Join-Path $venv "Scripts\pip.exe") install -U pip

# Installe runtime

& (Join-Path $venv "Scripts\pip.exe") install -r (Join-Path "backend" "requirements.txt")

# Installe dev si le fichier existe

$reqDev = Join-Path "backend" "requirements-dev.txt"
if (Test-Path $reqDev) {
& (Join-Path $venv "Scripts\pip.exe") install -r $reqDev
}

# Frontend install

Push-Location "frontend"
npm ci
Pop-Location

Write-Host "[init_repo] OK" -ForegroundColor Green
exit 0
