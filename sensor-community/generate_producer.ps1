. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\sensor-community.xreg.json --projectname sensor_community_producer --output sensor_community_producer
