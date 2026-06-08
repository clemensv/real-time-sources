# The checked-in xreg manifest is authoritative. Regenerate the client from it.

. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg generate --style kafkaproducer --language py --definitions xreg\smhi-weather.xreg.json --projectname smhi_weather_producer --output smhi_weather_producer

& (Join-Path $PSScriptRoot "generate_mqtt_producer.ps1")
& (Join-Path $PSScriptRoot "generate_amqp_producer.ps1")

Convert-GeneratedPyprojects
