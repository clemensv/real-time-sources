# Regenerate the Bluesky MQTT producer from the authoritative xreg manifest.
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\bluesky.xreg.json `
    --endpoint BlueskyFirehose.Mqtt `
    --projectname bluesky_mqtt_producer `
    --output bluesky_mqtt_producer
