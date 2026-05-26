# The checked-in xreg manifest is authoritative. Regenerate all transport producers from it.

. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate --style kafkaproducer --language py --definitions xreg\bfs_odl.xreg.json --endpoint de.bfs.odl.Kafka --projectname bfs_odl_producer --output bfs_odl_producer
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
xrcg generate --style mqttclient --language py --definitions xreg\bfs_odl.xreg.json --endpoint de.bfs.odl.Mqtt --projectname bfs_odl_mqtt_producer --output bfs_odl_mqtt_producer
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
xrcg generate --style amqpproducer --language py --definitions xreg\bfs_odl.xreg.json --endpoint de.bfs.odl.Amqp --projectname bfs_odl_amqp_producer --template-args azure_cbs_target=servicebus --output bfs_odl_amqp_producer
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
