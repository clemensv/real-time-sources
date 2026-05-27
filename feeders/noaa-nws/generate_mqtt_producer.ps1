$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\tools\require-xrcg.ps1"
xrcg generate --style mqttclient --language py --definitions "$scriptDir\xreg\noaa_nws.xreg.json" --endpoint Microsoft.OpenData.US.NOAA.NWS.Alerts.Mqtt --projectname noaa_nws_mqtt_producer --output "$scriptDir\noaa_nws_mqtt_producer"
