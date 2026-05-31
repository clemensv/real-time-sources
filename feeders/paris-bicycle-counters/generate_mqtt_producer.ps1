# Regenerate the MQTT producer (mqttclient style) from the authoritative xreg manifest.
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\paris-bicycle-counters.xreg.json `
    --endpoint FR.Paris.OpenData.Velo.Mqtt `
    --projectname paris_bicycle_counters_mqtt_producer `
    --output paris_bicycle_counters_mqtt_producer
