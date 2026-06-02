# Regenerate the MQTT producer (mqttclient style) from the authoritative xreg manifest.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\jma-bosai-warning.xreg.json `
    --endpoint JP.JMA.Warning.Mqtt `
    --projectname jma_bosai_warning_mqtt_producer `
    --output jma_bosai_warning_mqtt_producer
