$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\..\tools\require-xrcg.ps1')
Assert-XrcgVersion
$xregFile = Join-Path $PSScriptRoot 'xreg\openaq.xreg.json'
xrcg generate `
    --style kafkaproducer `
    --language py `
    --definitions $xregFile `
    --projectname openaq_producer `
    --output (Join-Path $PSScriptRoot 'openaq_producer')
xrcg generate `
    --style mqttclient `
    --language py `
    --definitions $xregFile `
    --endpoint org.openaq.Mqtt `
    --projectname openaq_mqtt_producer `
    --output (Join-Path $PSScriptRoot 'openaq_mqtt_producer')
xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions $xregFile `
    --endpoint org.openaq.Amqp `
    --projectname openaq_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output (Join-Path $PSScriptRoot 'openaq_amqp_producer')
Convert-GeneratedPyprojects

