# Regenerate the MQTT producer (mqttclient style) from the authoritative xreg manifest.
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\gracedb.xreg.json `
    --endpoint org.ligo.gracedb.Mqtt `
    --projectname gracedb_mqtt_producer `
    --output gracedb_mqtt_producer
