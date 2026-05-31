# Regenerate the MQTT producer (mqttclient style) from the authoritative xreg manifest.
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\usgs-geomag.xreg.json `
    --endpoint gov.usgs.geomag.Mqtt `
    --projectname usgs_geomag_mqtt_producer `
    --output usgs_geomag_mqtt_producer
