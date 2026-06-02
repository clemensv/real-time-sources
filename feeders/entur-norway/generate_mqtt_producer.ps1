# Regenerate the MQTT producer (mqttclient style) from the authoritative xreg manifest.
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\entur-norway.xreg.json `
    --endpoint no.entur.Mqtt `
    --projectname entur_norway_mqtt_producer `
    --output entur_norway_mqtt_producer
