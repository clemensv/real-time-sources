. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate --style kafkaproducer --language py --definitions xreg\luchtmeetnet_nl.xreg.json --projectname luchtmeetnet_nl_producer --output luchtmeetnet_nl_producer

xrcg generate --style mqttclient --language py --definitions xreg\luchtmeetnet_nl.xreg.json --endpoint nl.rivm.luchtmeetnet.Mqtt --projectname luchtmeetnet_nl_mqtt_producer --output luchtmeetnet_nl_mqtt_producer

xrcg generate --style amqpproducer --language py --definitions xreg\luchtmeetnet_nl.xreg.json --endpoint nl.rivm.luchtmeetnet.Amqp --projectname luchtmeetnet_nl_amqp_producer --template-args azure_cbs_target=servicebus --output luchtmeetnet_nl_amqp_producer
