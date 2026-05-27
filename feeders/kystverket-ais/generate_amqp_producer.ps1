. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\ais.xreg.json `
    --endpoint NO.Kystverket.AIS.Amqp `
    --projectname kystverket_ais_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output kystverket_ais_amqp_producer
