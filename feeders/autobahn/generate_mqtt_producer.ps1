# Regenerate the Autobahn MQTT producer from the authoritative xreg manifest.
$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$xregFile = Join-Path (Join-Path $scriptDir "xreg") "autobahn.xreg.json"
$outputDir = Join-Path $scriptDir "autobahn_mqtt_producer"

if (Test-Path $outputDir) {
    Remove-Item -Path $outputDir -Recurse -Force
}

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions $xregFile `
    --endpoint DE.Autobahn.Mqtt `
    --projectname autobahn_mqtt_producer `
    --output $outputDir

if ($LASTEXITCODE -ne 0) {
    throw "MQTT producer generation failed"
}

Write-Host "Autobahn MQTT producer generated at $outputDir" -ForegroundColor Green
