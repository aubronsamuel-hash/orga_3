#requires -Version 7.0
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-CmdTool {
param(
[Parameter(Mandatory)]
[ValidateSet("npm","npx")]
[string]$Name
)
$candidate = "$Name.cmd"
$cmd = Get-Command $candidate -ErrorAction SilentlyContinue
if (-not $cmd) {
Write-Error "Prerequis manquants: '$candidate' introuvable dans PATH. Installez Node.js et npm. (EXIT 2)"
exit 2
}
return $cmd.Source
}

function Invoke-Npm {
[CmdletBinding()]
param(
[Parameter(ValueFromRemainingArguments=$true)]
[string[]]$Args
)
$exe = Resolve-CmdTool -Name "npm"
& $exe @Args
}

function Invoke-Npx {
[CmdletBinding()]
param(
[Parameter(ValueFromRemainingArguments=$true)]
[string[]]$Args
)
$exe = Resolve-CmdTool -Name "npx"
& $exe @Args
}

Export-ModuleMember -Function Invoke-Npm, Invoke-Npx
