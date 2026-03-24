# Fix import statements in generated producer files

Write-Host "Fixing imports in producer files..." -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$targetDir = Join-Path $scriptDir "usgs_earthquakes" "usgs_earthquakes_producer"

# Get all Python files recursively
$pythonFiles = Get-ChildItem -Path $targetDir -Filter "*.py" -Recurse

$totalFiles = 0

foreach ($file in $pythonFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    $originalContent = $content

    # Fix imports for Event class from earthquakes
    $content = $content -replace 'from usgs-earthquakes-producer_data import Event', 'from usgs_earthquakes.usgs_earthquakes_producer.usgs.earthquakes.event import Event'

    # Fix any dotted imports from data package
    $content = $content -replace 'from usgs-earthquakes-producer_data\.', 'from usgs_earthquakes.usgs_earthquakes_producer.usgs.'
    $content = $content -replace 'import usgs-earthquakes-producer_data\.', 'import usgs_earthquakes.usgs_earthquakes_producer.usgs.'

    # Fix usgs-earthquakes-producer_kafka_producer imports
    $content = $content -replace 'from usgs-earthquakes-producer_kafka_producer\.', 'from usgs_earthquakes.usgs_earthquakes_producer.'
    $content = $content -replace 'import usgs-earthquakes-producer_kafka_producer\.', 'import usgs_earthquakes.usgs_earthquakes_producer.'

    # Fix bytes key for content-type header (generated code uses b"content-type" which creates a duplicate key)
    $content = $content -replace 'message\.headers\[b"content-type"\]', 'message.headers["content-type"]'

    if ($content -ne $originalContent) {
        Set-Content -Path $file.FullName -Value $content -NoNewline
        $totalFiles++
        Write-Host "  ✓ Fixed: $($file.Name)" -ForegroundColor Green
    }
}

Write-Host "`n✓ Import fixes completed" -ForegroundColor Green
Write-Host "Files modified: $totalFiles" -ForegroundColor Gray
