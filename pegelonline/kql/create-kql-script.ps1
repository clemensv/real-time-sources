$scriptPath = Split-Path -Parent $PSCommandPath
$jsonFiles = Get-ChildItem -Path "$scriptPath/../xreg" -Filter "*.avsc" | Select-Object -ExpandProperty FullName
$outputFile = ".schemas.avsc"

$mergedArray = @()
foreach ($file in $jsonFiles) {
    $jsonContent = Get-Content $file -Raw | ConvertFrom-Json
    $mergedArray += $jsonContent
}
$mergedArray | ConvertTo-Json -Depth 20 | Out-File $outputFile -Encoding UTF8

avrotize a2k $outputFile --emit-cloudevents-dispatch --emit-cloudevents-columns > pegelonline.kql
Remove-Item $outputFile