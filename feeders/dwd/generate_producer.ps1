# The checked-in xreg manifest is authoritative. Regenerate the client from it.

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\dwd.xreg.json --projectname dwd_producer --output dwd_producer

& (Join-Path $PSScriptRoot "generate_mqtt_producer.ps1")
& (Join-Path $PSScriptRoot "generate_amqp_producer.ps1")

Convert-GeneratedPyprojects
