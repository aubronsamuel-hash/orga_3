Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

# Force le chemin de recherche pour mypy
$env:MYPYPATH = "backend"
$python = if (Test-Path "backend.venv\Scripts\python.exe") { "backend.venv\Scripts\python" } else { "python" }
& $python -m mypy --config-file mypy.ini
