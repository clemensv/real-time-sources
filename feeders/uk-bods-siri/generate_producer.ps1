. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style kafkaproducer `
    --language py `
    --definitions xreg\uk-bods-siri.xreg.json `
    --endpoint uk.gov.dft.bods.Kafka `
    --projectname uk_bods_siri_producer `
    --output uk_bods_siri_producer

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\uk-bods-siri.xreg.json `
    --endpoint uk.gov.dft.bods.Mqtt `
    --projectname uk_bods_siri_mqtt_producer `
    --output uk_bods_siri_mqtt_producer

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\uk-bods-siri.xreg.json `
    --endpoint uk.gov.dft.bods.Amqp `
    --projectname uk_bods_siri_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output uk_bods_siri_amqp_producer
