$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\..\tools\require-xrcg.ps1')
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir 'xreg\seattle-street-closures.xreg.json'

xrcg generate --style kafkaproducer --language py --definitions $xregFile --endpoint 'US.WA.Seattle.StreetClosures.Kafka' --projectname seattle_street_closures_producer --output (Join-Path $scriptDir 'seattle_street_closures_producer')

xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint 'US.WA.Seattle.Mqtt' --projectname seattle_street_closures_mqtt_producer --output (Join-Path $scriptDir 'seattle_street_closures_mqtt_producer')

xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint 'US.WA.Seattle.Amqp' --projectname seattle_street_closures_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir 'seattle_street_closures_amqp_producer')
