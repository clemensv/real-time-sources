# The checked-in xreg manifest is authoritative. Regenerate the client from it.

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\mode-s.xreg.json --endpoint Mode_S.Kafka --projectname mode_s_producer --output mode_s_producer

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\mode-s.xreg.json `
    --endpoint Mode_S.Amqp `
    --projectname mode_s_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output mode_s_amqp_producer
