. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate --style kafkaproducer --language py --definitions xreg\defra_aurn.xreg.json --projectname defra_aurn_producer --output defra_aurn_producer

xrcg generate --style mqttclient --language py --definitions xreg\defra_aurn.xreg.json --endpoint uk.gov.defra.aurn.Mqtt --projectname defra_aurn_mqtt_producer --output defra_aurn_mqtt_producer

xrcg generate --style amqpproducer --language py --definitions xreg\defra_aurn.xreg.json --endpoint uk.gov.defra.aurn.Amqp --projectname defra_aurn_amqp_producer --template-args azure_cbs_target=servicebus --output defra_aurn_amqp_producer
