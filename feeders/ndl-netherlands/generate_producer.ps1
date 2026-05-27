$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\tools\require-xrcg.ps1')
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir 'xreg\ndl_netherlands.xreg.json'

xrcg generate --style kafkaproducer --language py --definitions $xregFile --endpoint 'NL.NDW.Traffic.Measurements.Kafka' --projectname ndl_netherlands_producer --output (Join-Path $scriptDir 'ndl_netherlands_producer')

xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint 'NL.NDW.Traffic.Mqtt' --projectname ndl_netherlands_mqtt_producer --output (Join-Path $scriptDir 'ndl_netherlands_mqtt_producer')

xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint 'NL.NDW.Traffic.Amqp' --projectname ndl_netherlands_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir 'ndl_netherlands_amqp_producer')
