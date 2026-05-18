$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\xreg\cdec_reservoirs.xreg.json"
$kqlFile = Join-Path $scriptDir "cdec_reservoirs.kql"
$generatorScript = Join-Path $scriptDir "..\..\tools\generate-kql-from-xreg.ps1"

& $generatorScript -XregPath $inputFile -OutputPath $kqlFile
