. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\aisstream.xreg.json `
    --endpoint IO.AISstream.Mqtt `
    --projectname aisstream_mqtt_producer `
    --output aisstream_mqtt_producer
