. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\king_county_marine.xreg.json `
    --endpoint US.WA.KingCounty.Marine.Amqp `
    --projectname king_county_marine_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output king_county_marine_amqp_producer
