# The checked-in xreg manifest is authoritative. Regenerate the AMQP producer from it.

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\smhi_hydro.xreg.json `
    --endpoint SE.Gov.SMHI.Hydro.Amqp `
    --projectname smhi_hydro_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output smhi_hydro_amqp_producer
