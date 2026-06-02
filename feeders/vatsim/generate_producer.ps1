# The checked-in xreg manifest is authoritative. Regenerate the client from it.

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\vatsim.xreg.json --projectname vatsim_producer --output vatsim_producer


xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\vatsim.xreg.json `
    --endpoint net.vatsim.Amqp `
    --projectname vatsim_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output vatsim_amqp_producer
