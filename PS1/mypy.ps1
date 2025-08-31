Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest
$python = if (Test-Path "backend.venv\Scripts\python.exe") { "backend.venv\Scripts\python" } else { "python" }
& $python -m mypy --config-file mypy.ini

