$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\..\tools\require-xrcg.ps1"
xrcg generate --style amqpproducer --language py --definitions "$scriptDir\xreg\smhi-weather.xreg.json" --endpoint SE.Gov.SMHI.Weather.Amqp --projectname smhi_weather_amqp_producer --template-args azure_cbs_target=servicebus --output "$scriptDir\smhi_weather_amqp_producer"
