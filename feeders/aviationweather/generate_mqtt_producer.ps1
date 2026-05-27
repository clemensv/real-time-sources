$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\tools\require-xrcg.ps1"
xrcg generate --style mqttclient --language py --definitions "$scriptDir\xreg\aviationweather.xreg.json" --endpoint gov.noaa.aviationweather.Mqtt --projectname aviationweather_mqtt_producer --output "$scriptDir\aviationweather_mqtt_producer"
