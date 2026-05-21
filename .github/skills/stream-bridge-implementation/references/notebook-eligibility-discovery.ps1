<#
.SYNOPSIS
  Discovers which sources in this repo are eligible for Fabric
  notebook hosting retrofit, as defined in the
  stream-bridge-implementation skill.

.DESCRIPTION
  Prints a JSON array of source ids that pass the eligibility gate
  defined in stream-bridge-implementation/SKILL.md (Fabric Notebook
  Hosting section). Use to fan out a fleet of retrofit agents.

.EXAMPLE
  pwsh .github/skills/stream-bridge-implementation/references/notebook-eligibility-discovery.ps1
  pwsh .github/skills/stream-bridge-implementation/references/notebook-eligibility-discovery.ps1 -Format Table
#>
[CmdletBinding()]
param(
    [ValidateSet('Json','Table','Lines')] [string]$Format = 'Json',
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot | Split-Path -Parent | Split-Path -Parent | Split-Path -Parent)
)

$ErrorActionPreference = 'Stop'
Push-Location $RepoRoot
try {
    $catalogPath = Join-Path $RepoRoot 'catalog.json'
    if (-not (Test-Path $catalogPath)) { throw "catalog.json not found at $catalogPath" }
    $catalog = Get-Content $catalogPath -Raw | ConvertFrom-Json
    $publishedIds = $catalog | ForEach-Object { $_.id }

    $e2eTestPath = Join-Path $RepoRoot 'tests/docker_e2e/test_docker_kafka_flow.py'
    $e2eContent = if (Test-Path $e2eTestPath) { Get-Content $e2eTestPath -Raw } else { '' }

    $results = foreach ($id in $publishedIds) {
        $srcDir = Join-Path $RepoRoot $id
        if (-not (Test-Path $srcDir)) { continue }
        if (-not (Test-Path (Join-Path $srcDir 'pyproject.toml'))) { continue }
        if (-not (Test-Path (Join-Path $srcDir 'xreg'))) { continue }
        $existingNb = Get-ChildItem -Path (Join-Path $srcDir 'notebook') -Filter '*.ipynb' -ErrorAction SilentlyContinue
        if ($existingNb) { continue }  # Already retrofitted

        $bridge = Get-ChildItem -Path $srcDir -Recurse -Include '*.py' -ErrorAction SilentlyContinue |
            Where-Object { $_.FullName -notmatch '_producer|[\\/]tests[\\/]|conftest\.py' } |
            Where-Object { Select-String -Path $_.FullName -Pattern '^def main\(' -Quiet } |
            Select-Object -First 1
        if (-not $bridge) { continue }

        $bridgeText = Get-Content $bridge.FullName -Raw
        $hasOnceCli = $bridgeText -match '--once'
        $hasOnceEnv = $bridgeText -match 'ONCE_MODE'
        $hasPollSig = $bridgeText -match 'time\.sleep|asyncio\.sleep|POLLING_INTERVAL|polling_interval|--interval'
        $hasStream  = $bridgeText -match 'websockets?\.connect|aiomqtt|paho\.mqtt|sseclient|EventSource'
        $hasE2E     = $e2eContent -match "['\""]$id['\""]|class\s+\w*$($id -replace '-','_')"

        $status = if ($hasStream)                              { 'skip:streaming' }
                  elseif (-not $hasPollSig)                    { 'skip:not-a-poller' }
                  elseif (-not $hasE2E)                        { 'skip:no-e2e' }
                  elseif ($hasOnceCli)                         { 'ready' }
                  elseif ($hasOnceEnv)                         { 'ready-env' }
                  else                                         { 'needs-once-flag' }

        [PSCustomObject]@{
            id              = $id
            status          = $status
            bridge          = $bridge.Name
            hasOnceCli      = $hasOnceCli
            hasOnceEnv      = $hasOnceEnv
            hasPollSig      = $hasPollSig
            hasStream       = $hasStream
            hasE2E          = $hasE2E
        }
    }

    switch ($Format) {
        'Table' { $results | Format-Table -AutoSize }
        'Lines' { $results | Where-Object { $_.status -like 'ready*' -or $_.status -eq 'needs-once-flag' } | ForEach-Object { $_.id } }
        default { $results | ConvertTo-Json -Depth 3 }
    }
}
finally { Pop-Location }
