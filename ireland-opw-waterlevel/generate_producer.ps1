# The checked-in xreg manifest is authoritative. Regenerate the client from it.

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\ireland_opw_waterlevel.xreg.json --projectname ireland_opw_waterlevel_producer --output ireland_opw_waterlevel_producer
