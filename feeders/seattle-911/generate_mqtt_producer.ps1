# Regenerate the MQTT producer (mqttclient style) from the authoritative xreg manifest.
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\seattle-911.xreg.json `
    --endpoint US.WA.Seattle.Fire911.Mqtt `
    --projectname seattle_911_mqtt_producer `
    --output seattle_911_mqtt_producer
