. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\usgs_iv.xreg.json `
    --endpoint USGS.IV.Amqp `
    --projectname usgs_iv_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output usgs_iv_amqp_producer
