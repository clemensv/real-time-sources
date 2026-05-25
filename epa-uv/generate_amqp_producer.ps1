# Regenerate the AMQP 1.0 producer (amqpproducer style) from the authoritative xreg manifest.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\epa_uv.xreg.json `
    --endpoint US.EPA.UVIndex.Amqp `
    --projectname epa_uv_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output epa_uv_amqp_producer
