. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir "xreg\singapore_nea.xreg.json"
xrcg generate --style kafkaproducer --language py --definitions $xregFile --projectname singapore_nea_producer --output (Join-Path $scriptDir "singapore_nea_producer")
if ($LASTEXITCODE -ne 0) { throw "Kafka producer generation failed" }
xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint SG.Gov.NEA.Environment.Mqtt --projectname singapore_nea_mqtt_producer --output (Join-Path $scriptDir "singapore_nea_mqtt_producer")
if ($LASTEXITCODE -ne 0) { throw "MQTT producer generation failed" }
xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint SG.Gov.NEA.Environment.Amqp --projectname singapore_nea_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir "singapore_nea_amqp_producer")
if ($LASTEXITCODE -ne 0) { throw "AMQP producer generation failed" }
