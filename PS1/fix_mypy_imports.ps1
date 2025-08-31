Param(
    [switch]$WhatIf = $true
)
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

Write-Host "[fix] Normalisation imports tests.utils -> .utils"
$testsDir = Join-Path -Path "backend" -ChildPath "tests"
if (-not (Test-Path $testsDir)) { Write-Error "Dossier tests introuvable: $testsDir"; exit 2 }

# Cible: from tests.utils import X  -> from .utils import X

# import tests.utils as U     -> from . import utils as U

$files = Get-ChildItem -Path $testsDir -Recurse -Include *.py
$pattern1 = 'from\s+tests.utils\s+import\s+'
$pattern2 = 'import\s+tests.utils\s+as\s+'
foreach ($f in $files) {
$content = Get-Content -LiteralPath $f.FullName -Raw
$orig = $content
$content = $content -replace $pattern1, 'from .utils import '
$content = $content -replace $pattern2, 'from . import utils as '
if ($content -ne $orig) {
Write-Host "  -> Patch: $($f.FullName)"
if (-not $WhatIf) {
Set-Content -LiteralPath $f.FullName -Value $content -NoNewline
}
}
}

# Garantir __init__.py pour tests/ (package explicite)

$testsInit = Join-Path $testsDir "__init__.py"
if (-not (Test-Path $testsInit)) {
Write-Host "  -> Ajout: $testsInit"
if (-not $WhatIf) { Set-Content -LiteralPath $testsInit -Value "# package tests" }
}

Write-Host "[fix] OK"
exit 0
