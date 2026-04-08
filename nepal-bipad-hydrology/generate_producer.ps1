# The checked-in xreg manifest is authoritative. Regenerate the client from it.

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\nepal_bipad_hydrology.xreg.json --projectname nepal_bipad_hydrology_producer --output nepal_bipad_hydrology_producer
