param()
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
& (Join-Path $root '..\..\tools\generate-kql-from-xreg.ps1') -XregPath (Join-Path $root 'xreg\erddap.xreg.json') -OutputPath (Join-Path $PSScriptRoot 'erddap.kql') -Qualified -Namespace org.erddap
