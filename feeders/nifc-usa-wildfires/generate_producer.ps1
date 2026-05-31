# Generate NIFC USA Wildfires producers from xRegistry definitions
. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion
$xregFile = Join-Path $PSScriptRoot "xreg\nifc-usa-wildfires.xreg.json"
xrcg generate --style kafkaproducer --language py --projectname nifc_usa_wildfires_producer --definitions $xregFile --endpoint Gov.NIFC.Kafka --output (Join-Path $PSScriptRoot "nifc_usa_wildfires_producer")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
xrcg generate --style mqttclient --language py --projectname nifc_usa_wildfires_mqtt_producer --definitions $xregFile --endpoint Gov.NIFC.Mqtt --output (Join-Path $PSScriptRoot "nifc_usa_wildfires_mqtt_producer")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
xrcg generate --style amqpproducer --language py --projectname nifc_usa_wildfires_amqp_producer --definitions $xregFile --endpoint Gov.NIFC.Amqp --template-args azure_cbs_target=servicebus --output (Join-Path $PSScriptRoot "nifc_usa_wildfires_amqp_producer")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
