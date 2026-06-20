$scriptDir = Split-Path -Parent $PSCommandPath
$inputFile = Join-Path $scriptDir "..\..\gbfs-bikeshare\xreg\gbfs-bikeshare.xreg.json"
$kqlFile = Join-Path $scriptDir "tokyo-docomo-bikeshare.kql"
$generatorScript = Join-Path $scriptDir "..\..\..\tools\generate-kql-from-xreg.ps1"

& $generatorScript -XregPath $inputFile -OutputPath $kqlFile -Qualified
