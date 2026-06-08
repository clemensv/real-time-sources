. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate --style kafkaproducer --language py --definitions xreg\laqn-london.xreg.json --projectname laqn_london_producer --output laqn_london_producer

xrcg generate --style mqttclient --language py --definitions xreg\laqn-london.xreg.json --endpoint uk.kcl.laqn.Mqtt --projectname laqn_london_mqtt_producer --output laqn_london_mqtt_producer

xrcg generate --style amqpproducer --language py --definitions xreg\laqn-london.xreg.json --endpoint uk.kcl.laqn.Amqp --projectname laqn_london_amqp_producer --template-args azure_cbs_target=servicebus --output laqn_london_amqp_producer

Convert-GeneratedPyprojects
