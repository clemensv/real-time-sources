. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate --style kafkaproducer --language py --definitions xreg\sensor-community.xreg.json --projectname sensor_community_producer --output sensor_community_producer

xrcg generate --style mqttclient --language py --definitions xreg\sensor-community.xreg.json --endpoint io.sensor.community.Mqtt --projectname sensor_community_mqtt_producer --output sensor_community_mqtt_producer

xrcg generate --style amqpproducer --language py --definitions xreg\sensor-community.xreg.json --endpoint io.sensor.community.Amqp --projectname sensor_community_amqp_producer --template-args azure_cbs_target=servicebus --output sensor_community_amqp_producer
