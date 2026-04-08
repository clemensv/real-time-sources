# The checked-in xreg manifest is authoritative. Regenerate the client from it.

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\luchtmeetnet_nl.xreg.json --projectname luchtmeetnet_nl_producer --output luchtmeetnet_nl_producer
