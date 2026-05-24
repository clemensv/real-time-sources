# Regenerate the MQTT producer (mqttclient style) from the authoritative xreg manifest.
. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\carbon_intensity.xreg.json `
    --endpoint uk.org.carbonintensity.Mqtt `
    --projectname carbon_intensity_mqtt_producer `
    --output carbon_intensity_mqtt_producer
