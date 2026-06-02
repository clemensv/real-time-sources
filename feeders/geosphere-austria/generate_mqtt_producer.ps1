$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\..\tools\require-xrcg.ps1"
xrcg generate --style mqttclient --language py --definitions "$scriptDir\xreg\geosphere-austria.xreg.json" --endpoint at.geosphere.tawes.Mqtt --projectname geosphere_austria_mqtt_producer --output "$scriptDir\geosphere_austria_mqtt_producer"
