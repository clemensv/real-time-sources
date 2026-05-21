# The checked-in xreg manifest is authoritative. Regenerate the client from it.

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
Remove-Item -Recurse -Force (Join-Path $PSScriptRoot "jma_bosai_warning_producer") -ErrorAction SilentlyContinue
xrcg generate --style kafkaproducer --language py --definitions xreg\jma-bosai-warning.xreg.json --projectname jma_bosai_warning_producer --output jma_bosai_warning_producer
