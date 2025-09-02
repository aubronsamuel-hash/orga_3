#requires -Version 7.0
[CmdletBinding()]
param(
    [switch]$SkipBackend,
    [switch]$SkipFrontend
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Info($msg) { Write-Host $msg }

# Force npm/npx .cmd (evite npm.ps1 sous PowerShell)
Set-Alias npm npm.cmd -Scope Global -Force
Set-Alias npx npx.cmd -Scope Global -Force

# --- Backend setup ---
if (-not $SkipBackend) {
    $be = Join-Path (Get-Location) "backend"
    if (-not (Test-Path $be)) { throw "Missing folder: $be" }
    Push-Location $be
    try {
        Info "[backend] creating venv"
        python -m venv .venv
        .\.venv\Scripts\Activate.ps1

        Info "[backend] upgrading pip"
        python -m pip install -U pip

        if (Test-Path "./requirements.txt") {
            Info "[backend] pip install -r requirements.txt"
            pip install -r requirements.txt
        }
        if (Test-Path "./requirements-dev.txt") {
            Info "[backend] pip install -r requirements-dev.txt"
            pip install -r requirements-dev.txt
        }

        if (Test-Path "./.env.example" -and -not (Test-Path "./.env")) {
            Info "[backend] copying .env.example -> .env"
            Copy-Item "./.env.example" "./.env"
        }

        if (Test-Path "./alembic.ini") {
            Info "[backend] alembic upgrade head"
            alembic upgrade head
        } else {
            Info "[backend] no alembic.ini, skipping migrations"
        }
    } finally {
        Pop-Location
    }
} else {
    Info "[backend] skipped"
}

# --- Frontend setup ---
if (-not $SkipFrontend) {
    $fe = Join-Path (Get-Location) "frontend"
    if (-not (Test-Path $fe)) { throw "Missing folder: $fe" }
    Push-Location $fe
    try {
        Info "[frontend] npm ci"
        npm ci
        Info "[frontend] npm run build"
        npm run build
    } finally {
        Pop-Location
    }
} else {
    Info "[frontend] skipped"
}

Info "OK init_repo done."
Info "Next:"
Info " - Backend dev:   cd backend; ..venv\Scripts\Activate.ps1; uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
Info " - Frontend dev:  cd frontend; npm run dev"
Info " - Or staging via Docker: docker compose -f deploy/staging/compose.yaml up --build -d"
