Param(
    [int]$UserId = 1,
    [string]$Start = "2025-09-05T09:00:00Z",
    [string]$End = "2025-09-05T18:00:00Z"
)
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest
$body = @{ user_id=$UserId; start_at=$Start; end_at=$End } | ConvertTo-Json -Compress
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/v1/availabilities" -Body $body -Headers @{ "Content-Type"="application/json"; "Authorization"="***" }
