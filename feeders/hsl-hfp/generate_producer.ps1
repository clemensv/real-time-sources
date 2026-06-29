# The checked-in xreg manifest is authoritative. Regenerate the four code
# artifacts from it:
#   1. the UPSTREAM subscriber data classes + topic helpers (novel approach):
#      the HSL HFP broker is described as an xRegistry MQTT consumer message
#      group, so xrcg emits the data classes and topic-template helpers the
#      bridge uses to parse the verbatim HFP firehose.
#   2-4. the downstream CloudEvents producers, one per transport (Kafka, MQTT,
#      AMQP). Each producer endpoint spans BOTH the telemetry and the reference
#      messagegroups, so a single generated producer carries every send method.
#
# Each pass uses --endpoint to scope generation to a single endpoint and its
# referenced messagegroups; shared base messages are pulled in transitively via
# basemessageuri resolution. Generated code is NEVER hand-edited -- fix the
# manifest and regenerate.

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion
Push-Location $PSScriptRoot

# 1. Upstream subscriber (novel): generated data classes + topic helpers for
#    the plain-JSON HFP firehose on mqtt.hsl.fi. The bridge drives a thin paho
#    receive loop with these helpers (see hsl_hfp_core) until xregistry/codegen
#    #487 lands the plain-message consumer dispatch.
xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\hsl-hfp.xreg.json `
    --endpoint fi.hsl.hfp.Upstream `
    --projectname hsl_hfp_upstream `
    --output hsl_hfp_upstream_producer

# 2. Downstream Kafka / Event Hubs producer (telemetry + reference). Generated
#    WITHOUT --endpoint (digitraffic-maritime pattern): xrcg walks every KAFKA
#    endpoint and emits one send method per referenced base-group message, each
#    carrying that endpoint's endpoint-level key. The four Kafka endpoints
#    (hfp + gtfs.operator/route/stop) all target the single `hsl-hfp` topic.
#
#    The whole-manifest pass is fed a producer-only *view* of the manifest
#    because xrcg's kafkaproducer sample template crashes on the plain,
#    envelope-less upstream consumer group (see tools/xreg-producer-view.py and
#    xregistry/codegen). The view strips the consumer endpoint + upstream group
#    only; producer endpoints/groups/schemas are untouched, so the generated
#    producer is identical to an upstream-free manifest.
$producerView = "xreg\_producer-view.xreg.json"
python (Join-Path $PSScriptRoot "..\..\tools\xreg-producer-view.py") "xreg\hsl-hfp.xreg.json" $producerView
try {
    xrcg generate `
        --style kafkaproducer `
        --language py `
        --definitions $producerView `
        --projectname hsl_hfp_producer `
        --output hsl_hfp_producer
}
finally {
    Remove-Item -Force (Join-Path $PSScriptRoot $producerView) -ErrorAction SilentlyContinue
}

# 3. Downstream MQTT 5 producer (telemetry mirrors the HFP topic tree;
#    reference data retained on a reference topic tree).
xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\hsl-hfp.xreg.json `
    --endpoint fi.hsl.Mqtt `
    --projectname hsl_hfp_mqtt_producer `
    --output hsl_hfp_mqtt_producer

# 4. Downstream AMQP 1.0 producer (Service Bus / Event Hubs / generic brokers).
xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\hsl-hfp.xreg.json `
    --endpoint fi.hsl.Amqp `
    --projectname hsl_hfp_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output hsl_hfp_amqp_producer

Convert-GeneratedPyprojects
Pop-Location
