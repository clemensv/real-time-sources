$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\tools\require-xrcg.ps1')
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir 'xreg\gtfs.xreg.json'

xrcg generate --style kafkaproducer --language py --definitions $xregFile --endpoint 'GeneralTransitFeed.Kafka' --projectname gtfs_producer --output (Join-Path $scriptDir 'gtfs_producer')

xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint 'GeneralTransitFeedRealTime.Mqtt' --projectname gtfs_mqtt_producer --output (Join-Path $scriptDir 'gtfs_mqtt_producer')

xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint 'GeneralTransitFeedRealTime.Amqp' --projectname gtfs_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir 'gtfs_amqp_producer')
