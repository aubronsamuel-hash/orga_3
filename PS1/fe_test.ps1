Param()
$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest
Push-Location (Join-Path (Get-Location) "frontend")
try {
npm ci --no-audit --no-fund --registry=https://registry.npmjs.org/
npm run lint
npm run typecheck
npm run test:unit
} finally { Pop-Location }
