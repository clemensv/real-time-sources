$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\tools\require-xrcg.ps1')
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir 'xreg\autobahn.xreg.json'

xrcg generate --style kafkaproducer --language py --definitions $xregFile --endpoint 'DE.Autobahn.Kafka' --projectname autobahn_producer --output (Join-Path $scriptDir 'autobahn_producer')

xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint 'DE.Autobahn.Mqtt' --projectname autobahn_mqtt_producer --output (Join-Path $scriptDir 'autobahn_mqtt_producer')

xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint 'DE.Amqp' --projectname autobahn_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir 'autobahn_amqp_producer')
