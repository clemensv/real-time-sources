$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\xreg\nasa_firms.xreg.json"
$kqlFile = Join-Path $scriptDir "nasa-firms.kql"
$generatorScript = Join-Path $scriptDir "..\..\..\tools\generate-kql-from-xreg.ps1"

& $generatorScript -XregPath $inputFile -OutputPath $kqlFile -Qualified
