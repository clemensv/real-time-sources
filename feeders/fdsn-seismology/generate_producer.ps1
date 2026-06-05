. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style kafkaproducer `
    --language py `
    --definitions xreg\fdsn-seismology.xreg.json `
    --endpoint org.fdsn.event.Kafka `
    --projectname fdsn_seismology_producer `
    --output fdsn_seismology_producer

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\fdsn-seismology.xreg.json `
    --endpoint org.fdsn.event.Mqtt `
    --projectname fdsn_seismology_mqtt_producer `
    --output fdsn_seismology_mqtt_producer

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\fdsn-seismology.xreg.json `
    --endpoint org.fdsn.event.Amqp `
    --projectname fdsn_seismology_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output fdsn_seismology_amqp_producer
