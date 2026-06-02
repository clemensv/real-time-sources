# The checked-in xreg manifest is authoritative. Regenerate all producers
# from it: one per transport endpoint. The Kafka and AMQP endpoints multiplex
# the metObs, oceanObs and lightning messagegroups onto a single topic/address;
# the MQTT endpoint carries metObs + oceanObs as retained QoS-1 LKV topics
# (lightning is excluded from MQTT because per-strike events do not fit
# LKV semantics).

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style kafkaproducer `
    --language py `
    --definitions xreg\dmi.xreg.json `
    --endpoint dk.dmi.Kafka `
    --projectname dmi_producer `
    --output dmi_producer

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\dmi.xreg.json `
    --endpoint dk.dmi.Mqtt `
    --projectname dmi_mqtt_producer `
    --output dmi_mqtt_producer

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\dmi.xreg.json `
    --endpoint dk.dmi.Amqp `
    --projectname dmi_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output dmi_amqp_producer
