# The checked-in xreg manifest is authoritative. Regenerate all transport producers from it.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate --style kafkaproducer --language py --definitions xreg\jma-bosai-volcano.xreg.json --endpoint JP.JMA.Volcano.Kafka --projectname jma_bosai_volcano_producer --output jma_bosai_volcano_producer
xrcg generate --style mqttclient --language py --definitions xreg\jma-bosai-volcano.xreg.json --endpoint JP.JMA.Volcano.Mqtt --projectname jma_bosai_volcano_mqtt_producer --output jma_bosai_volcano_mqtt_producer
xrcg generate --style amqpproducer --language py --definitions xreg\jma-bosai-volcano.xreg.json --endpoint JP.JMA.Volcano.Amqp --projectname jma_bosai_volcano_amqp_producer --template-args azure_cbs_target=servicebus --output jma_bosai_volcano_amqp_producer

Convert-GeneratedPyprojects
