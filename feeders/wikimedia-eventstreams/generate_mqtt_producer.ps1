# Regenerate the Wikimedia EventStreams MQTT producer from the authoritative xreg manifest.
. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\wikimedia_eventstreams.xreg.json `
    --endpoint Wikimedia.EventStreams.Mqtt `
    --projectname wikimedia_eventstreams_mqtt_producer `
    --output wikimedia_eventstreams_mqtt_producer
