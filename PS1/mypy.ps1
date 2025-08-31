Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

# Chemins de recherche pour mypy (code + stubs)
$env:MYPYPATH = "backend;backend/typings"

$python = if (Test-Path "backend.venv\Scripts\python.exe") { "backend.venv\Scripts\python" } else { "python" }
& $python -m mypy --config-file mypy.ini

if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

