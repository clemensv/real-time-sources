$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\..\tools\require-xrcg.ps1"
xrcg generate --style mqttclient --language py --definitions "$scriptDir\xreg\dwd_pollenflug.xreg.json" --endpoint DE.DWD.Pollenflug.Mqtt --projectname dwd_pollenflug_mqtt_producer --output "$scriptDir\dwd_pollenflug_mqtt_producer"
