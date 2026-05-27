# The checked-in xreg manifest is authoritative. Regenerate the MQTT client from it.

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style mqttclient --language py --definitions xreg\irail.xreg.json --endpoint be.irail.Mqtt --projectname irail_mqtt_producer --output irail_mqtt_producer
