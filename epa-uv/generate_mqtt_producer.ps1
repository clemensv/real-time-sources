# Regenerate the MQTT producer (mqttclient style) from the authoritative xreg manifest.
. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\epa_uv.xreg.json `
    --endpoint US.EPA.UVIndex.Mqtt `
    --projectname epa_uv_mqtt_producer `
    --output epa_uv_mqtt_producer
