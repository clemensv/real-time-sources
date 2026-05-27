$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\xreg\cbp_border_wait.xreg.json"
$kqlFile = Join-Path $scriptDir "cbp_border_wait.kql"
$generatorScript = Join-Path $scriptDir "..\..\tools\generate-kql-from-xreg.ps1"

& $generatorScript -XregPath $inputFile -OutputPath $kqlFile
