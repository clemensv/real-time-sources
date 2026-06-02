. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate --style kafkaproducer --language py --definitions xreg\fmi-finland.xreg.json --projectname fmi_finland_producer --output fmi_finland_producer

xrcg generate --style mqttclient --language py --definitions xreg\fmi-finland.xreg.json --endpoint fi.fmi.opendata.airquality.Mqtt --projectname fmi_finland_mqtt_producer --output fmi_finland_mqtt_producer

xrcg generate --style amqpproducer --language py --definitions xreg\fmi-finland.xreg.json --endpoint fi.fmi.opendata.airquality.Amqp --projectname fmi_finland_amqp_producer --template-args azure_cbs_target=servicebus --output fmi_finland_amqp_producer
