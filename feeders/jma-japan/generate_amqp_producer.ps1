$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\..\tools\require-xrcg.ps1"
xrcg generate --style amqpproducer --language py --definitions "$scriptDir\xreg\jma_japan.xreg.json" --endpoint jp.go.jma.WeatherBulletins.Amqp --projectname jma_japan_amqp_producer --template-args azure_cbs_target=servicebus --output "$scriptDir\jma_japan_amqp_producer"
