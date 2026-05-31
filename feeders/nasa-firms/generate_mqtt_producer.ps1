. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\nasa_firms.xreg.json `
    --endpoint NASA.FIRMS.Mqtt `
    --projectname nasa_firms_mqtt_producer `
    --output nasa_firms_mqtt_producer

