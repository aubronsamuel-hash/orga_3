#requires -Version 7.0
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

param(
[switch]$Frontend,
[switch]$Build,
[switch]$Dev,
[switch]$NoWait
)

# EXIT CODES

# 0 OK; 1 USAGE_INVALIDE; 2 PREREQUIS_MANQUANTS; 10 ERREUR_INTERNE

function Write-Info($msg){ Write-Host "[INFO] $msg" }
function Write-Err($msg){ Write-Host "[ERREUR] $msg"; }

# Import wrappers

$WrappersPath = Join-Path $PSScriptRoot "tools\npm_wrappers.ps1"
if (-not (Test-Path $WrappersPath)) {
    Write-Err "Fichier manquant: $WrappersPath. (EXIT 10)"
    exit 10
}
. $WrappersPath

if (-not ($Frontend)) {
    Write-Err "Usage invalide: specify -Frontend (et -Build ou -Dev). (EXIT 1)"
    exit 1
}

$frontendDir = Join-Path $PSScriptRoot "..\frontend"
if (-not (Test-Path $frontendDir)) {
    Write-Err "Repertoire frontend introuvable: $frontendDir (EXIT 10)"
    exit 10
}

Push-Location $frontendDir
try {
    Write-Info "Installation des dependances NPM (npm.cmd ci)..."
    Invoke-Npm ci

    if ($Build) {
        Write-Info "Build frontend (npm.cmd run build)..."
        Invoke-Npm run build
        Write-Info "Build termine."
    }

    if ($Dev) {
        Write-Info "Lancement du serveur de dev (npm.cmd run dev)..."
        if ($NoWait) {
            Start-Process -FilePath (Resolve-CmdTool -Name "npm") -ArgumentList "run","dev"
            Write-Info "Serveur dev lance en arriere-plan."
        } else {
            Invoke-Npm run dev
        }
    }

}
catch {
    Write-Err "Erreur pendant l initialisation frontend: $($_.Exception.Message) (EXIT 10)"
    exit 10
}
finally {
    Pop-Location
}

exit 0
