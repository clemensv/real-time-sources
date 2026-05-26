$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\tools\require-xrcg.ps1"
xrcg generate --style amqpproducer --language py --definitions "$scriptDir\xreg\bom_australia.xreg.json" --endpoint AU.Gov.BOM.Weather.Amqp --projectname bom_australia_amqp_producer --template-args azure_cbs_target=servicebus --output "$scriptDir\bom_australia_amqp_producer"
