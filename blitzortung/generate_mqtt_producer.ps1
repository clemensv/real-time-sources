. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\blitzortung.xreg.json `
    --endpoint Blitzortung.Lightning.Mqtt `
    --projectname blitzortung_mqtt_producer `
    --output blitzortung_mqtt_producer
