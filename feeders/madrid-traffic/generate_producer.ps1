$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\..\tools\require-xrcg.ps1')
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir 'xreg\madrid-traffic.xreg.json'

xrcg generate --style kafkaproducer --language py --definitions $xregFile --endpoint 'es.madrid.informo.Kafka' --projectname madrid_traffic_producer --output (Join-Path $scriptDir 'madrid_traffic_producer')

xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint 'es.madrid.Mqtt' --projectname madrid_traffic_mqtt_producer --output (Join-Path $scriptDir 'madrid_traffic_mqtt_producer')

xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint 'es.madrid.Amqp' --projectname madrid_traffic_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir 'madrid_traffic_amqp_producer')
