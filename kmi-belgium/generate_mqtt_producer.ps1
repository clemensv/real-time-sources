$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\tools\require-xrcg.ps1"
xrcg generate --style mqttclient --language py --definitions "$scriptDir\xreg\kmi_belgium.xreg.json" --endpoint BE.Gov.KMI.Weather.Mqtt --projectname kmi_belgium_mqtt_producer --output "$scriptDir\kmi_belgium_mqtt_producer"
