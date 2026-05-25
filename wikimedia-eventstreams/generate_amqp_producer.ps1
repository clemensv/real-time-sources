. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\wikimedia_eventstreams.xreg.json `
    --endpoint Wikimedia.EventStreams.Amqp `
    --projectname wikimedia_eventstreams_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output wikimedia_eventstreams_amqp_producer
