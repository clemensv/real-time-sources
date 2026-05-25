$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\tools\require-xrcg.ps1"
xrcg generate --style mqttclient --language py --definitions "$scriptDir\xreg\smhi_weather.xreg.json" --endpoint SE.Gov.SMHI.Weather.Mqtt --projectname smhi_weather_mqtt_producer --output "$scriptDir\smhi_weather_mqtt_producer"
