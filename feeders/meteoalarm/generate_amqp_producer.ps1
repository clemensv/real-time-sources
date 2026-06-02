# Regenerate the AMQP 1.0 producer (amqpproducer style) from the authoritative xreg manifest.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\meteoalarm.xreg.json `
    --endpoint Meteoalarm.Warnings.Amqp `
    --projectname meteoalarm_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output meteoalarm_amqp_producer
