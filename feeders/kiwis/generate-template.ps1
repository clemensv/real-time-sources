$ErrorActionPreference = 'Stop'
$root = Resolve-Path (Join-Path $PSScriptRoot '..\..')
python (Join-Path $root 'tools\generate-arm-templates.py') --repo-root $root --catalog (Join-Path $PSScriptRoot 'fleet-catalog.json') --filter kiwis
