$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\xreg\nina_bbk.xreg.json"
$kqlFile = Join-Path $scriptDir "nina_bbk.kql"
$generatorScript = Join-Path $scriptDir "..\..\tools\generate-kql-from-xreg.ps1"

& $generatorScript -XregPath $inputFile -OutputPath $kqlFile
