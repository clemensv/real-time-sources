$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir "xreg\ireland_opw_waterlevel.xreg.json"

Write-Host "Generating ireland-opw-waterlevel producers from xRegistry definitions..." -ForegroundColor Cyan

$outputDir = Join-Path $scriptDir "ireland_opw_waterlevel_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style kafkaproducer --language py --projectname ireland_opw_waterlevel_producer --definitions $xregFile --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$outputDir = Join-Path $scriptDir "ireland_opw_waterlevel_mqtt_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style mqttclient --language py --projectname ireland_opw_waterlevel_mqtt_producer --definitions $xregFile --endpoint ie.gov.opw.waterlevel.Mqtt --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$outputDir = Join-Path $scriptDir "ireland_opw_waterlevel_amqp_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style amqpproducer --language py --projectname ireland_opw_waterlevel_amqp_producer --definitions $xregFile --endpoint ie.gov.opw.waterlevel.Amqp --template-args azure_cbs_target=servicebus --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Producer generation completed successfully" -ForegroundColor Green

Convert-GeneratedPyprojects
