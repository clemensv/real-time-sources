. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\aisstream.xreg.json `
    --endpoint IO.AISstream.Amqp `
    --projectname aisstream_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output aisstream_amqp_producer
