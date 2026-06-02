. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\jma-bosai-quake.xreg.json `
    --endpoint JP.JMA.Quake.Amqp `
    --projectname jma_bosai_quake_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output jma_bosai_quake_amqp_producer
