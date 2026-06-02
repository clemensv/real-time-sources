# The checked-in xreg manifest is authoritative. Regenerate the AMQP producer from it.

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\german_waters.xreg.json `
    --endpoint DE.Waters.Hydrology.Amqp `
    --projectname german_waters_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output german_waters_amqp_producer
