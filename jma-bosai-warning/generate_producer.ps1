# The checked-in xreg manifest is authoritative. Regenerate all transport producers from it.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate --style kafkaproducer --language py --definitions xreg\jma-bosai-warning.xreg.json --projectname jma_bosai_warning_producer --output jma_bosai_warning_producer
xrcg generate --style mqttclient --language py --definitions xreg\jma-bosai-warning.xreg.json --endpoint JP.JMA.Warning.Mqtt --projectname jma_bosai_warning_mqtt_producer --output jma_bosai_warning_mqtt_producer
xrcg generate --style amqpproducer --language py --definitions xreg\jma-bosai-warning.xreg.json --endpoint JP.JMA.Warning.Amqp --projectname jma_bosai_warning_amqp_producer --template-args azure_cbs_target=servicebus --output jma_bosai_warning_amqp_producer
