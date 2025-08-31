Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest
pushd backend
if (Test-Path .venv\Scripts\python.exe) {
  .\.venv\Scripts\python -m pytest -q backend\tests\test_conflicts_service_ok.py backend\tests\test_conflicts_service_ko.py
} else {
  python -m pytest -q backend\tests\test_conflicts_service_ok.py backend\tests\test_conflicts_service_ko.py
}
popd
