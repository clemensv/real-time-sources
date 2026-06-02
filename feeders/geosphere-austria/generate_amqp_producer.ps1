$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\..\tools\require-xrcg.ps1"
xrcg generate --style amqpproducer --language py --definitions "$scriptDir\xreg\geosphere-austria.xreg.json" --endpoint at.geosphere.tawes.Amqp --projectname geosphere_austria_amqp_producer --template-args azure_cbs_target=servicebus --output "$scriptDir\geosphere_austria_amqp_producer"
