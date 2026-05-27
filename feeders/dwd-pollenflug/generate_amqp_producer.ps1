$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\tools\require-xrcg.ps1"
xrcg generate --style amqpproducer --language py --definitions "$scriptDir\xreg\dwd_pollenflug.xreg.json" --endpoint DE.DWD.Pollenflug.Amqp --projectname dwd_pollenflug_amqp_producer --template-args azure_cbs_target=servicebus --output "$scriptDir\dwd_pollenflug_amqp_producer"
