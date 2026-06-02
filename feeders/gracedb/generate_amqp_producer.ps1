. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\gracedb.xreg.json `
    --endpoint org.ligo.gracedb.Amqp `
    --projectname gracedb_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output gracedb_amqp_producer
