. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style kafkaproducer `
    --language py `
    --definitions xreg\siri.xreg.json `
    --endpoint org.siri.Kafka `
    --projectname siri_producer `
    --output siri_producer

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\siri.xreg.json `
    --endpoint org.siri.Mqtt `
    --projectname siri_mqtt_producer `
    --output siri_mqtt_producer

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\siri.xreg.json `
    --endpoint org.siri.Amqp `
    --projectname siri_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output siri_amqp_producer

Convert-GeneratedPyprojects
