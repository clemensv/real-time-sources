# Regenerate the MQTT producer (mqttclient style) from the authoritative xreg manifest.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\ptwc-tsunami.xreg.json `
    --endpoint PTWC.Bulletins.Mqtt `
    --projectname ptwc_tsunami_mqtt_producer `
    --output ptwc_tsunami_mqtt_producer
