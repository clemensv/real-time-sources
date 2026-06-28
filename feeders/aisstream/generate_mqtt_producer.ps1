. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

# Clean the output directory so stale generated files (e.g. data classes for
# event types that were removed from the manifest) do not leak across regens.
$mqttOut = Join-Path $PSScriptRoot "aisstream_mqtt_producer"
if (Test-Path $mqttOut) { Remove-Item -Path $mqttOut -Recurse -Force }

xrcg generate `
    --style mqttclient `
    --language py `
    --definitions xreg\aisstream.xreg.json `
    --endpoint IO.AISstream.Mqtt `
    --projectname aisstream_mqtt_producer `
    --output aisstream_mqtt_producer
