# Regenerate the AMQP 1.0 producer (amqpproducer style) from the authoritative xreg manifest.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\hongkong_epd.xreg.json `
    --endpoint HK.Gov.EPD.AQHI.Amqp `
    --projectname hongkong_epd_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output hongkong_epd_amqp_producer
