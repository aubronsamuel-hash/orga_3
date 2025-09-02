$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

Write-Host "== Ruff =="
backend.venv\Scripts\python -m ruff check backend

Write-Host "== mypy backend =="
backend.venv\Scripts\python tools/mypy_backend.py

Write-Host "== E2E FE smoke =="
cd frontend
npm run e2e:smoke
cd ..
