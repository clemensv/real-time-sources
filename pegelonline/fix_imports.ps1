# Fix imports in generated producer code
$producerFile = "pegelonline_producer_kafka_producer\producer.py"

# Read the file content
$content = Get-Content $producerFile -Raw

# Fix the import statements - remove hyphens from package names
$content = $content -replace 'from pegelonline-producer-data', 'from pegelonline_producer_data'
$content = $content -replace 'from pegelonline-producer-kafka-producer', 'from pegelonline_producer_kafka_producer'
$content = $content -replace 'import pegelonline-producer-data', 'import pegelonline_producer_data'
$content = $content -replace 'import pegelonline-producer-kafka-producer', 'import pegelonline_producer_kafka_producer'

# Write the fixed content back
Set-Content -Path $producerFile -Value $content

Write-Host "Fixed imports in $producerFile"

# Fix imports in data model files
$dataPath = "pegelonline_producer_data\de\wsv\pegelonline"
if (Test-Path $dataPath) {
    Get-ChildItem -Path $dataPath -Filter "*.py" -Recurse | ForEach-Object {
        $fileContent = Get-Content $_.FullName -Raw
        $fileContent = $fileContent -replace 'from pegelonline-producer-data', 'from pegelonline_producer_data'
        $fileContent = $fileContent -replace 'import pegelonline-producer-data', 'import pegelonline_producer_data'
        Set-Content -Path $_.FullName -Value $fileContent
        Write-Host "Fixed imports in $($_.Name)"
    }
}

Write-Host "All imports fixed successfully"
