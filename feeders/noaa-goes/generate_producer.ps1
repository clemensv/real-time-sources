. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir "xreg\noaa-goes.xreg.json"
xrcg generate --style kafkaproducer --language py --definitions $xregFile --projectname noaa-goes-producer --output (Join-Path $scriptDir "noaa_goes_producer")
if ($LASTEXITCODE -ne 0) { throw "Kafka producer generation failed" }
xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint Microsoft.OpenData.US.NOAA.SWPC.GOES.Mqtt --projectname noaa_goes_mqtt_producer --output (Join-Path $scriptDir "noaa_goes_mqtt_producer")
if ($LASTEXITCODE -ne 0) { throw "MQTT producer generation failed" }
xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint Microsoft.OpenData.US.NOAA.SWPC.GOES.Amqp --projectname noaa_goes_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir "noaa_goes_amqp_producer")
if ($LASTEXITCODE -ne 0) { throw "AMQP producer generation failed" }
