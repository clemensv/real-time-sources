# The checked-in xreg manifest is authoritative. Regenerate the client from it.

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\bom_australia.xreg.json --projectname bom_australia_producer --output bom_australia_producer

& (Join-Path $PSScriptRoot "generate_mqtt_producer.ps1")
& (Join-Path $PSScriptRoot "generate_amqp_producer.ps1")

Convert-GeneratedPyprojects
