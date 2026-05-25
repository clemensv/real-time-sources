$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\tools\require-xrcg.ps1')
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir 'xreg\tfl_road_traffic.xreg.json'

xrcg generate --style kafkaproducer --language py --definitions $xregFile --endpoint 'uk.gov.tfl.road.corridors.Kafka' --projectname tfl_road_traffic_producer --output (Join-Path $scriptDir 'tfl_road_traffic_producer')

xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint 'uk.gov.tfl.road.Mqtt' --projectname tfl_road_traffic_mqtt_producer --output (Join-Path $scriptDir 'tfl_road_traffic_mqtt_producer')

xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint 'uk.gov.tfl.road.Amqp' --projectname tfl_road_traffic_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir 'tfl_road_traffic_amqp_producer')
