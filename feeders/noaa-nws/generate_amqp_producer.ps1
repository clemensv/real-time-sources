$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\tools\require-xrcg.ps1"
xrcg generate --style amqpproducer --language py --definitions "$scriptDir\xreg\noaa-nws.xreg.json" --endpoint Microsoft.OpenData.US.NOAA.NWS.Alerts.Amqp --projectname noaa_nws_amqp_producer --template-args azure_cbs_target=servicebus --output "$scriptDir\noaa_nws_amqp_producer"
