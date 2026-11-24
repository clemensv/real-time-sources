# The checked-in xreg manifest is authoritative. Regenerate all producers
# from it: one per transport endpoint (Kafka, MQTT and AMQP). Each pass uses
# --endpoint to scope generation to a single endpoint and its derived
# messagegroup; the shared base messagegroup is pulled in transitively via
# basemessageurl resolution.

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion -RequiredVersion '0.11.2.dev6'

xrcg generate `
    --style kafkaproducer `
    --language py `
    --definitions xreg\pegelonline.xreg.json `
    --endpoint de.wsv.pegelonline.Kafka `
    --projectname pegelonline_producer `
    --output pegelonline_producer
if ($LASTEXITCODE -ne 0) { throw "Kafka producer generation failed" }

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\pegelonline.xreg.json `
    --endpoint de.wsv.pegelonline.Mqtt `
    --projectname pegelonline_mqtt_producer `
    --output pegelonline_mqtt_producer
if ($LASTEXITCODE -ne 0) { throw "MQTT producer generation failed" }

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\pegelonline.xreg.json `
    --endpoint de.wsv.pegelonline.Amqp `
    --projectname pegelonline_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output pegelonline_amqp_producer
if ($LASTEXITCODE -ne 0) { throw "AMQP producer generation failed" }

$definition = Join-Path ([IO.Path]::GetTempPath()) ("pegelonline-" + [guid]::NewGuid() + ".json")
try {
    python ..\..\tools\deploy-fabric\generate_schema_set.py `
        --registry fabric\schematized\pegelonline.fabric.xreg.json `
        --messagegroup de.wsv.pegelonline.avro `
        --definition $definition `
        --python-data-output pegelonline_amqp_producer\pegelonline_amqp_producer_data `
        --python-package pegelonline_amqp_producer_data
    if ($LASTEXITCODE -ne 0) { throw "AMQP dual-encoding data generation failed" }
} finally {
    if (Test-Path $definition) { Remove-Item -LiteralPath $definition }
}

Convert-GeneratedPyprojects
