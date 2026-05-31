$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\xreg\tfl-road-traffic.xreg.json"
$kqlFile = Join-Path $scriptDir "tfl-road-traffic.kql"
$generatorScript = Join-Path $scriptDir "..\..\..\tools\generate-kql-from-xreg.ps1"

& $generatorScript -XregPath $inputFile -OutputPath $kqlFile -Qualified -Namespace "uk.gov.tfl.road"
