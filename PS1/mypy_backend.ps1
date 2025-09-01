Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest
$python = if (Test-Path "backend.venv\Scripts\python.exe") { "backend.venv\Scripts\python" } else { "python" }
pushd backend
& $python -m mypy --config-file ../mypy.ini app tests
$code = $LASTEXITCODE
popd
if ($code -ne 0) { exit $code }
