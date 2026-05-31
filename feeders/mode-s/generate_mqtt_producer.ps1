# Regenerate the Mode-S MQTT producer from the authoritative xreg manifest.
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\mode-s.xreg.json `
    --endpoint Mode_S.Mqtt `
    --projectname mode_s_mqtt_producer `
    --output mode_s_mqtt_producer
