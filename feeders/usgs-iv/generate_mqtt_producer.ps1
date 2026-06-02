# Regenerate the MQTT producer (mqttclient style) from the authoritative xreg manifest.
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\usgs_iv.xreg.json `
    --endpoint USGS.IV.Mqtt `
    --projectname usgs_iv_mqtt_producer `
    --output usgs_iv_mqtt_producer
