# Regenerate the MQTT producer (mqttclient style) from the authoritative xreg manifest.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\gdacs.xreg.json `
    --endpoint GDACS.Alerts.Mqtt `
    --projectname gdacs_mqtt_producer `
    --output gdacs_mqtt_producer
