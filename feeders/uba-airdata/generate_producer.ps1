. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate --style kafkaproducer --language py --definitions xreg\uba_airdata.xreg.json --projectname uba_airdata_producer --output uba_airdata_producer

xrcg generate --style mqttclient --language py --definitions xreg\uba_airdata.xreg.json --endpoint de.uba.airdata.Mqtt --projectname uba_airdata_mqtt_producer --output uba_airdata_mqtt_producer

xrcg generate --style amqpproducer --language py --definitions xreg\uba_airdata.xreg.json --endpoint de.uba.airdata.Amqp --projectname uba_airdata_amqp_producer --template-args azure_cbs_target=servicebus --output uba_airdata_amqp_producer
