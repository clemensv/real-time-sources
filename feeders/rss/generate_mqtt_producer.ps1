# Regenerate the MQTT bridge support from the authoritative xreg manifest.
# RSS currently uses a small handwritten MQTT publisher because the existing
# JsonStructure uses nested {"type":{"$ref":...}} references that xrcg 0.10.6
# cannot regenerate without changing the established Kafka data package shape.
. (Join-Path $PSScriptRoot "..\tools\require-xrcg.ps1")
Assert-XrcgVersion
xrcg validate --definitions xreg\feeds.xreg.json
