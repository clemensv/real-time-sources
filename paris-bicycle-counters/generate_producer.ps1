$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\tools\require-xrcg.ps1')
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir 'xreg\paris_bicycle_counters.xreg.json'

xrcg generate --style kafkaproducer --language py --definitions $xregFile --endpoint 'FR.Paris.OpenData.Velo.Kafka' --projectname paris_bicycle_counters_producer --output (Join-Path $scriptDir 'paris_bicycle_counters_producer')

xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint 'FR.Paris.OpenData.Velo.Mqtt' --projectname paris_bicycle_counters_mqtt_producer --output (Join-Path $scriptDir 'paris_bicycle_counters_mqtt_producer')

xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint 'FR.Paris.OpenData.Amqp' --projectname paris_bicycle_counters_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir 'paris_bicycle_counters_amqp_producer')
