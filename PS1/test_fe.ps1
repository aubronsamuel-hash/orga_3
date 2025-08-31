# Windows-first, ASCII only
Set-Location $PSScriptRoot\..\frontend
npm ci
npx playwright install
npm run lint
npm run test
$env:E2E_BASE_URL = "http://localhost:5173"
npm run e2e:smoke

