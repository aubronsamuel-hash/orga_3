Param(
    [switch]$SkipInstall = $false
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$root = Split-Path -Parent $PSScriptRoot
$frontend = Join-Path $root "frontend"

Write-Host "[i] Build Storybook (Windows)"
Push-Location $frontend
try {
    if (-not $SkipInstall) {
        npm ci
    }
    $env:NODE_OPTIONS="--max-old-space-size=4096"
    npx storybook build
    Write-Host "[OK] Storybook construit dans frontend/storybook-static"
    exit 0
}
catch {
    Write-Error "Echec build Storybook: $($_.Exception.Message)"
    exit 2
}
finally {
    Pop-Location
}
