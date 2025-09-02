$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $here
docker compose -f compose.yaml down
Pop-Location
exit 0
