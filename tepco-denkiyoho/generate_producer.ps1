# The checked-in xreg manifest is authoritative. Regenerate the client from it.

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\tepco-denkiyoho.xreg.json --projectname tepco_denkiyoho_producer --output tepco_denkiyoho_producer
