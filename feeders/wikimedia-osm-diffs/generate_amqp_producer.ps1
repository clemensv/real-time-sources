. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\wikimedia_osm_diffs.xreg.json `
    --endpoint Org.OpenStreetMap.Diffs.Amqp `
    --projectname wikimedia_osm_diffs_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output wikimedia_osm_diffs_amqp_producer
