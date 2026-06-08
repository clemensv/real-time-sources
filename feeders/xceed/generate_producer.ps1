# Regenerate Kafka, MQTT, and AMQP producers from the source xRegistry manifest.
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir "xreg\xceed.xreg.json"
foreach ($output in @("xceed_producer", "xceed_mqtt_producer", "xceed_amqp_producer")) {
  $outputDir = Join-Path $scriptDir $output
  if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
}
xrcg generate --style kafkaproducer --language py --definitions $xregFile --projectname xceed_producer --output (Join-Path $scriptDir "xceed_producer")
if ($LASTEXITCODE -ne 0) { throw "Kafka producer generation failed" }
xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint xceed.Mqtt --projectname xceed_mqtt_producer --output (Join-Path $scriptDir "xceed_mqtt_producer")
if ($LASTEXITCODE -ne 0) { throw "MQTT producer generation failed" }
xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint xceed.Amqp --projectname xceed_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir "xceed_amqp_producer")
if ($LASTEXITCODE -ne 0) { throw "AMQP producer generation failed" }

Convert-GeneratedPyprojects
