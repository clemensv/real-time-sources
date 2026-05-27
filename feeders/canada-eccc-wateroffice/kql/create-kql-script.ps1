$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\xreg\canada-eccc-wateroffice.xreg.json"
$kqlFile = Join-Path $scriptDir "canada-eccc-wateroffice.kql"
$generatorScript = Join-Path $scriptDir "..\..\tools\generate-kql-from-xreg.ps1"
& $generatorScript -XregPath $inputFile -OutputPath $kqlFile

