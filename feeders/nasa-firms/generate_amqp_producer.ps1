. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\nasa_firms.xreg.json `
    --endpoint NASA.FIRMS.Amqp `
    --projectname nasa_firms_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output nasa_firms_amqp_producer

