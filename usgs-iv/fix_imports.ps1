# Fix import statements in generated producer files

Write-Host "Fixing imports in producer files..." -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$targetDir = Join-Path $scriptDir "usgs_iv" "usgs_iv_producer"

# Get all Python files recursively
$pythonFiles = Get-ChildItem -Path $targetDir -Filter "*.py" -Recurse

$totalFiles = 0

foreach ($file in $pythonFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    $originalContent = $content
    
    # Fix imports for classes from instantaneousvalues
    $instantaneousClasses = @(
        'OtherParameter', 'Precipitation', 'Streamflow', 'GageHeight', 'WaterTemperature',
        'DissolvedOxygen', 'PH', 'SpecificConductance', 'Turbidity', 'AirTemperature',
        'WindSpeed', 'WindDirection', 'RelativeHumidity', 'BarometricPressure', 'TurbidityFNU',
        'FDOM', 'ReservoirStorage', 'LakeElevationNGVD29', 'WaterDepth', 'EquipmentStatus',
        'TidallyFilteredDischarge', 'WaterVelocity', 'EstuaryElevationNGVD29', 'LakeElevationNAVD88',
        'Salinity', 'GateOpening'
    )
    
    foreach ($className in $instantaneousClasses) {
        $classNameLower = $className.ToLower()
        $content = $content -replace "from usgs-iv-producer_data import $className", "from usgs_iv.usgs_iv_producer.usgs.instantaneousvalues.$classNameLower import $className"
    }
    
    # Fix imports for classes from sites
    $content = $content -replace 'from usgs-iv-producer_data import Site', 'from usgs_iv.usgs_iv_producer.usgs.sites.site import Site'
    $content = $content -replace 'from usgs-iv-producer_data import SiteTimeseries', 'from usgs_iv.usgs_iv_producer.usgs.sites.sitetimeseries import SiteTimeseries'
    
    # Fix any dotted imports
    $content = $content -replace 'from usgs-iv-producer_data\.', 'from usgs_iv.usgs_iv_producer.usgs.'
    $content = $content -replace 'import usgs-iv-producer_data\.', 'import usgs_iv.usgs_iv_producer.usgs.'
    
    # Fix usgs-iv-producer_kafka_producer imports  
    $content = $content -replace 'from usgs-iv-producer_kafka_producer\.', 'from usgs_iv.usgs_iv_producer.'
    $content = $content -replace 'import usgs-iv-producer_kafka_producer\.', 'import usgs_iv.usgs_iv_producer.'
    
    if ($content -ne $originalContent) {
        Set-Content -Path $file.FullName -Value $content -NoNewline
        $totalFiles++
        Write-Host "  ✓ Fixed: $($file.Name)" -ForegroundColor Green
    }
}

Write-Host "`n✓ Import fixes completed" -ForegroundColor Green
Write-Host "Files modified: $totalFiles" -ForegroundColor Gray
