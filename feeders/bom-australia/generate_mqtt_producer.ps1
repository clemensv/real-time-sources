$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\..\tools\require-xrcg.ps1"
xrcg generate --style mqttclient --language py --definitions "$scriptDir\xreg\bom_australia.xreg.json" --endpoint AU.Gov.BOM.Weather.Mqtt --projectname bom_australia_mqtt_producer --output "$scriptDir\bom_australia_mqtt_producer"
