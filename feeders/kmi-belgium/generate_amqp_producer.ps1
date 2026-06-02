$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\..\..\tools\require-xrcg.ps1"
xrcg generate --style amqpproducer --language py --definitions "$scriptDir\xreg\kmi_belgium.xreg.json" --endpoint BE.Gov.KMI.Weather.Amqp --projectname kmi_belgium_amqp_producer --template-args azure_cbs_target=servicebus --output "$scriptDir\kmi_belgium_amqp_producer"
