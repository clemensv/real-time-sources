$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\tools\require-xrcg.ps1"
xrcg generate --style mqttclient --language py --definitions "$scriptDir\xreg\blitzortung.xreg.json" --endpoint Blitzortung.Lightning.Mqtt --projectname blitzortung_mqtt_producer --output "$scriptDir\blitzortung_mqtt_producer"
