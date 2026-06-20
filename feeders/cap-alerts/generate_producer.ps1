$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\..\tools\require-xrcg.ps1')
Assert-XrcgVersion

$xregFile = Join-Path $PSScriptRoot 'xreg\cap-alerts.xreg.json'

xrcg generate `
    --style kafkaproducer `
    --language py `
    --definitions $xregFile `
    --projectname cap_alerts_producer `
    --output (Join-Path $PSScriptRoot 'cap_alerts_producer')

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions $xregFile `
    --endpoint org.oasis.cap.alerts.Mqtt `
    --projectname cap_alerts_mqtt_producer `
    --output (Join-Path $PSScriptRoot 'cap_alerts_mqtt_producer')

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions $xregFile `
    --endpoint org.oasis.cap.alerts.Amqp `
    --projectname cap_alerts_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output (Join-Path $PSScriptRoot 'cap_alerts_amqp_producer')

Convert-GeneratedPyprojects
