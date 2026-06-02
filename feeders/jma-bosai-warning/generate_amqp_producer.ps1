. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\jma-bosai-warning.xreg.json `
    --endpoint JP.JMA.Warning.Amqp `
    --projectname jma_bosai_warning_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output jma_bosai_warning_amqp_producer
