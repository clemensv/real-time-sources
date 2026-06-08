# The checked-in xreg manifest is authoritative. Regenerate all three
# transport producers from it: one xrcg pass per endpoint. Each pass uses
# --endpoint to scope generation to a single endpoint and its derived
# messagegroup; the shared base messagegroup is pulled in transitively via
# basemessageurl resolution.

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate `
    --style kafkaproducer `
    --language py `
    --definitions xreg\noaa_swpc_l1.xreg.json `
    --endpoint gov.noaa.swpc.l1.Kafka `
    --projectname noaa_swpc_l1_producer `
    --output noaa_swpc_l1_producer

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\noaa_swpc_l1.xreg.json `
    --endpoint gov.noaa.swpc.l1.Mqtt `
    --projectname noaa_swpc_l1_mqtt_producer `
    --output noaa_swpc_l1_mqtt_producer

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\noaa_swpc_l1.xreg.json `
    --endpoint gov.noaa.swpc.l1.Amqp `
    --projectname noaa_swpc_l1_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output noaa_swpc_l1_amqp_producer

Convert-GeneratedPyprojects
