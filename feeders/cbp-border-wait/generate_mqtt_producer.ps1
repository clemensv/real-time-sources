# The checked-in xreg manifest is authoritative. Regenerate the MQTT client from it.

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style mqttclient --language py --definitions xreg\cbp_border_wait.xreg.json --endpoint gov.cbp.borderwait.Mqtt --projectname cbp_border_wait_mqtt_producer --output cbp_border_wait_mqtt_producer
