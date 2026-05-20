# The checked-in xreg manifest is authoritative. Regenerate the client from it.

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\jma-bosai-volcano.xreg.json --projectname jma_bosai_volcano_producer --output jma_bosai_volcano_producer
