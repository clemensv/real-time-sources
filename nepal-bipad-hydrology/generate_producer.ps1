$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir "xreg\nepal_bipad_hydrology.xreg.json"

Write-Host "Generating nepal-bipad-hydrology producers from xRegistry definitions..." -ForegroundColor Cyan

$outputDir = Join-Path $scriptDir "nepal_bipad_hydrology_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style kafkaproducer --language py --projectname nepal_bipad_hydrology_producer --definitions $xregFile --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$outputDir = Join-Path $scriptDir "nepal_bipad_hydrology_mqtt_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style mqttclient --language py --projectname nepal_bipad_hydrology_mqtt_producer --definitions $xregFile --endpoint np.gov.bipad.hydrology.Mqtt --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$outputDir = Join-Path $scriptDir "nepal_bipad_hydrology_amqp_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style amqpproducer --language py --projectname nepal_bipad_hydrology_amqp_producer --definitions $xregFile --endpoint np.gov.bipad.hydrology.Amqp --template-args azure_cbs_target=servicebus --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Producer generation completed successfully" -ForegroundColor Green
