$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path (Join-Path $scriptDir "xreg") "digitraffic_road.xreg.json"
$outputDir = Join-Path $scriptDir "digitraffic_road_producer"

Write-Host "Generating Digitraffic Road Kafka producer from $xregFile"

if (-not (Test-Path $xregFile)) {
    throw "xRegistry file not found: $xregFile"
}

if (Test-Path $outputDir) {
    Remove-Item -Path $outputDir -Recurse -Force
}

xrcg generate `
    --style kafkaproducer `
    --language py `
    --projectname digitraffic-road-producer `
    --definitions $xregFile `
    --output $outputDir

if ($LASTEXITCODE -ne 0) {
    throw "Kafka producer generation failed"
}

Write-Host "Kafka producer generated successfully in $outputDir"

# --- MQTT producer ---
$mqttOutputDir = Join-Path $scriptDir "digitraffic_road_mqtt_producer"
if (Test-Path $mqttOutputDir) {
    Remove-Item -Path $mqttOutputDir -Recurse -Force
}

Write-Host "Generating Digitraffic Road MQTT producer from $xregFile"

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions $xregFile `
    --endpoint fi.digitraffic.road.Mqtt `
    --projectname digitraffic_road_mqtt_producer `
    --output $mqttOutputDir

if ($LASTEXITCODE -ne 0) {
    throw "MQTT producer generation failed"
}

Write-Host "MQTT producer generated successfully in $mqttOutputDir"

# --- AMQP producer ---
$amqpOutputDir = Join-Path $scriptDir "digitraffic_road_amqp_producer"
if (Test-Path $amqpOutputDir) {
    Remove-Item -Path $amqpOutputDir -Recurse -Force
}

Write-Host "Generating Digitraffic Road AMQP producer from $xregFile"

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions $xregFile `
    --endpoint fi.digitraffic.road.Amqp `
    --projectname digitraffic_road_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output $amqpOutputDir

if ($LASTEXITCODE -ne 0) {
    throw "AMQP producer generation failed"
}

Write-Host "AMQP producer generated successfully in $amqpOutputDir"

Convert-GeneratedPyprojects
