$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\..\tools\require-xrcg.ps1')
Assert-XrcgVersion
$xregFile = Join-Path $PSScriptRoot 'xreg\kiwis.xreg.json'
xrcg generate --style kafkaproducer --language py --definitions $xregFile --projectname kiwis_producer --output (Join-Path $PSScriptRoot 'kiwis_producer')
xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint org.kiwis.Mqtt --projectname kiwis_mqtt_producer --output (Join-Path $PSScriptRoot 'kiwis_mqtt_producer')
xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint org.kiwis.Amqp --projectname kiwis_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $PSScriptRoot 'kiwis_amqp_producer')
Convert-GeneratedPyprojects
