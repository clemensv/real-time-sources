$jsonFiles = @("currentmeasurement.avsc", "station.avsc")
$outputFile = "schemas.avsc"

$mergedArray = @()
foreach ($file in $jsonFiles) {
    $jsonContent = Get-Content $file -Raw | ConvertFrom-Json
    $mergedArray += $jsonContent
}
$mergedArray | ConvertTo-Json -Depth 10 | Out-File $outputFile -Encoding UTF8

avrotize a2k schemas.avsc --emit-cloudevents-dispatch --emit-cloudevents-columns > pegelonline.kql
