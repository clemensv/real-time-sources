. (Join-Path $PSScriptRoot "..\..\tools\require-xrcg.ps1")
Assert-XrcgVersion

# Clean the output directory so stale generated files (e.g. data classes for
# event types that were removed from the manifest) do not leak across regens.
$amqpOut = Join-Path $PSScriptRoot "aisstream_amqp_producer"
if (Test-Path $amqpOut) { Remove-Item -Path $amqpOut -Recurse -Force }

xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\aisstream.xreg.json `
    --endpoint IO.AISstream.Amqp `
    --projectname aisstream_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output aisstream_amqp_producer
