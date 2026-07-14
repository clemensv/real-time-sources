$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\..\tools\require-xrcg.ps1')
Assert-XrcgVersion

$xregFile = Join-Path $PSScriptRoot 'xreg\taipei-youbike.xreg.json'

xrcg generate `
    --style kafkaproducer `
    --language py `
    --definitions $xregFile `
    --projectname taipei_youbike_producer `
    --output (Join-Path $PSScriptRoot 'taipei_youbike_producer')

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions $xregFile `
    --endpoint TW.YouBike.Mqtt `
    --projectname taipei_youbike_mqtt_producer `
    --output (Join-Path $PSScriptRoot 'taipei_youbike_mqtt_producer')

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions $xregFile `
    --endpoint TW.YouBike.Amqp `
    --template-args azure_cbs_target=servicebus `
    --projectname taipei_youbike_amqp_producer `
    --output (Join-Path $PSScriptRoot 'taipei_youbike_amqp_producer')

Convert-GeneratedPyprojects
