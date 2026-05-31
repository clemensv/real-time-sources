. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\kystverket-ais.xreg.json `
    --endpoint NO.Kystverket.AIS.Mqtt `
    --projectname kystverket_ais_mqtt_producer `
    --output kystverket_ais_mqtt_producer
