# The checked-in xreg manifest is authoritative. Regenerate the AMQP producer from it.

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\wallonia_issep.xreg.json `
    --endpoint be.issep.airquality.Sensors.Amqp `
    --projectname wallonia_issep_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output wallonia_issep_amqp_producer
