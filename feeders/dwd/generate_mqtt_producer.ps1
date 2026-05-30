$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\..\tools\require-xrcg.ps1"
xrcg generate --style mqttclient --language py --definitions "$scriptDir\xreg\dwd.xreg.json" --endpoint DE.DWD.CDC.Mqtt --projectname dwd_mqtt_producer --output "$scriptDir\dwd_mqtt_producer"
