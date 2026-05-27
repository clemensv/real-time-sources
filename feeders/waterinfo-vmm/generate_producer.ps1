$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir "xreg\waterinfo_vmm.xreg.json"

Write-Host "Generating waterinfo-vmm producers from xRegistry definitions..." -ForegroundColor Cyan

$outputDir = Join-Path $scriptDir "waterinfo_vmm_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style kafkaproducer --language py --projectname waterinfo_vmm_producer --definitions $xregFile --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$outputDir = Join-Path $scriptDir "waterinfo_vmm_mqtt_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style mqttclient --language py --projectname waterinfo_vmm_mqtt_producer --definitions $xregFile --endpoint BE.Vlaanderen.Waterinfo.VMM.Mqtt --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$outputDir = Join-Path $scriptDir "waterinfo_vmm_amqp_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style amqpproducer --language py --projectname waterinfo_vmm_amqp_producer --definitions $xregFile --endpoint BE.Vlaanderen.Waterinfo.VMM.Amqp --template-args azure_cbs_target=servicebus --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Producer generation completed successfully" -ForegroundColor Green
