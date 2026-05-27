$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\xreg\carbon_intensity.xreg.json"
$kqlFile = Join-Path $scriptDir "carbon_intensity.kql"
$generatorScript = Join-Path $scriptDir "..\..\tools\generate-kql-from-xreg.ps1"

& $generatorScript -XregPath $inputFile -OutputPath $kqlFile
