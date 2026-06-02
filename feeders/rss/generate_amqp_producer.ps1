. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\feeds.xreg.json `
    --endpoint Microsoft.OpenData.RssFeeds.Amqp `
    --projectname rssbridge_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output rssbridge_amqp_producer
