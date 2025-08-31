Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

# Delimiteur path cross-OS

$sep = [IO.Path]::PathSeparator  # ';' sur Windows, ':' sur Linux/mac
$env:MYPYPATH = @("backend/typings","backend") -join $sep

$python = if (Test-Path "backend.venv\Scripts\python.exe") { "backend.venv\Scripts\python" } else { "python" }
& $python -m mypy --config-file mypy.ini
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
