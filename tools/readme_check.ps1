Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

# Verifie sections requises dans README.md

$readme = Get-Content -Path "README.md" -Raw
$required = @("Quickstart Windows","Scripts clefs","Envs requis","Ports","Tests/Lint","FAQ","Badges","README Policy","Dependances et lockfiles")
foreach ($s in $required) {
    if ($readme -notmatch [regex]::Escape($s)) {
        Write-Error "README incomplet: section manquante: $s"
        exit 1
    }
}
Write-Host "README structure OK"
exit 0
