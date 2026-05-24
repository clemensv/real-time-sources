# Regenerate the MQTT producer (mqttclient style) from the authoritative xreg manifest.
. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\eaws_albina.xreg.json `
    --endpoint org.EAWS.ALBINA.Mqtt `
    --projectname eaws_albina_mqtt_producer `
    --output eaws_albina_mqtt_producer
