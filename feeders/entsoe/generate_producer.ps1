# Generate the ENTSO-E data producers using xrcg: one generated package per transport.

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path $scriptDir "xreg\entsoe.xreg.json"

Write-Host "Generating ENTSO-E producers from xRegistry definitions..." -ForegroundColor Cyan
Write-Host "  xRegistry file: $xregFile" -ForegroundColor Gray

$outputs = @("entsoe_producer", "entsoe_mqtt_producer", "entsoe_amqp_producer")
foreach ($output in $outputs) {
    $outputDir = Join-Path $scriptDir $output
    if (Test-Path $outputDir) {
        Write-Host "  Cleaning existing output directory: $output" -ForegroundColor Yellow
        Remove-Item -Path $outputDir -Recurse -Force
    }
}

Write-Host "  Generating Kafka producer code..." -ForegroundColor Cyan
xrcg generate `
    --style kafkaproducer `
    --language py `
    --definitions $xregFile `
    --projectname entsoe_producer `
    --output (Join-Path $scriptDir "entsoe_producer")
if ($LASTEXITCODE -ne 0) { throw "Kafka producer generation failed with exit code $LASTEXITCODE" }

Write-Host "  Generating MQTT producer code..." -ForegroundColor Cyan
xrcg generate `
    --style mqttclient `
    --language py `
    --definitions $xregFile `
    --endpoint eu.entsoe.transparency.Mqtt `
    --projectname entsoe_mqtt_producer `
    --output (Join-Path $scriptDir "entsoe_mqtt_producer")
if ($LASTEXITCODE -ne 0) { throw "MQTT producer generation failed with exit code $LASTEXITCODE" }

Write-Host "  Generating AMQP producer code..." -ForegroundColor Cyan
xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions $xregFile `
    --endpoint eu.entsoe.transparency.Amqp `
    --projectname entsoe_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output (Join-Path $scriptDir "entsoe_amqp_producer")
if ($LASTEXITCODE -ne 0) { throw "AMQP producer generation failed with exit code $LASTEXITCODE" }

Write-Host "Producer generation completed successfully" -ForegroundColor Green
