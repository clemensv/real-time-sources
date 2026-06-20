param()
$ErrorActionPreference = 'Stop'
$SourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& (Join-Path $SourceDir '..\..\..\tools\generate-kql-from-xreg.ps1') `
  -XregPath (Join-Path $SourceDir '..\xreg\openaq.xreg.json') `
  -OutputPath (Join-Path $SourceDir 'openaq.kql') `
  -Qualified `
  -Namespace org.openaq
