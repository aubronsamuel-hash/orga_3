Param(
    [switch]$Rebuild = $false
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$root = Split-Path -Parent $PSScriptRoot
$frontend = Join-Path $root "frontend"

Push-Location $frontend
try {
    if ($Rebuild) {
        Write-Host "[i] Rebuild Storybook static"
        npm ci
        $env:NODE_OPTIONS="--max-old-space-size=4096"
        npx storybook build
    }
    Write-Host "[i] Installing Playwright Chromium (if needed)"
    npx playwright install chromium | Out-Null
    Write-Host "[i] Running Storybook a11y smoke tests"
    npx start-server-and-test "http-server storybook-static -p 6006" http://127.0.0.1:6006 "test-storybook --url http://127.0.0.1:6006"
    Write-Host "[OK] Tests Storybook passes"
    exit 0
}
catch {
    Write-Error "Echec tests Storybook: $($_.Exception.Message)"
    exit 2
}
finally {
    Pop-Location
}
