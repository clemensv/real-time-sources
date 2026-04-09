. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\geosphere-austria.xreg.json --projectname geosphere_austria_producer --output geosphere_austria_producer
