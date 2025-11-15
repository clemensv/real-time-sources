# Fix test mocks to use new class name

Write-Host "Fixing test mocks..." -ForegroundColor Cyan

$testFiles = @(
    "tests\test_noaa_unit.py",
    "tests\test_noaa_integration.py",
    "tests\test_noaa_e2e.py"
)

$fixCount = 0

foreach ($file in $testFiles) {
    if (Test-Path $file) {
        Write-Host "  Processing: $file" -ForegroundColor Yellow
        $content = Get-Content -Path $file -Raw
        $originalContent = $content
        
        # Replace old class name with new one in @patch decorators
        $content = $content -replace "MicrosoftOpendataUsNoaaEventProducer", "MicrosoftOpenDataUSNOAAEventProducer"
        
        if ($content -ne $originalContent) {
            Set-Content -Path $file -Value $content -NoNewline
            Write-Host "  Fixed: $file" -ForegroundColor Green
            $fixCount++
        } else {
            Write-Host "  No changes needed: $file" -ForegroundColor Gray
        }
    } else {
        Write-Host "  Not found: $file" -ForegroundColor Red
    }
}

Write-Host "`n✓ Fixed $fixCount test files" -ForegroundColor Green
