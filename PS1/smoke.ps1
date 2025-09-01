Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest
$base = $Env:API_BASE
if (-not $base) { $base = "http://localhost:8000" }
Write-Host "Ping $base/api/v1/conflicts/user/1"
try {
  $code = (Invoke-WebRequest -UseBasicParsing -Uri "$base/api/v1/conflicts/user/1").StatusCode
  Write-Host "HTTP $code"
  if ($code -ne 200) { exit 4 }
} catch {
  Write-Error $_
  exit 4
}

