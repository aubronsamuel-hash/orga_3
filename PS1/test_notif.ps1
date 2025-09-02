#Requires -Version 7
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

Write-Host "[test_notif] Lancement des tests unitaires notif"
pushd backend
python -m pytest -q tests/test_notifications_email.py tests/test_notifications_tokens.py tests/test_notifications_rate_limit.py tests/test_notifications_endpoints.py
popd

Write-Host "[test_notif] Curl endpoint test-email (MailPit requis sur 1025)"
$body = @{
    to = "dev@example.test"
    subject = "Ping"
    template = "invite"
    context = @{
        user_name = "Sam"
        mission = "Covertramp"
        accept_url = "http://localhost:5173/public/invite/accept?t=fake"
        decline_url = "http://localhost:5173/public/invite/decline?t=fake"
    }
} | ConvertTo-Json -Depth 5

curl.exe -s -X POST http://localhost:8000/api/v1/notifications/test-email -H "Content-Type: application/json" -d $body

Write-Host "[test_notif] OK"
