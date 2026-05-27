. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\wallonia_issep.xreg.json --projectname wallonia_issep_producer --output wallonia_issep_producer
