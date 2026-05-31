. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir "xreg\nws-forecasts.xreg.json"
xrcg generate --style kafkaproducer --language py --definitions $xregFile --endpoint Microsoft.OpenData.US.NOAA.NWS.Forecasts.Kafka --projectname nws_forecasts_producer --output (Join-Path $scriptDir "nws_forecasts_producer")
if ($LASTEXITCODE -ne 0) { throw "Kafka producer generation failed" }
xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint Microsoft.OpenData.US.NOAA.NWS.Forecasts.Mqtt --projectname nws_forecasts_mqtt_producer --output (Join-Path $scriptDir "nws_forecasts_mqtt_producer")
if ($LASTEXITCODE -ne 0) { throw "MQTT producer generation failed" }
xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint Microsoft.OpenData.US.NOAA.NWS.Forecasts.Amqp --projectname nws_forecasts_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir "nws_forecasts_amqp_producer")
if ($LASTEXITCODE -ne 0) { throw "AMQP producer generation failed" }
