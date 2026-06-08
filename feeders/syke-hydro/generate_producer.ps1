$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir "xreg\syke_hydro.xreg.json"

Write-Host "Generating syke-hydro producers from xRegistry definitions..." -ForegroundColor Cyan

$outputDir = Join-Path $scriptDir "syke_hydro_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style kafkaproducer --language py --projectname syke_hydro_producer --definitions $xregFile --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$outputDir = Join-Path $scriptDir "syke_hydro_mqtt_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style mqttclient --language py --projectname syke_hydro_mqtt_producer --definitions $xregFile --endpoint FI.SYKE.Hydrology.Mqtt --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$outputDir = Join-Path $scriptDir "syke_hydro_amqp_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style amqpproducer --language py --projectname syke_hydro_amqp_producer --definitions $xregFile --endpoint FI.SYKE.Hydrology.Amqp --template-args azure_cbs_target=servicebus --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Producer generation completed successfully" -ForegroundColor Green

Convert-GeneratedPyprojects
