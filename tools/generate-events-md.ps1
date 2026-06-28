<#
.SYNOPSIS
    Regenerates source EVENTS.md files from xRegistry manifests.
.DESCRIPTION
    Discovery is repo-driven: every feeders\<source>\xreg\*.xreg.json manifest
    is picked up automatically. To add a source, commit the xRegistry manifest;
    this script derives title/description metadata and writes feeders\<source>\EVENTS.md.
.PARAMETER Source
    Optional source folder id (under feeders\) to regenerate.
.PARAMETER Check
    Regenerate into a repository-local scratch directory and fail when committed
    EVENTS.md differs. Intended as a future CI gate.
#>
[CmdletBinding()]
param([string]$Source, [switch]$Check)

$ErrorActionPreference = 'Continue'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$FeedersRoot = Join-Path $RepoRoot 'feeders'
$PrintDoc = Join-Path $ScriptDir 'printdoc.py'
$ScratchDir = Join-Path $RepoRoot '.events-md-check'

# Hand-maintenance guard: a few EVENTS.md files are hand-polished beyond what
# printdoc.py emits (e.g. README/CONTAINER link-triangle, CloudEvents envelope
# tables, the deterministic-payload NOTE). Regenerating them would silently
# discard that work, so honour an opt-out sentinel: a file that declares
# 'xreg-generator:hand-maintained' is skipped in both generate and -Check modes.
function Test-Protected([string]$Path) {
    if (-not (Test-Path $Path)) { return $false }
    return [bool](Select-String -Path $Path -Pattern 'xreg-generator:hand-maintained' -SimpleMatch -Quiet)
}

function Humanize([string]$Value) {
    (($Value -split '[-_\s]+' | Where-Object { $_ }) | ForEach-Object { $_.Substring(0,1).ToUpperInvariant() + $(if ($_.Length -gt 1) { $_.Substring(1) } else { '' }) }) -join ' '
}
function Read-ReadmeInfo([string]$SourceDir) {
    $r=[ordered]@{Title=$null;Description=$null}; $path=Join-Path $SourceDir 'README.md'
    if (-not (Test-Path $path)) { return $r }
    $lines=Get-Content $path -Encoding UTF8
    foreach ($line in $lines) { if ($line -match '^#\s+(.+)$') { $r.Title=$Matches[1].Trim(); break } }
    $seen=$false; $para=@()
    foreach ($line in $lines) {
        if (-not $seen) { if ($line -match '^#\s+') { $seen=$true }; continue }
        if ([string]::IsNullOrWhiteSpace($line)) { if ($para.Count) { break } else { continue } }
        if ($line -match '^(#|```|\||!\[)') { if ($para.Count) { break } else { continue } }
        $para += $line.Trim()
    }
    if ($para.Count) { $r.Description = ($para -join ' ') }
    return $r
}
function Read-XregInfo([string]$Manifest) {
    $r=[ordered]@{Title=$null;Description=$null}
    try { $j=Get-Content $Manifest -Raw -Encoding UTF8 | ConvertFrom-Json -Depth 100 } catch { return $r }
    if ($j.name) { $r.Title = "$($j.name) Events" }
    if ($j.description) { $r.Description = [string]$j.description }
    elseif ($j.documentation) {
        if ($j.documentation -is [string]) { $r.Description=[string]$j.documentation }
        elseif ($j.documentation.description) { $r.Description=[string]$j.documentation.description }
        elseif ($j.documentation.url) { $r.Description=[string]$j.documentation.url }
    }
    if (-not $r.Description -and $j.messagegroups) {
        $g=$j.messagegroups.PSObject.Properties | ForEach-Object { $_.Value } | Where-Object { $_.description } | Select-Object -First 1
        if ($g) { $r.Description=[string]$g.description }
    }
    return $r
}
function Get-Entries {
    $excluded=@('.git','.github','tools','ghpages','docs','tests','node_modules','.events-md-check','_poller_core')
    Get-ChildItem $FeedersRoot -Directory | Where-Object { $excluded -notcontains $_.Name -and ((-not $Source) -or $_.Name -eq $Source) } | ForEach-Object {
        $dir=$_; $xreg=Join-Path $dir.FullName 'xreg'; if (-not (Test-Path $xreg)) { return }
        Get-ChildItem $xreg -Filter '*.xreg.json' -File | ForEach-Object {
            $xi=Read-XregInfo $_.FullName; $ri=Read-ReadmeInfo $dir.FullName; $human=Humanize $dir.Name
            [pscustomobject]@{
                Source=$dir.Name; Manifest=$_.FullName; Output=(Join-Path $dir.FullName 'EVENTS.md')
                Title=$(if ($xi.Title) { $xi.Title } elseif ($ri.Title) { "$($ri.Title) Events" } else { "$human Bridge Events" })
                Description=$(if ($xi.Description) { $xi.Description } elseif ($ri.Description) { $ri.Description } else { "This document describes the CloudEvents emitted by the $human bridge." })
            }
        }
    }
}
$entries=@(Get-Entries | Sort-Object Source, Manifest)
if ($Source -and -not $entries.Count) { Write-Error "No source with xRegistry manifest found under feeders/ for '$Source'."; exit 2 }
if (-not $entries.Count) { Write-Error 'No xRegistry manifests found under feeders/.'; exit 2 }
if ($Check) { if (Test-Path $ScratchDir) { Remove-Item $ScratchDir -Recurse -Force }; New-Item $ScratchDir -ItemType Directory -Force | Out-Null }
$fail=@(); $stale=@(); $protected=@()
foreach ($e in $entries) {
    if (Test-Protected $e.Output) {
        Write-Host "Skipping $($e.Source): EVENTS.md is hand-maintained (sentinel present); not regenerating."
        $protected += $e.Source; continue
    }
    $target = if ($Check) { Join-Path $ScratchDir "$($e.Source).EVENTS.md" } else { $e.Output }
    Write-Host "Generating $($e.Source): $($e.Manifest) -> $target"
    $old=$env:PRINTDOC_SUPPRESS_COMPAT_NOTICE; $env:PRINTDOC_SUPPRESS_COMPAT_NOTICE='1'
    & python $PrintDoc $e.Manifest --title $e.Title --description $e.Description --output $target
    if ($null -eq $old) { Remove-Item Env:\PRINTDOC_SUPPRESS_COMPAT_NOTICE -ErrorAction SilentlyContinue } else { $env:PRINTDOC_SUPPRESS_COMPAT_NOTICE=$old }
    if ($LASTEXITCODE -ne 0) { $fail += $e.Source; continue }
    if ($Check) {
        if (-not (Test-Path $e.Output)) { $stale += "$($e.Source) (missing EVENTS.md)"; continue }
        $diff=& git --no-pager diff --no-index -- $e.Output $target 2>$null
        if ($LASTEXITCODE -ne 0) { $stale += $e.Source; $diff | Select-Object -First 80 | ForEach-Object { Write-Host $_ } }
    }
}
if ($Check -and (Test-Path $ScratchDir)) { Remove-Item $ScratchDir -Recurse -Force }
if ($fail.Count) { Write-Error "EVENTS.md generation failed for: $($fail -join ', ')" }
if ($stale.Count) { Write-Error "Stale EVENTS.md files: $($stale -join ', ')" }
if ($fail.Count -or $stale.Count) { exit 1 }
if ($protected.Count) { Write-Host "Protected (hand-maintained, skipped): $($protected -join ', ')" }
Write-Host "Processed $($entries.Count) xRegistry manifest(s)."
