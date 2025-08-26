Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest
$Env:PYTHONPATH="backend"
backend.venv\Scripts\python -m pytest -q -k "obs or readiness or metrics"
