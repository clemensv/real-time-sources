# The checked-in xreg manifest is authoritative. Regenerate the client from it.

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\jma-bosai-amedas.xreg.json --projectname jma_bosai_amedas_producer --output jma_bosai_amedas_producer
