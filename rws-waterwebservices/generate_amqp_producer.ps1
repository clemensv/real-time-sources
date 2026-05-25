# The checked-in xreg manifest is authoritative. Regenerate the AMQP producer from it.

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\rws_waterwebservices.xreg.json `
    --endpoint NL.RWS.Waterwebservices.Amqp `
    --projectname rws_waterwebservices_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output rws_waterwebservices_amqp_producer
