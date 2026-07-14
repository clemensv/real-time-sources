$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\..\tools\require-xrcg.ps1')
Assert-XrcgVersion

$xregFile = Join-Path $PSScriptRoot 'xreg\tfl-cycles.xreg.json'

xrcg generate `
    --style kafkaproducer `
    --language py `
    --definitions $xregFile `
    --projectname tfl_cycles_producer `
    --output (Join-Path $PSScriptRoot 'tfl_cycles_producer')

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions $xregFile `
    --endpoint UK.Gov.TfL.Cycles.Mqtt `
    --projectname tfl_cycles_mqtt_producer `
    --output (Join-Path $PSScriptRoot 'tfl_cycles_mqtt_producer')

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions $xregFile `
    --endpoint UK.Gov.TfL.Cycles.Amqp `
    --projectname tfl_cycles_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output (Join-Path $PSScriptRoot 'tfl_cycles_amqp_producer')

Convert-GeneratedPyprojects
