$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\..\tools\require-xrcg.ps1"
xrcg generate --style mqttclient --language py --definitions "$scriptDir\xreg\jma_japan.xreg.json" --endpoint jp.go.jma.WeatherBulletins.Mqtt --projectname jma_japan_mqtt_producer --output "$scriptDir\jma_japan_mqtt_producer"
