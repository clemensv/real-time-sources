# Regenerate the NWS Alerts MQTT producer from the authoritative xreg manifest.
$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path (Join-Path $scriptDir "xreg") "nws-alerts.xreg.json"
$outputDir = Join-Path $scriptDir "nws_alerts_mqtt_producer"

Write-Host "Generating NWS Alerts MQTT producer from $xregFile"

if (-not (Test-Path $xregFile)) {
    throw "xRegistry file not found: $xregFile"
}

if (Test-Path $outputDir) {
    Remove-Item -Path $outputDir -Recurse -Force
}

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions $xregFile `
    --endpoint NWS.Alerts.Mqtt `
    --projectname nws_alerts_mqtt_producer `
    --output $outputDir

if ($LASTEXITCODE -ne 0) {
    throw "MQTT producer generation failed"
}

Write-Host "NWS Alerts MQTT producer generated at $outputDir" -ForegroundColor Green
