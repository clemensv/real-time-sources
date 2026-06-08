$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\..\tools\require-xrcg.ps1')
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir 'xreg\nextbus.xreg.json'

xrcg generate --style kafkaproducer --language py --definitions $xregFile --endpoint 'nextbus.Kafka' --projectname nextbus_producer --output (Join-Path $scriptDir 'nextbus_producer')

xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint 'nextbus.Mqtt' --projectname nextbus_mqtt_producer --output (Join-Path $scriptDir 'nextbus_mqtt_producer')

xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint 'nextbus.Amqp' --projectname nextbus_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir 'nextbus_amqp_producer')

Convert-GeneratedPyprojects
