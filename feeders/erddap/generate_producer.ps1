$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\..\tools\require-xrcg.ps1')
Assert-XrcgVersion
$xregFile = Join-Path $PSScriptRoot 'xreg\erddap.xreg.json'
xrcg generate `
    --style kafkaproducer `
    --language py `
    --definitions $xregFile `
    --projectname erddap_producer `
    --output (Join-Path $PSScriptRoot 'erddap_producer')
xrcg generate `
    --style mqttclient `
    --language py `
    --definitions $xregFile `
    --endpoint org.erddap.Mqtt `
    --projectname erddap_mqtt_producer `
    --output (Join-Path $PSScriptRoot 'erddap_mqtt_producer')
xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions $xregFile `
    --endpoint org.erddap.Amqp `
    --projectname erddap_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output (Join-Path $PSScriptRoot 'erddap_amqp_producer')
Convert-GeneratedPyprojects
