param()
$ErrorActionPreference = 'Stop'
& (Join-Path $PSScriptRoot '..\..\..\tools\generate-kql-from-xreg.ps1') `
  -XregPath (Join-Path $PSScriptRoot '..\xreg\kiwis.xreg.json') `
  -OutputPath (Join-Path $PSScriptRoot 'kiwis.kql') `
  -Qualified `
  -Namespace 'org.kiwis'
