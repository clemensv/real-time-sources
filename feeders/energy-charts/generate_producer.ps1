# Regenerate Kafka, MQTT, and AMQP producers from the source xRegistry manifest.
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir "xreg\energy_charts.xreg.json"

foreach ($output in @("energy_charts_producer", "energy_charts_mqtt_producer", "energy_charts_amqp_producer")) {
  $outputDir = Join-Path $scriptDir $output
  if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
}
xrcg generate --style kafkaproducer --language py --definitions $xregFile --projectname energy_charts_producer --output (Join-Path $scriptDir "energy_charts_producer")
if ($LASTEXITCODE -ne 0) { throw "Kafka producer generation failed" }
xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint info.energy_charts.Mqtt --projectname energy_charts_mqtt_producer --output (Join-Path $scriptDir "energy_charts_mqtt_producer")
if ($LASTEXITCODE -ne 0) { throw "MQTT producer generation failed" }
xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint info.energy_charts.Amqp --projectname energy_charts_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir "energy_charts_amqp_producer")
if ($LASTEXITCODE -ne 0) { throw "AMQP producer generation failed" }
