# The checked-in xreg manifest is authoritative. Regenerate the AMQP producer from it.

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\bafu_hydro.xreg.json `
    --endpoint CH.BAFU.Hydrology.Amqp `
    --projectname bafu_hydro_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output bafu_hydro_amqp_producer
