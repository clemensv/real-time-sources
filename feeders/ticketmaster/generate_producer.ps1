# Regenerate Kafka, MQTT, and AMQP producers from the source xRegistry manifest.
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir "xreg\ticketmaster.xreg.json"
foreach ($output in @("ticketmaster_producer", "ticketmaster_mqtt_producer", "ticketmaster_amqp_producer")) {
  $outputDir = Join-Path $scriptDir $output
  if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
}
xrcg generate --style kafkaproducer --language py --definitions $xregFile --projectname ticketmaster_producer --output (Join-Path $scriptDir "ticketmaster_producer")
if ($LASTEXITCODE -ne 0) { throw "Kafka producer generation failed" }
xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint Ticketmaster.Events.Mqtt --projectname ticketmaster_mqtt_producer --output (Join-Path $scriptDir "ticketmaster_mqtt_producer")
if ($LASTEXITCODE -ne 0) { throw "MQTT producer generation failed" }
xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint Ticketmaster.Events.Amqp --projectname ticketmaster_amqp_producer --template-args azure_cbs_target=servicebus --output (Join-Path $scriptDir "ticketmaster_amqp_producer")
if ($LASTEXITCODE -ne 0) { throw "AMQP producer generation failed" }

Convert-GeneratedPyprojects
