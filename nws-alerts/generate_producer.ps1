$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path (Join-Path $scriptDir "xreg") "nws_alerts.xreg.json"
$outputDir = Join-Path $scriptDir "nws_alerts_producer"

Write-Host "Generating NWS Alerts producer from $xregFile"

if (-not (Test-Path $xregFile)) {
    throw "xRegistry file not found: $xregFile"
}

if (Test-Path $outputDir) {
    Remove-Item -Path $outputDir -Recurse -Force
}

xrcg generate `
    --style kafkaproducer `
    --language py `
    --projectname nws-alerts-producer `
    --definitions $xregFile `
    --output $outputDir

if ($LASTEXITCODE -ne 0) {
    throw "Producer generation failed"
}


& (Join-Path $scriptDir "generate_mqtt_producer.ps1")

$amqpOutputDir = Join-Path $scriptDir "nws_alerts_amqp_producer"
if (Test-Path $amqpOutputDir) { Remove-Item -Path $amqpOutputDir -Recurse -Force }
xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions $xregFile `
    --endpoint NWS.Alerts.Amqp `
    --projectname nws_alerts_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output $amqpOutputDir
if ($LASTEXITCODE -ne 0) { throw "AMQP producer generation failed" }
