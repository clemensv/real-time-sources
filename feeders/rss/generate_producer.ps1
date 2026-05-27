. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion

xrcg generate --style kafkaproducer --language py --definitions xreg\feeds.xreg.json --projectname rssbridge_producer --output rssbridge_producer --template-args use_avro=True use_json=True