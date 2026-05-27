$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir "xreg\usgs_nwis_wq.xreg.json"

Write-Host "Generating usgs-nwis-wq producers from xRegistry definitions..." -ForegroundColor Cyan

$outputDir = Join-Path $scriptDir "usgs_nwis_wq_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style kafkaproducer --language py --projectname usgs_nwis_wq_producer --definitions $xregFile --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$outputDir = Join-Path $scriptDir "usgs_nwis_wq_mqtt_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style mqttclient --language py --projectname usgs_nwis_wq_mqtt_producer --definitions $xregFile --endpoint USGS.WaterQuality.Mqtt --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$outputDir = Join-Path $scriptDir "usgs_nwis_wq_amqp_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style amqpproducer --language py --projectname usgs_nwis_wq_amqp_producer --definitions $xregFile --endpoint USGS.WaterQuality.Amqp --template-args azure_cbs_target=servicebus --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Producer generation completed successfully" -ForegroundColor Green
