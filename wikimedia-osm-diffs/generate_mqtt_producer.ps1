. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\wikimedia_osm_diffs.xreg.json `
    --endpoint WikimediaOsmDiffs.Mqtt `
    --projectname wikimedia_osm_diffs_mqtt_producer `
    --output wikimedia_osm_diffs_mqtt_producer
