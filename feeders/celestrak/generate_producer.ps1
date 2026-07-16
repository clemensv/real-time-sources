# The checked-in xreg manifest is authoritative. Regenerate all three producers
# from it: one per transport endpoint (Kafka, MQTT and AMQP). Each pass uses
# --endpoint to scope generation to a single endpoint and its derived
# messagegroup; the shared base messagegroup is pulled in transitively via
# basemessageuri resolution.

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style kafkaproducer `
    --language py `
    --definitions xreg\celestrak.xreg.json `
    --endpoint org.celestrak.Kafka `
    --projectname celestrak_producer `
    --output celestrak_producer

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\celestrak.xreg.json `
    --endpoint org.celestrak.Mqtt `
    --projectname celestrak_mqtt_producer `
    --output celestrak_mqtt_producer

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\celestrak.xreg.json `
    --endpoint org.celestrak.Amqp `
    --projectname celestrak_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output celestrak_amqp_producer

Convert-GeneratedPyprojects
