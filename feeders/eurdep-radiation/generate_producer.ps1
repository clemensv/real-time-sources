# The checked-in xreg manifest is authoritative. Regenerate all transport producers from it.
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\eurdep_radiation.xreg.json --endpoint eu.jrc.eurdep.Kafka --projectname eurdep_radiation_producer --output eurdep_radiation_producer
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
xrcg generate --style mqttclient --language py --definitions xreg\eurdep_radiation.xreg.json --endpoint eu.jrc.eurdep.Mqtt --projectname eurdep_radiation_mqtt_producer --output eurdep_radiation_mqtt_producer
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
xrcg generate --style amqpproducer --language py --definitions xreg\eurdep_radiation.xreg.json --endpoint eu.jrc.eurdep.Amqp --projectname eurdep_radiation_amqp_producer --template-args azure_cbs_target=servicebus --output eurdep_radiation_amqp_producer
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Convert-GeneratedPyprojects
