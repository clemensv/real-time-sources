# Fix imports in generated producer files
# Replace 'noaa-producer_data' with proper Python package imports

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$targetDir = Join-Path $scriptDir "noaa\noaa_producer\microsoft"

Write-Host "Fixing imports in generated files..." -ForegroundColor Cyan

$files = Get-ChildItem -Path $targetDir -Filter "*.py" -Recurse

$fixedCount = 0
foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw
    $originalContent = $content
    
    # Replace the bad import pattern
    $content = $content -replace 'from noaa-producer_data\.', 'from noaa.noaa_producer.'
    $content = $content -replace 'import noaa-producer_data\.', 'import noaa.noaa_producer.'
    
    if ($content -ne $originalContent) {
        Set-Content -Path $file.FullName -Value $content -NoNewline
        Write-Host "  Fixed: $($file.Name)" -ForegroundColor Gray
        $fixedCount++
    }
}

Write-Host ""
Write-Host "✓ Fixed $fixedCount files" -ForegroundColor Green
