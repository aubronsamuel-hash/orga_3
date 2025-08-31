Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest
Write-Host "[smoke] Ping BE/FE..."
curl.exe -s http://localhost:8000/health || exit 4
curl.exe -s http://localhost:5173 || exit 4
Write-Host "[smoke] Conflits endpoint..."
curl.exe -s "http://localhost:8000/api/v1/conflicts?from=2025-09-01T00:00:00Z&to=2025-09-30T00:00:00Z" | Out-Null
Write-Host "OK" ; exit 0
