Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

# Choix python

$python = if (Test-Path "backend.venv\Scripts\python.exe") { "backend.venv\Scripts\python" } else { "python" }

# Lancer mypy depuis backend pour resoudre 'app' et 'tests'

pushd backend
& $python -m mypy --config-file ../mypy.ini app tests
$code = $LASTEXITCODE
popd
if ($code -ne 0) { exit $code }
