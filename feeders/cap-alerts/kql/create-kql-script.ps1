param()
$ErrorActionPreference = 'Stop'
$root = Resolve-Path (Join-Path $PSScriptRoot '..\..\..')
& (Join-Path $root 'tools\generate-kql-from-xreg.ps1') -XregPath (Join-Path $PSScriptRoot '..\xreg\cap-alerts.xreg.json') -OutputPath (Join-Path $PSScriptRoot 'cap-alerts.kql') -Qualified -Namespace org.oasis.cap.alerts
