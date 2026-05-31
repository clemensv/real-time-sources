. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\usgs-earthquakes.xreg.json `
    --endpoint USGS.Earthquakes.Amqp `
    --projectname usgs_earthquakes_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output usgs_earthquakes_amqp_producer
