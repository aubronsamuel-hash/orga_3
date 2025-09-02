$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

Push-Location (Join-Path $PSScriptRoot "..\..")
try {
  # Repro rapide mypy (meme logique que CI)
  $env:PYTHONPATH = "backend"
  python tools/mypy_backend.py
  Write-Host "mypy OK"
  exit 0
} catch {
  Write-Error $_.Exception.Message
  exit 1
} finally {
  Pop-Location
}
