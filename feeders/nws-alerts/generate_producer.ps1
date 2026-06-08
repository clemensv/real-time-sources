$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path (Join-Path $scriptDir "xreg") "nws-alerts.xreg.json"
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

& (Join-Path $PSScriptRoot "generate_amqp_producer.ps1")

Convert-GeneratedPyprojects
