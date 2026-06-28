$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\xreg\ndw-road-traffic.xreg.json"
$kqlFile = Join-Path $scriptDir "ndw-road-traffic.kql"
$generatorScript = Join-Path $scriptDir "..\..\..\tools\generate-kql-from-xreg.ps1"
& $generatorScript -XregPath $inputFile -OutputPath $kqlFile

