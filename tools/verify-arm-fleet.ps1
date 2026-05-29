<#
.SYNOPSIS
Runs ARM template verification for a fleet of feeder variant tuples.
#>
[CmdletBinding()]
param(
  [string[]]$Tuples,
  [string]$CatalogPath = (Join-Path (Split-Path -Parent $PSScriptRoot) 'catalog.json'),
  [string]$Location = 'westeurope',
  [switch]$KeepResourceGroup,
  [string]$SecretsFile,
  [switch]$DryRun,
  [int]$DataFlowTimeoutSeconds = 300,
  [int]$MaxParallel = 3
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$VariantFiles = @{
  kafka = 'azure-template.json'
  eventhub = 'azure-template-with-eventhub.json'
  servicebus = 'azure-template-with-servicebus.json'
  amqp = 'azure-template-amqp.json'
  mqtt = 'azure-template-mqtt.json'
  'eventgrid-mqtt' = 'azure-template-with-eventgrid-mqtt.json'
}

function Resolve-RepoRoot { Split-Path -Parent $PSScriptRoot }

function Test-TemplateExistsForTuple {
  param([string]$Slug, [string]$Variant)
  $root = Resolve-RepoRoot
  $file = $VariantFiles[$Variant]
  return (Test-Path -LiteralPath (Join-Path $root "feeders\$Slug\$file") -PathType Leaf) -or
         (Test-Path -LiteralPath (Join-Path $root "feeders\$Slug\infra\$file") -PathType Leaf) -or
         (Test-Path -LiteralPath (Join-Path $root "$Slug\$file") -PathType Leaf) -or
         (Test-Path -LiteralPath (Join-Path $root "$Slug\infra\$file") -PathType Leaf)
}

function Get-CatalogTuples {
  param([string]$Path)
  if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Catalog '$Path' not found." }
  $catalog = Get-Content -LiteralPath $Path -Raw -ErrorAction Stop | ConvertFrom-Json -ErrorAction Stop
  $found = New-Object System.Collections.Generic.List[string]
  foreach ($entry in $catalog) {
    $slug = [string]$entry.id
    if (-not $slug) { continue }
    foreach ($variant in $VariantFiles.Keys) {
      if (Test-TemplateExistsForTuple -Slug $slug -Variant $variant) { $found.Add("${slug}:$variant") }
    }
  }
  return [string[]]$found
}

if (-not $Tuples -or $Tuples.Count -eq 0) {
  $Tuples = Get-CatalogTuples -Path $CatalogPath
}
if (-not $Tuples -or $Tuples.Count -eq 0) { throw 'No verification tuples supplied or discovered.' }
if ($MaxParallel -lt 1) { throw '-MaxParallel must be at least 1.' }

$verifier = Join-Path $PSScriptRoot 'verify-arm-template.ps1'
if (-not (Test-Path -LiteralPath $verifier -PathType Leaf)) { throw "Verifier script '$verifier' not found." }

$results = New-Object System.Collections.Generic.List[object]
$jobs = New-Object System.Collections.Generic.List[object]
$queue = [System.Collections.Queue]::new()
foreach ($tuple in $Tuples) { $queue.Enqueue($tuple) }

function Start-VerifyJob {
  param([string]$Tuple)
  if ($Tuple -notmatch '^([^:]+):(kafka|eventhub|servicebus|amqp|mqtt|eventgrid-mqtt)$') {
    throw "Invalid tuple '$Tuple'. Expected slug:variant."
  }
  $slug = $Matches[1]
  $variant = $Matches[2]
  $script:verifierPath = $verifier
  $script:loc = $Location
  $script:keep = [bool]$KeepResourceGroup
  $script:secrets = $SecretsFile
  $script:dry = [bool]$DryRun
  $script:timeout = $DataFlowTimeoutSeconds
  Write-Host "Starting $Tuple..."
  Start-ThreadJob -Name $Tuple -ScriptBlock {
    param($VerifierPath, $Slug, $Variant, $Loc, $Keep, $Secrets, $Dry, $Timeout)
    $args = @('-NoProfile','-ExecutionPolicy','Bypass','-File',$VerifierPath,'-FeederSlug',$Slug,'-Variant',$Variant,'-Location',$Loc,'-DataFlowTimeoutSeconds',[string]$Timeout)
    if ($Keep) { $args += '-KeepResourceGroup' }
    if ($Secrets) { $args += @('-SecretsFile',$Secrets) }
    if ($Dry) { $args += '-DryRun' }
    $started = Get-Date
    $output = & pwsh @args 2>&1
    $exit = $LASTEXITCODE
    [pscustomobject]@{
      Tuple = "${Slug}:$Variant"
      Slug = $Slug
      Variant = $Variant
      ExitCode = $exit
      Status = if ($exit -eq 0) { 'PASS' } else { 'FAIL' }
      Seconds = [Math]::Round(((Get-Date) - $started).TotalSeconds, 1)
      Output = ($output -join "`n")
    }
  } -ArgumentList $verifier, $slug, $variant, $Location, ([bool]$KeepResourceGroup), $SecretsFile, ([bool]$DryRun), $DataFlowTimeoutSeconds
}

while ($queue.Count -gt 0 -or $jobs.Count -gt 0) {
  while ($queue.Count -gt 0 -and $jobs.Count -lt $MaxParallel) {
    $jobs.Add((Start-VerifyJob -Tuple ([string]$queue.Dequeue())))
  }
  if ($jobs.Count -eq 0) { break }
  $completed = Wait-Job -Job $jobs -Any
  foreach ($job in @($completed)) {
    $result = Receive-Job -Job $job -ErrorAction Stop
    Remove-Job -Job $job -Force
    [void]$jobs.Remove($job)
    $results.Add($result)
    Write-Host "Finished $($result.Tuple): $($result.Status) in $($result.Seconds)s"
    if ($result.Status -ne 'PASS') { Write-Host $result.Output }
  }
}

Write-Host ''
Write-Host '==== Fleet verification summary ===='
$results | Sort-Object Tuple | Format-Table Tuple,Status,Seconds,ExitCode -AutoSize

if (@($results | Where-Object { $_.ExitCode -ne 0 }).Count -gt 0) { exit 1 }
exit 0
