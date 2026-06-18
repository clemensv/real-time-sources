#Requires -Version 7
<#
    Fleet EG-MQTT re-validation driver.
    Re-runs every feeders/*/azure-template-with-eventgrid-mqtt.json source
    through the fixed cert-subscriber validator (commit c1245bcdb).
    Isolated auto-deleting RGs, throttled parallelism, per-source logs.
#>
param(
    [int]$Throttle = 10,
    [int]$TimeoutSeconds = 300,
    [string]$Region = "westcentralus",
    [string]$Subscription = "041abda7-3870-4275-ae24-6bf4c5300523",
    [string]$SessionDir = "tests\e2e_deploy\sessions\2026-06-10-205957"
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path "$PSScriptRoot\..\..").Path
Set-Location $repoRoot

# Inject the API keys we have (each source reads only its own param's env var).
$secrets = Get-Content "$repoRoot\tmp\secrets.local.json" -Raw | ConvertFrom-Json
$env:AISSTREAM_API_KEY     = $secrets.aisstream
$env:ENTSOE_SECURITY_TOKEN = $secrets.entsoe
$env:WSDOT_ACCESS_CODE     = $secrets.wsdot
$env:NVE_API_KEY           = $secrets.'nve-hydro'

$logDir = "$repoRoot\tmp\eg-rerun-logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

# All eg sources, minus aisstream (already proven PASS this segment).
$sources = Get-ChildItem "$repoRoot\feeders\*\azure-template-with-eventgrid-mqtt.json" |
    ForEach-Object { $_.Directory.Name } |
    Where-Object { $_ -ne 'aisstream' } |
    Sort-Object

Write-Host "Re-validating $($sources.Count) eg sources (throttle=$Throttle, window=${TimeoutSeconds}s, region=$Region)" -ForegroundColor Cyan
$started = Get-Date

$runner    = "$repoRoot\tests\e2e_deploy\test_azure_aci.ps1"
$absSession = (Resolve-Path "$repoRoot\$SessionDir").Path

$sources | ForEach-Object -ThrottleLimit $Throttle -Parallel {
    $src     = $_
    $runner  = $using:runner
    $session = $using:absSession
    $sub     = $using:Subscription
    $region  = $using:Region
    $timeout = $using:TimeoutSeconds
    $logDir  = $using:logDir
    $log     = Join-Path $logDir "$src.log"
    $stamp   = (Get-Date -Format "HH:mm:ss")
    try {
        & $runner -Source $src -Variant eventgrid-mqtt -SessionDir $session `
            -Subscription $sub -Region $region -TimeoutSeconds $timeout -MinMessages 1 `
            *> $log
        # Read back the result the runner wrote.
        $rf = Join-Path $session "$src-azure-eventgrid-mqtt-result.json"
        if (Test-Path $rf) {
            $r = Get-Content $rf -Raw | ConvertFrom-Json
            $line = "[$stamp] $($src.PadRight(34)) $($r.result.ToUpper().PadRight(5)) msgs=$($r.messages_received)"
        } else {
            # No result file written => early skip (missing key / no template).
            $line = "[$stamp] $($src.PadRight(34)) SKIP  (no result file; missing key or skipped)"
        }
        Write-Host $line
        Add-Content -Path (Join-Path $using:logDir "_summary.log") -Value $line
    }
    catch {
        $line = "[$stamp] $($src.PadRight(34)) ERROR $($_.Exception.Message)"
        Write-Host $line -ForegroundColor Red
        Add-Content -Path (Join-Path $using:logDir "_summary.log") -Value $line
    }
}

$elapsed = (Get-Date) - $started
Write-Host "`nDONE in $([int]$elapsed.TotalMinutes)m. Summary:" -ForegroundColor Green
Get-Content (Join-Path $logDir "_summary.log") | Sort-Object
