$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\..\tools\require-xrcg.ps1')
Assert-XrcgVersion
$xregFile = Join-Path $PSScriptRoot 'xreg\datex2.xreg.json'
xrcg generate --style kafkaproducer --language py --definitions $xregFile --projectname datex2_producer --output (Join-Path $PSScriptRoot 'datex2_producer')
xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint org.datex2.Mqtt --projectname datex2_mqtt_producer --output (Join-Path $PSScriptRoot 'datex2_mqtt_producer')
xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint org.datex2.Amqp --projectname datex2_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $PSScriptRoot 'datex2_amqp_producer')
Convert-GeneratedPyprojects
