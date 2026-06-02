$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\..\tools\require-xrcg.ps1')
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir 'xreg\wsdot.xreg.json'

xrcg generate --style kafkaproducer --language py --definitions $xregFile --endpoint 'us.wa.wsdot.traffic.Kafka' --projectname wsdot_producer --output (Join-Path $scriptDir 'wsdot_producer')

xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint 'us.wa.wsdot.Mqtt' --projectname wsdot_mqtt_producer --output (Join-Path $scriptDir 'wsdot_mqtt_producer')

xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint 'us.wa.wsdot.Amqp' --projectname wsdot_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir 'wsdot_amqp_producer')
