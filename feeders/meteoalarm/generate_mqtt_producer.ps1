# Regenerate the MQTT producer (mqttclient style) from the authoritative xreg manifest.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\meteoalarm.xreg.json `
    --endpoint Meteoalarm.Warnings.Mqtt `
    --projectname meteoalarm_mqtt_producer `
    --output meteoalarm_mqtt_producer
