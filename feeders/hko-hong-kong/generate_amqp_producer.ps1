$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\..\tools\require-xrcg.ps1"
xrcg generate --style amqpproducer --language py --definitions "$scriptDir\xreg\hko_hong_kong.xreg.json" --endpoint HK.Gov.HKO.Weather.Amqp --projectname hko_hong_kong_amqp_producer --template-args azure_cbs_target=servicebus --output "$scriptDir\hko_hong_kong_amqp_producer"
