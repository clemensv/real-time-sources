$scriptPath = Split-Path -Parent $PSCommandPath
$jsonFiles = Get-ChildItem -Path "$scriptPath/gtfs-static" -Filter "*.avsc" | Select-Object -ExpandProperty FullName
$gtfsRtFiles = Get-ChildItem -Path "$scriptPath" -Filter "gtfs-rt-*.avsc" | Select-Object -ExpandProperty FullName
$jsonFiles += $gtfsRtFiles
$outputFile = ".schemas.avsc"

$mergedArray = @()
foreach ($file in $jsonFiles) {
    $jsonContent = Get-Content $file -Raw | ConvertFrom-Json
    $mergedArray += $jsonContent
}
$mergedArray | ConvertTo-Json -Depth 20 | Out-File $outputFile -Encoding UTF8

avrotize a2k $outputFile --emit-cloudevents-dispatch --emit-cloudevents-columns > gtfs.kql
Remove-Item $outputFile
