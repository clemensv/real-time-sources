. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\bfs_odl.xreg.json `
    --endpoint de.bfs.odl.Amqp `
    --projectname bfs_odl_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output bfs_odl_amqp_producer
