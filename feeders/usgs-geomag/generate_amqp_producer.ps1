. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\usgs_geomag.xreg.json `
    --endpoint gov.usgs.geomag.Amqp `
    --projectname usgs_geomag_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output usgs_geomag_amqp_producer
