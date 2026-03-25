# Fix imports in generated producer files

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$targetDir = Join-Path $scriptDir "hubeau_hydrometrie\hubeau_hydrometrie_producer"

Write-Host "Fixing imports in generated files..." -ForegroundColor Cyan

$files = Get-ChildItem -Path $targetDir -Filter "*.py" -Recurse
$fixedCount = 0
foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw
    $originalContent = $content

    $content = $content -replace 'from hubeau-hydrometrie-producer_data\.', 'from hubeau_hydrometrie.hubeau_hydrometrie_producer.'
    $content = $content -replace 'import hubeau-hydrometrie-producer_data\.', 'import hubeau_hydrometrie.hubeau_hydrometrie_producer.'
    $content = [regex]::Replace($content, 'from hubeau-hydrometrie-producer_data import (\w+)', {
        param($m)
        $className = $m.Groups[1].Value
        $moduleName = $className.ToLower()
        "from hubeau_hydrometrie.hubeau_hydrometrie_producer.fr.gov.eaufrance.hubeau.hydrometrie.$moduleName import $className"
    })
    $content = $content -replace 'message\.headers\[b"content-type"\]', 'message.headers["content-type"]'

    if ($content -ne $originalContent) {
        Set-Content -Path $file.FullName -Value $content -NoNewline
        Write-Host "  Fixed: $($file.Name)" -ForegroundColor Gray
        $fixedCount++
    }
}

Write-Host "✓ Fixed $fixedCount files" -ForegroundColor Green
