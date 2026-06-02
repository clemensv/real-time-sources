$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\..\tools\require-xrcg.ps1"
xrcg generate --style amqpproducer --language py --definitions "$scriptDir\xreg\aviationweather.xreg.json" --endpoint gov.noaa.aviationweather.Amqp --projectname aviationweather_amqp_producer --template-args azure_cbs_target=servicebus --output "$scriptDir\aviationweather_amqp_producer"
