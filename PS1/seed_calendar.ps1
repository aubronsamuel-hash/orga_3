param(
  [string]$BaseUrl = "http://localhost:8000",
  [string]$Token = ""
)
$Headers = @{ "Content-Type" = "application/json" }
if ($Token -ne "") { $Headers["Authorization"] = "Bearer $Token" }

$body = @(
  @{ id="a1"; title="Mission A"; start="2025-09-01T09:00:00Z"; end="2025-09-01T11:00:00Z"; status="ACCEPTED" },
  @{ id="b1"; title="Mission B"; start="2025-09-01T13:00:00Z"; end="2025-09-01T14:00:00Z"; status="INVITED" }
) | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/calendar/seed" -Headers $Headers -Body $body
Write-Host "Seed OK"
