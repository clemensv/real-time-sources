. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate --style kafkaproducer --language py --definitions xreg\gios_poland.xreg.json --endpoint pl.gov.gios.airquality.Kafka --projectname gios_poland_producer --output gios_poland_producer

xrcg generate --style mqttclient --language py --definitions xreg\gios_poland.xreg.json --endpoint pl.gov.gios.airquality.Mqtt --projectname gios_poland_mqtt_producer --output gios_poland_mqtt_producer

xrcg generate --style amqpproducer --language py --definitions xreg\gios_poland.xreg.json --endpoint pl.gov.gios.airquality.Amqp --projectname gios_poland_amqp_producer --template-args azure_cbs_target=servicebus --output gios_poland_amqp_producer
