$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir "xreg\uk-ea-flood-monitoring.xreg.json"

Write-Host "Generating uk-ea-flood-monitoring producers from xRegistry definitions..." -ForegroundColor Cyan

$outputDir = Join-Path $scriptDir "uk_ea_flood_monitoring_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style kafkaproducer --language py --projectname uk_ea_flood_monitoring_producer --definitions $xregFile --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$outputDir = Join-Path $scriptDir "uk_ea_flood_monitoring_mqtt_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style mqttclient --language py --projectname uk_ea_flood_monitoring_mqtt_producer --definitions $xregFile --endpoint UK.Gov.Environment.EA.FloodMonitoring.Mqtt --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$outputDir = Join-Path $scriptDir "uk_ea_flood_monitoring_amqp_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style amqpproducer --language py --projectname uk_ea_flood_monitoring_amqp_producer --definitions $xregFile --endpoint UK.Gov.Environment.EA.FloodMonitoring.Amqp --template-args azure_cbs_target=servicebus --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Producer generation completed successfully" -ForegroundColor Green

Convert-GeneratedPyprojects
