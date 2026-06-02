. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\carbon_intensity.xreg.json `
    --endpoint uk.org.carbonintensity.Amqp `
    --projectname carbon_intensity_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output carbon_intensity_amqp_producer
