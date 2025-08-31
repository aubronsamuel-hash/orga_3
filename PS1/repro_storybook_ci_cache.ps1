Param(
    [switch]$SkipBuild
)
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

Push-Location (Join-Path $PSScriptRoot ".." "frontend")
try {
    if (-not (Test-Path "./package-lock.json")) {
        throw "Manque frontend\package-lock.json (requis par CI cache)."
    }
    if (-not $SkipBuild) {
        npm ci --no-audit --no-fund
        npm run build-storybook -- --quiet
    }
    Write-Host "OK: cache CI base sur frontend/package-lock.json et build storybook passe."
} finally {
    Pop-Location
}
