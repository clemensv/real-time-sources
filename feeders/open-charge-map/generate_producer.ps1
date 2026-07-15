$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\..\tools\require-xrcg.ps1')
Assert-XrcgVersion

$xregFile = Join-Path $PSScriptRoot 'xreg\open-charge-map.xreg.json'

xrcg generate `
    --style kafkaproducer `
    --language py `
    --definitions $xregFile `
    --projectname open_charge_map_producer `
    --output (Join-Path $PSScriptRoot 'open_charge_map_producer')

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions $xregFile `
    --endpoint IO.OpenChargeMap.Mqtt `
    --projectname open_charge_map_mqtt_producer `
    --output (Join-Path $PSScriptRoot 'open_charge_map_mqtt_producer')

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions $xregFile `
    --endpoint IO.OpenChargeMap.Amqp `
    --template-args azure_cbs_target=servicebus `
    --projectname open_charge_map_amqp_producer `
    --output (Join-Path $PSScriptRoot 'open_charge_map_amqp_producer')

Convert-GeneratedPyprojects
