# Regenerate the MQTT producer (mqttclient style) from the authoritative xreg manifest.
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\usgs-earthquakes.xreg.json `
    --endpoint USGS.Earthquakes.Mqtt `
    --projectname usgs_earthquakes_mqtt_producer `
    --output usgs_earthquakes_mqtt_producer
