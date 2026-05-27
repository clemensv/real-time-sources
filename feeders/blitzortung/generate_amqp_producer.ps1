. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\blitzortung.xreg.json `
    --endpoint Blitzortung.Lightning.Amqp `
    --projectname blitzortung_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output blitzortung_amqp_producer
