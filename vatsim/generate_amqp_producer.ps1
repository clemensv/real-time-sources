. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\vatsim.xreg.json `
    --endpoint net.vatsim.Amqp `
    --projectname vatsim_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output vatsim_amqp_producer
