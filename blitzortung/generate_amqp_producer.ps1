$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\tools\require-xrcg.ps1"
xrcg generate --style amqpproducer --language py --definitions "$scriptDir\xreg\blitzortung.xreg.json" --endpoint Blitzortung.Lightning.Amqp --projectname blitzortung_amqp_producer --template-args azure_cbs_target=servicebus --output "$scriptDir\blitzortung_amqp_producer"
