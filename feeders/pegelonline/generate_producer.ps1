# The checked-in xreg manifest is authoritative. Regenerate both producers
# from it: one per transport endpoint (Kafka and MQTT). Each pass uses
# --endpoint to scope generation to a single endpoint and its derived
# messagegroup; the shared base messagegroup is pulled in transitively via
# basemessageurl resolution.

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style kafkaproducer `
    --language py `
    --definitions xreg\pegelonline.xreg.json `
    --endpoint de.wsv.pegelonline.Kafka `
    --projectname pegelonline_producer `
    --output pegelonline_producer

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\pegelonline.xreg.json `
    --endpoint de.wsv.pegelonline.Mqtt `
    --projectname pegelonline_mqtt_producer `
    --output pegelonline_mqtt_producer

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\pegelonline.xreg.json `
    --endpoint de.wsv.pegelonline.Amqp `
    --projectname pegelonline_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output pegelonline_amqp_producer

Convert-GeneratedPyprojects
