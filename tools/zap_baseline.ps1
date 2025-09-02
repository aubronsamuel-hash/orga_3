Param(
    [Parameter(Mandatory=$true)][string]$Target,
    [string]$Out = "zap_report.html"
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
Write-Host "[INFO] Lancement ZAP baseline sur $Target"
docker run --rm -v ${PWD}:/zap/wrk ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t $Target -x zap_report.xml -w zap_report.md -r $Out
if (!(Test-Path $Out)) { Write-Error "Rapport ZAP manquant" ; exit 4 }
Write-Host "[OK] Rapport genere: $Out"
exit 0
