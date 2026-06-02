# The checked-in xreg manifest is authoritative. Regenerate the AMQP producer from it.

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\chmi_hydro.xreg.json `
    --endpoint CZ.Gov.CHMI.Hydro.Amqp `
    --projectname chmi_hydro_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output chmi_hydro_amqp_producer
