$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\xreg\pegelonline.xreg.json"
$kqlFile = Join-Path $scriptDir "pegelonline.kql"
$generatorScript = Join-Path $scriptDir "..\..\tools\generate-kql-from-xreg.ps1"

& $generatorScript -XregPath $inputFile -OutputPath $kqlFile
