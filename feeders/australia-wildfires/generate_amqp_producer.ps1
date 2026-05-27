. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\australia_wildfires.xreg.json `
    --endpoint AU.Gov.Emergency.Wildfires.Amqp `
    --projectname australia_wildfires_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output australia_wildfires_amqp_producer
