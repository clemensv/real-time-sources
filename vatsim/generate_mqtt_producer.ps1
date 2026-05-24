# Regenerate the MQTT producer (mqttclient style) from the authoritative xreg manifest.
. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\vatsim.xreg.json `
    --endpoint net.vatsim.Mqtt `
    --projectname vatsim_mqtt_producer `
    --output vatsim_mqtt_producer
