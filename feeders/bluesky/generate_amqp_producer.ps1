. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\bluesky.xreg.json `
    --endpoint BlueskyFirehose.Amqp `
    --projectname bluesky_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output bluesky_amqp_producer
