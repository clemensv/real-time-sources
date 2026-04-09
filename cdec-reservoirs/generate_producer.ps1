# The checked-in xreg manifest is authoritative. Regenerate the client from it.

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\cdec_reservoirs.xreg.json --projectname cdec_reservoirs_producer --output cdec_reservoirs_producer
