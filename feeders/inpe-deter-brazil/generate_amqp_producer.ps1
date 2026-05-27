. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\inpe_deter_brazil.xreg.json `
    --endpoint BR.INPE.DETER.Amqp `
    --projectname inpe_deter_brazil_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output inpe_deter_brazil_amqp_producer
