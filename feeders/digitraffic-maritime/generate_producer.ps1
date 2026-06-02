# Generate the Digitraffic Maritime data producer using xrcg

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = $scriptDir
$xregFile = Join-Path $projectRoot "xreg\digitraffic_maritime.xreg.json"
$outputDir = Join-Path $projectRoot "digitraffic_maritime_producer"
$mqttOutputDir = Join-Path $projectRoot "digitraffic_maritime_mqtt_producer"
$amqpOutputDir = Join-Path $projectRoot "digitraffic_maritime_amqp_producer"

Write-Host "Generating Digitraffic Maritime producer from xRegistry definitions..." -ForegroundColor Cyan
Write-Host "  xRegistry file: $xregFile" -ForegroundColor Gray
Write-Host "  Output directory: $outputDir" -ForegroundColor Gray

# Ensure the output directory exists
if (Test-Path $outputDir) {
    Write-Host "  Cleaning existing output directory..." -ForegroundColor Yellow
    Remove-Item -Path $outputDir -Recurse -Force
}
if (Test-Path $mqttOutputDir) {
    Write-Host "  Cleaning existing MQTT output directory..." -ForegroundColor Yellow
    Remove-Item -Path $mqttOutputDir -Recurse -Force
}
if (Test-Path $amqpOutputDir) {
    Write-Host "  Cleaning existing AMQP output directory..." -ForegroundColor Yellow
    Remove-Item -Path $amqpOutputDir -Recurse -Force
}

# Generate the Kafka producer code
Write-Host "  Generating Kafka producer code..." -ForegroundColor Cyan
xrcg generate --style kafkaproducer --language py --projectname digitraffic-maritime-producer --definitions $xregFile --output $outputDir
xrcg generate --style mqttclient --language py --definitions $xregFile --endpoint fi.digitraffic.marine.Mqtt --projectname digitraffic_maritime_mqtt_producer --output $mqttOutputDir
xrcg generate --style amqpproducer --language py --definitions $xregFile --endpoint fi.digitraffic.marine.Amqp --projectname digitraffic_maritime_amqp_producer --template-args azure_cbs_target=servicebus --output $amqpOutputDir

if ($LASTEXITCODE -eq 0) {
    Write-Host "Producer generation completed successfully" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Review the generated code in: $outputDir" -ForegroundColor Gray
    Write-Host "  2. Install dependencies: poetry install" -ForegroundColor Gray
    Write-Host "  3. Run the producer: poetry run python -m digitraffic_maritime" -ForegroundColor Gray
} else {
    Write-Host "Producer generation failed with exit code: $LASTEXITCODE" -ForegroundColor Red
}
