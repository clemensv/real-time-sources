$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\..\tools\require-xrcg.ps1')
Assert-XrcgVersion

$xregFile = Join-Path $PSScriptRoot 'xreg\gbfs-bikeshare.xreg.json'

xrcg generate `
    --style kafkaproducer `
    --language py `
    --definitions $xregFile `
    --projectname gbfs_bikeshare_producer `
    --output (Join-Path $PSScriptRoot 'gbfs_bikeshare_producer')

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions $xregFile `
    --endpoint org.gbfs.Mqtt `
    --projectname gbfs_bikeshare_mqtt_producer `
    --output (Join-Path $PSScriptRoot 'gbfs_bikeshare_mqtt_producer')

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions $xregFile `
    --endpoint org.gbfs.Amqp `
    --projectname gbfs_bikeshare_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output (Join-Path $PSScriptRoot 'gbfs_bikeshare_amqp_producer')
