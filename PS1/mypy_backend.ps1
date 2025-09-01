Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

# Choix python (Windows-first)

$python = if (Test-Path "backend.venv\Scripts\python.exe") { "backend.venv\Scripts\python" } else { "python" }

# Forcer cwd=backend et exposer nos stubs

$sep = [IO.Path]::PathSeparator  # ';' sur Windows, ':' sur Linux/mac
$env:MYPYPATH = @("typing_stubs") -join $sep

pushd backend
& $python -m mypy --config-file ../mypy.ini app tests
$code = $LASTEXITCODE
popd

exit $code
