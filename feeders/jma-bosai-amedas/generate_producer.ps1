# The checked-in xreg manifest is authoritative. Regenerate all transport producers from it.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate --style kafkaproducer --language py --definitions xreg\jma-bosai-amedas.xreg.json --endpoint JP.JMA.Amedas.Kafka --projectname jma_bosai_amedas_producer --output jma_bosai_amedas_producer
xrcg generate --style mqttclient --language py --definitions xreg\jma-bosai-amedas.xreg.json --endpoint JP.JMA.Amedas.Mqtt --projectname jma_bosai_amedas_mqtt_producer --output jma_bosai_amedas_mqtt_producer
xrcg generate --style amqpproducer --language py --definitions xreg\jma-bosai-amedas.xreg.json --endpoint JP.JMA.Amedas.Amqp --projectname jma_bosai_amedas_amqp_producer --template-args azure_cbs_target=servicebus --output jma_bosai_amedas_amqp_producer
