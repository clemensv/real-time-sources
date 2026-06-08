. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\kmi_belgium.xreg.json --projectname kmi_belgium_producer --output kmi_belgium_producer

& (Join-Path $PSScriptRoot "generate_mqtt_producer.ps1")
& (Join-Path $PSScriptRoot "generate_amqp_producer.ps1")

Convert-GeneratedPyprojects
