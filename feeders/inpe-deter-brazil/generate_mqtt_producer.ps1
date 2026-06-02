# Regenerate the MQTT producer (mqttclient style) from the authoritative xreg manifest.
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\inpe_deter_brazil.xreg.json `
    --endpoint BR.INPE.DETER.Mqtt `
    --projectname inpe_deter_brazil_mqtt_producer `
    --output inpe_deter_brazil_mqtt_producer
