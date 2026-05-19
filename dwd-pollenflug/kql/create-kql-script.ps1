$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\xreg\dwd_pollenflug.xreg.json"
$kqlFile = Join-Path $scriptDir "dwd_pollenflug.kql"
$generatorScript = Join-Path $scriptDir "..\..\tools\generate-kql-from-xreg.ps1"

& $generatorScript -XregPath $inputFile -OutputPath $kqlFile -Qualified -Namespace DE.DWD.Pollenflug
