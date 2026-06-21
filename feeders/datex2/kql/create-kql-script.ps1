$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
& (Join-Path $root '..\..\tools\generate-kql-from-xreg.ps1') -XregPath (Join-Path $root 'xreg\datex2.xreg.json') -OutputPath (Join-Path $PSScriptRoot 'datex2.kql') -Qualified
