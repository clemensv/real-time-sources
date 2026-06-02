$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\..\tools\require-xrcg.ps1"
xrcg generate --style amqpproducer --language py --definitions "$scriptDir\xreg\environment_canada.xreg.json" --endpoint CA.Gov.ECCC.Weather.Amqp --projectname environment_canada_amqp_producer --template-args azure_cbs_target=servicebus --output "$scriptDir\environment_canada_amqp_producer"
