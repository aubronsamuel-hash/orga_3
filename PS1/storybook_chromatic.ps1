Param(
    [switch]$DryRun = $false
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if ([string]::IsNullOrWhiteSpace($Env:CHROMATIC_PROJECT_TOKEN)) {
    Write-Warning "CHROMATIC_PROJECT_TOKEN absent. Publication Chromatic sautee."
    exit 0
}

$root = Split-Path -Parent $PSScriptRoot
$frontend = Join-Path $root "frontend"

Push-Location $frontend
try {
    if ($DryRun) {
        Write-Host "[i] DryRun Chromatic. Commande affichee:"
        Write-Host "npx chromatic --project-token *** --ci --only-changed --exit-zero-on-changes --auto-accept-changes"
        exit 0
    }
    npx chromatic --project-token $Env:CHROMATIC_PROJECT_TOKEN --ci --build-script-name build:storybook --only-changed --exit-zero-on-changes --auto-accept-changes
    Write-Host "[OK] Publication Chromatic reussie."
    exit 0
}
catch {
    Write-Error "Echec Chromatic: $($_.Exception.Message)"
    exit 5
}
finally {
    Pop-Location
}
