# Regenerate the MQTT producer (mqttclient style) from the authoritative xreg manifest.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\nina_bbk.xreg.json `
    --endpoint NINA.Warnings.Mqtt `
    --projectname nina_bbk_mqtt_producer `
    --output nina_bbk_mqtt_producer
