$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\xreg\snotel.xreg.json"
$kqlFile = Join-Path $scriptDir "snotel.kql"
$generatorScript = Join-Path $scriptDir "..\..\tools\generate-kql-from-xreg.ps1"

& $generatorScript -XregPath $inputFile -OutputPath $kqlFile -Qualified -Namespace gov.usda.nrcs.snotel
