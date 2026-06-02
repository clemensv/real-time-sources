. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate --style kafkaproducer --language py --definitions xreg\canada-aqhi.xreg.json --projectname canada_aqhi_producer --output canada_aqhi_producer

xrcg generate --style mqttclient --language py --definitions xreg\canada-aqhi.xreg.json --endpoint ca.gc.weather.aqhi.Mqtt --projectname canada_aqhi_mqtt_producer --output canada_aqhi_mqtt_producer

xrcg generate --style amqpproducer --language py --definitions xreg\canada-aqhi.xreg.json --endpoint ca.gc.weather.aqhi.Amqp --projectname canada_aqhi_amqp_producer --template-args azure_cbs_target=servicebus --output canada_aqhi_amqp_producer
