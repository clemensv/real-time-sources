$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir "xreg\hubeau_hydrometrie.xreg.json"

Write-Host "Generating hubeau-hydrometrie producers from xRegistry definitions..." -ForegroundColor Cyan

$outputDir = Join-Path $scriptDir "hubeau_hydrometrie_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style kafkaproducer --language py --projectname hubeau_hydrometrie_producer --definitions $xregFile --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$outputDir = Join-Path $scriptDir "hubeau_hydrometrie_mqtt_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style mqttclient --language py --projectname hubeau_hydrometrie_mqtt_producer --definitions $xregFile --endpoint FR.Gov.Eaufrance.HubEau.Hydrometrie.Mqtt --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$outputDir = Join-Path $scriptDir "hubeau_hydrometrie_amqp_producer"
if (Test-Path $outputDir) { Remove-Item -Path $outputDir -Recurse -Force }
xrcg generate --style amqpproducer --language py --projectname hubeau_hydrometrie_amqp_producer --definitions $xregFile --endpoint FR.Gov.Eaufrance.HubEau.Hydrometrie.Amqp --template-args azure_cbs_target=servicebus --output $outputDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Producer generation completed successfully" -ForegroundColor Green

Convert-GeneratedPyprojects
