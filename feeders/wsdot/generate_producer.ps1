$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\..\tools\require-xrcg.ps1')
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir 'xreg\wsdot.xreg.json'

# NOTE: do NOT pass --endpoint here. Scoping the kafka generation to a single
# endpoint (e.g. us.wa.wsdot.traffic.Kafka) only emits the data classes reachable
# from that one endpoint, leaving the other families' data classes stale on disk
# and making generation non-reproducible. The runtime imports data classes for
# every family from wsdot_producer_data, so all messagegroups must be generated.
xrcg generate --style kafkaproducer --language py --definitions $xregFile --projectname wsdot_producer --output (Join-Path $scriptDir 'wsdot_producer')

xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint 'us.wa.wsdot.Mqtt' --projectname wsdot_mqtt_producer --output (Join-Path $scriptDir 'wsdot_mqtt_producer')

xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint 'us.wa.wsdot.Amqp' --projectname wsdot_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir 'wsdot_amqp_producer')

Convert-GeneratedPyprojects
