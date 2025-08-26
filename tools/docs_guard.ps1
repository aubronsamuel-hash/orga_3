Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

# Echec si code change et README.md ou docs/ non mis a jour (heuristique simple)

$changed = git diff --name-only HEAD~1 | Where-Object { $_ -match "^(backend|frontend|PS1|tools|\.github)" }
if ($changed) {
    $docsChanged = git diff --name-only HEAD~1 | Where-Object { $_ -match "^(README.md|docs/)" }
    if (-not $docsChanged) {
        Write-Error "Docs guard: des changements code sans mise a jour README/docs."
        exit 1
    }
}
Write-Host "Docs guard OK"
exit 0
