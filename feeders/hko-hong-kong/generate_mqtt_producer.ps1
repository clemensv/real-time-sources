$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\..\tools\require-xrcg.ps1"
xrcg generate --style mqttclient --language py --definitions "$scriptDir\xreg\hko_hong_kong.xreg.json" --endpoint HK.Gov.HKO.Weather.Mqtt --projectname hko_hong_kong_mqtt_producer --output "$scriptDir\hko_hong_kong_mqtt_producer"
