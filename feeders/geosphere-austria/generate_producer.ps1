. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\geosphere-austria.xreg.json --projectname geosphere_austria_producer --output geosphere_austria_producer

& (Join-Path $PSScriptRoot "generate_mqtt_producer.ps1")
& (Join-Path $PSScriptRoot "generate_amqp_producer.ps1")
