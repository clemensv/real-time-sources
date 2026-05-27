. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate --style kafkaproducer --language py --definitions xreg\irceline_belgium.xreg.json --projectname irceline_belgium_producer --output irceline_belgium_producer

xrcg generate --style mqttclient --language py --definitions xreg\irceline_belgium.xreg.json --endpoint be.irceline.Mqtt --projectname irceline_belgium_mqtt_producer --output irceline_belgium_mqtt_producer

xrcg generate --style amqpproducer --language py --definitions xreg\irceline_belgium.xreg.json --endpoint be.irceline.Amqp --projectname irceline_belgium_amqp_producer --template-args azure_cbs_target=servicebus --output irceline_belgium_amqp_producer
