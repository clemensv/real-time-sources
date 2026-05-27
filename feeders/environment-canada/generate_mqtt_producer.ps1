$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\tools\require-xrcg.ps1"
xrcg generate --style mqttclient --language py --definitions "$scriptDir\xreg\environment_canada.xreg.json" --endpoint CA.Gov.ECCC.Weather.Mqtt --projectname environment_canada_mqtt_producer --output "$scriptDir\environment_canada_mqtt_producer"
