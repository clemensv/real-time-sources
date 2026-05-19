<#
.SYNOPSIS
    Deploys a real-time-source feeder as a Fabric notebook (instead of an
    ACI container). The notebook runs the source's bridge package via
    `python -m <source> feed --once` on each invocation.

.DESCRIPTION
    Two-stage workflow that delegates Fabric infra setup to the existing
    deploy-fabric.ps1 script:

      Stage A. Calls deploy-fabric.ps1 with -SkipArm to:
                - resolve/create the Fabric workspace
                - resolve/create the Eventhouse + KQL database + apply schema
                - create the Event Stream and bind its custom-endpoint
                - retrieve the Event Stream connection string (written to
                  a temp file via the new -OutCsFile switch)

      Stage B. Patches the source's notebook
              (<source>/notebook/<source>-feed.ipynb):
                - sets CONNECTION_STRING from Stage A
                - sets STATE_FILE to a Lakehouse path
                - sets SOURCE_REF to the deploy branch (default 'main')
                - binds metadata.dependencies.kqlDatabases to the source DB
              and uploads it to the Fabric workspace.

    The user then runs / schedules the notebook from the Fabric portal.
    A Data Factory pipeline + schedule trigger can be added in a future
    iteration; for the prototype the notebook is the only artifact.

.PARAMETER Source
    Source name (folder name in this repo). Currently only 'pegelonline'
    ships a notebook; this script is generic so other sources can opt in
    by adding <source>/notebook/<source>-feed.ipynb.

.PARAMETER Workspace
    Fabric workspace name or GUID.

.PARAMETER Eventhouse
    Fabric eventhouse name. Default: source name (with '-' -> '_').

.PARAMETER DatabaseName
    KQL database name. Default: source name (with '-' -> '_').

.PARAMETER SubscriptionId
    Azure subscription ID used by Stage A.

.PARAMETER ResourceGroup
    Required by Stage A's deploy-fabric.ps1 contract (used as scratch).
    Not actually used for ACI since -SkipArm is set.

.PARAMETER Location
    Azure region (parity with Stage A).

.PARAMETER Repo
    GitHub repo for `pip install git+...`. Default 'clemensv/real-time-sources'.

.PARAMETER Branch
    Branch to install from. Default 'main'.

.PARAMETER NotebookName
    Display name of the Fabric notebook item. Default '<source>-feed'.

.PARAMETER StatePath
    Lakehouse-mounted directory used by the bridge for dedupe state.
    Default '/lakehouse/default/Files/feeder-state/<source>'.

.PARAMETER PollingInterval
    Bridge polling interval in seconds (used if ONCE_MODE is disabled).
    Default 900 (matches pegelonline's native upstream cadence).

.PARAMETER OnceMode
    If $true (default), the bridge exits after one polling cycle. Use
    in scheduled runs. Set to $false to let the bridge loop forever
    (e.g., always-on Spark session).

.PARAMETER SkipInfra
    Skip Stage A. Use when the KQL DB / Event Stream already exist.
    The notebook resolves the Event Stream connection string at runtime
    via the Topology API, so no -ConnectionString parameter is needed.

.EXAMPLE
    ./deploy-feeder-notebook.ps1 -Source pegelonline `
        -SubscriptionId 041abda7-... `
        -ResourceGroup rg-pegelonline-test `
        -Workspace ContosoRealTimeTest `
        -Eventhouse ContosoRealTimeTest-eh
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Source,

    [string]$ResourceGroup,
    [string]$Location,
    [string]$SubscriptionId,

    [Parameter(Mandatory = $true)]
    [string]$Workspace,

    [string]$Eventhouse,
    [string]$DatabaseName,

    [string]$Repo = "clemensv/real-time-sources",
    [string]$Branch = "main",

    [string]$NotebookName,
    [string]$StatePath,
    [int]$PollingInterval = 900,
    [bool]$OnceMode = $true,

    [string]$EnvironmentName,
    [switch]$SkipEnvironment,
    [switch]$BuildWheelsLocally,
    [string]$WheelsBundleUrl,

    [string]$DefaultLakehouse,
    [int]$ScheduleIntervalMinutes = 15,
    [switch]$NoSchedule,
    [switch]$NoTriggerNow,

    [switch]$SkipInfra
)

$ErrorActionPreference = "Stop"
$FabricApi = "https://api.fabric.microsoft.com/v1"
$guidRx = '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
$TempDir = if ($env:TEMP) { $env:TEMP } elseif ($env:TMPDIR) { $env:TMPDIR } else { [System.IO.Path]::GetTempPath() }

if (-not $ResourceGroup)           { $ResourceGroup = "rg-$Source-notebook" }
if (-not $DatabaseName)            { $DatabaseName = $Source -replace '-', '_' }
if ([string]::IsNullOrWhiteSpace($Eventhouse)) { $Eventhouse = $Source -replace '-', '_' }
if (-not $NotebookName)            { $NotebookName = "$Source-feed" }
if (-not $StatePath)               { $StatePath    = "/lakehouse/default/Files/feeder-state/$Source" }
if (-not $EnvironmentName)         { $EnvironmentName = "$Source-feeder-env" }

$repoRoot     = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$notebookPath = Join-Path $repoRoot "$Source/notebook/$Source-feed.ipynb"
if (-not (Test-Path $notebookPath)) {
    # Cloud Shell / standalone usage: only the helper scripts were downloaded,
    # not the full repo. Try to fetch the notebook from GitHub raw.
    $rawNbUrl = "https://raw.githubusercontent.com/$Repo/$Branch/$Source/notebook/$Source-feed.ipynb"
    $localNb  = Join-Path $TempDir "$Source-feed_$(Get-Random).ipynb"
    Write-Host "Notebook not in working tree; downloading from $rawNbUrl" -ForegroundColor DarkYellow
    try {
        Invoke-WebRequest -Uri $rawNbUrl -OutFile $localNb -UseBasicParsing -ErrorAction Stop
        $notebookPath = $localNb
    } catch {
        throw "Notebook not found locally and could not be downloaded from $rawNbUrl. " +
              "Source '$Source' may not have a Fabric notebook published yet (expected " +
              "$Source/notebook/$Source-feed.ipynb in the repo). Underlying error: $($_.Exception.Message)"
    }
}

function Write-Step { param([string]$Step, [string]$Msg) Write-Host "`n[$Step] $Msg" -ForegroundColor Yellow }
function Write-OK   { param([string]$Msg) Write-Host "  $Msg" -ForegroundColor Green }
function Write-Info { param([string]$Msg) Write-Host "  $Msg" -ForegroundColor DarkYellow }

function Invoke-FabricApi {
    param([string]$Method, [string]$Url, [object]$Body)
    $azArgs = @("rest", "--method", $Method, "--url", $Url, "--resource", "https://api.fabric.microsoft.com")
    if ($Body) {
        $bodyFile = Join-Path $TempDir "fabric_body_$(Get-Random).json"
        $json = if ($Body -is [string]) { $Body } else { $Body | ConvertTo-Json -Depth 30 -Compress }
        [System.IO.File]::WriteAllText($bodyFile, $json, [System.Text.UTF8Encoding]::new($false))
        $azArgs += @("--body", "@$bodyFile", "--headers", "Content-Type=application/json")
    }
    $result = & az @azArgs 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Fabric API error ($Method $Url): $($result | Out-String)" }
    if ($result) { return $result | ConvertFrom-Json }
    return $null
}

function Invoke-FabricApiRaw {
    # Same as Invoke-FabricApi, but returns the raw response (so 202 LROs can be inspected).
    param([string]$Method, [string]$Url, [object]$Body)
    $azArgs = @("rest", "--method", $Method, "--url", $Url, "--resource", "https://api.fabric.microsoft.com", "--output", "json")
    if ($Body) {
        $bodyFile = Join-Path $TempDir "fabric_body_$(Get-Random).json"
        $json = if ($Body -is [string]) { $Body } else { $Body | ConvertTo-Json -Depth 30 -Compress }
        [System.IO.File]::WriteAllText($bodyFile, $json, [System.Text.UTF8Encoding]::new($false))
        $azArgs += @("--body", "@$bodyFile", "--headers", "Content-Type=application/json")
    }
    $result = & az @azArgs 2>&1
    return [pscustomobject]@{ ExitCode = $LASTEXITCODE; Body = ($result | Out-String) }
}

function Get-PrebuiltWheels {
    <#
    Download the per-source wheel bundle from the `notebook-wheels` release
    (built by .github/workflows/publish-notebook-wheels.yml). Returns the
    array of extracted .whl FileInfo objects in a fresh temp dir.

    -WheelsBundleUrl overrides the default release-asset URL. Useful for
    pinning to a specific commit or using a fork.
    #>
    param([string]$Source, [string]$Repo, [string]$WheelsBundleUrl)

    if (-not $WheelsBundleUrl) {
        $WheelsBundleUrl = "https://github.com/$Repo/releases/download/notebook-wheels/$Source-notebook-wheels.zip"
    }

    $outDir = Join-Path $TempDir "feeder-wheels-$Source-$(Get-Random)"
    New-Item -ItemType Directory -Force -Path $outDir | Out-Null
    $zipFile = Join-Path $outDir "$Source-notebook-wheels.zip"

    Write-Info "  downloading $WheelsBundleUrl"
    try {
        Invoke-WebRequest -Uri $WheelsBundleUrl -OutFile $zipFile -ErrorAction Stop
    } catch {
        throw "Failed to download wheel bundle from $WheelsBundleUrl`: $($_.Exception.Message)`nIf the source's wheels haven't been published yet, rerun with -BuildWheelsLocally."
    }

    Expand-Archive -LiteralPath $zipFile -DestinationPath $outDir -Force
    Remove-Item $zipFile

    $manifestFile = Join-Path $outDir "manifest.json"
    if (Test-Path $manifestFile) {
        $manifest = Get-Content $manifestFile -Raw | ConvertFrom-Json
        Write-OK "  bundle built from commit $($manifest.shortCommit) at $($manifest.built_utc)"
    }

    $wheels = Get-ChildItem -LiteralPath $outDir -Filter *.whl
    if (-not $wheels) { throw "No wheels found in $WheelsBundleUrl" }
    return ,$wheels
}

function Build-SourceWheels {
    <#
    Builds wheels for the source's bridge + its generated producer sub-packages
    using `pip wheel --no-deps` and strips poetry path-deps from the top-level
    wheel's METADATA so it installs cleanly in the Fabric Environment.

    Returns an array of FileInfo objects pointing at the wheels under $outDir.
    #>
    param([string]$Source, [string]$RepoRoot)

    $srcDir = Join-Path $RepoRoot $Source
    if (-not (Test-Path $srcDir)) { throw "Source folder not found: $srcDir" }

    $producerRoot = Join-Path $srcDir "$($Source -replace '-', '_')_producer"
    if (-not (Test-Path $producerRoot)) { throw "Generated producer folder not found: $producerRoot. Run generate_producer.ps1 first." }

    $outDir = Join-Path $TempDir "feeder-wheels-$Source-$(Get-Random)"
    New-Item -ItemType Directory -Force -Path $outDir | Out-Null

    # Build the producer sub-packages first (each is a self-contained poetry project),
    # then the top-level source bridge package which references them via path-deps.
    $subPackages = Get-ChildItem -Directory $producerRoot |
        Where-Object { Test-Path (Join-Path $_.FullName "pyproject.toml") } |
        ForEach-Object { $_.FullName }
    $toBuild = @($subPackages) + @($srcDir)

    foreach ($pkgDir in $toBuild) {
        Write-Info "  pip wheel $($pkgDir | Split-Path -Leaf)"
        & python -m pip wheel --no-deps --no-build-isolation --wheel-dir $outDir $pkgDir 2>&1 | Out-Host
        if ($LASTEXITCODE -ne 0) { throw "pip wheel failed for $pkgDir" }
    }

    $wheels = Get-ChildItem -LiteralPath $outDir -Filter *.whl
    if (-not $wheels) { throw "No wheels produced in $outDir" }

    $stripper = Join-Path $PSScriptRoot "strip-wheel-pathdeps.py"
    & python $stripper @($wheels | ForEach-Object { $_.FullName }) | Out-Host
    if ($LASTEXITCODE -ne 0) { throw "Wheel METADATA post-processing failed." }

    return ,$wheels
}

function Get-FabricToken {
    $tok = az account get-access-token --resource https://api.fabric.microsoft.com --query accessToken -o tsv 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Failed to acquire Fabric token: $tok" }
    return ($tok | Out-String).Trim()
}

function Upload-EnvironmentLibrary {
    <#
    POST /environments/{id}/staging/libraries with multipart/form-data 'file' part.
    The Fabric SDKs perform this upload one library file at a time.
    #>
    param([string]$WorkspaceId, [string]$EnvironmentId, [System.IO.FileInfo]$Wheel, [string]$Token)

    $url = "$FabricApi/workspaces/$WorkspaceId/environments/$EnvironmentId/staging/libraries"
    try {
        $resp = Invoke-WebRequest -Uri $url -Method Post `
            -Headers @{ Authorization = "Bearer $Token" } `
            -Form @{ file = $Wheel } `
            -UseBasicParsing -ErrorAction Stop
        return $resp.StatusCode
    } catch {
        $errBody = ""
        if ($_.Exception.Response) {
            try {
                $stream = $_.Exception.Response.GetResponseStream()
                $reader = New-Object System.IO.StreamReader($stream)
                $errBody = $reader.ReadToEnd()
            } catch {}
        }
        throw "Upload library '$($Wheel.Name)' failed: $($_.Exception.Message)`n$errBody"
    }
}

function Update-EnvironmentSparkCompute {
    param([string]$WorkspaceId, [string]$EnvironmentId)

    # The staging/sparkcompute endpoint accepts JSON; runtime_version 1.3 keeps things current.
    $body = @{
        instancePool = @{ name = "Starter Pool"; type = "Workspace" }
        driverCores = 4
        driverMemory = "28g"
        executorCores = 4
        executorMemory = "28g"
        dynamicExecutorAllocation = @{ enabled = $false }
        runtimeVersion = "1.3"
        sparkProperties = @{}
    }
    Invoke-FabricApi -Method PATCH `
        -Url "$FabricApi/workspaces/$WorkspaceId/environments/$EnvironmentId/staging/sparkcompute" `
        -Body $body | Out-Null
}

function Wait-EnvironmentPublished {
    param([string]$WorkspaceId, [string]$EnvironmentId, [int]$TimeoutMinutes = 25)

    $deadline = (Get-Date).AddMinutes($TimeoutMinutes)
    $lastState = ""
    while ((Get-Date) -lt $deadline) {
        try {
            $publishUri = "$FabricApi/workspaces/$WorkspaceId/environments/$EnvironmentId"
            $env = Invoke-FabricApi -Method GET -Url $publishUri
            $state = $null
            if ($env.properties -and $env.properties.publishDetails) {
                $state = $env.properties.publishDetails.state
            }
            if ($state -and $state -ne $lastState) {
                Write-Info "    publish state: $state"
                $lastState = $state
            }
            if ($state -eq "Success" -or $state -eq "Published") { return }
            if ($state -eq "Failed" -or $state -eq "Cancelled") {
                throw "Environment publish ended in state '$state'."
            }
        } catch {
            Write-Info "    poll error (will retry): $_"
        }
        Start-Sleep -Seconds 15
    }
    throw "Environment publish did not finish within $TimeoutMinutes minutes."
}

Write-Host "=== $Source Notebook Feeder Deployment ===" -ForegroundColor Cyan
Write-Host "  Source:           $Source"          -ForegroundColor White
Write-Host "  Workspace:        $Workspace"       -ForegroundColor White
Write-Host "  Eventhouse:       $Eventhouse"      -ForegroundColor White
Write-Host "  KQL Database:     $DatabaseName"    -ForegroundColor White
Write-Host "  Notebook:         $NotebookName"    -ForegroundColor White
Write-Host "  Notebook file:    $notebookPath"    -ForegroundColor White
Write-Host "  Source ref:       $Repo@$Branch"    -ForegroundColor White
Write-Host "  Polling interval: $PollingInterval s (once-mode=$OnceMode)" -ForegroundColor White

# ── Stage A: Fabric infra (Eventhouse + KQL DB + Event Stream) ────────────
# The notebook resolves the Event Stream connection string at runtime via
# the Topology API using its workspace/user identity, so Stage A only needs
# to ensure the Fabric infra exists. No connection string is required here.
if (-not $SkipInfra) {
    Write-Step "A" "Setting up Fabric infra via deploy-fabric.ps1 -SkipArm..."
    $deployFabric = Join-Path $PSScriptRoot "deploy-fabric.ps1"
    if (-not (Test-Path $deployFabric)) { throw "deploy-fabric.ps1 not found alongside this script." }

    $fwdArgs = @{
        Source        = $Source
        ResourceGroup = $ResourceGroup
        Workspace     = $Workspace
        Eventhouse    = $Eventhouse
        DatabaseName  = $DatabaseName
        Repo          = $Repo
        Branch        = $Branch
        SkipArm       = $true
    }
    if ($Location)       { $fwdArgs['Location']       = $Location }
    if ($SubscriptionId) { $fwdArgs['SubscriptionId'] = $SubscriptionId }

    & $deployFabric @fwdArgs
    if ($LASTEXITCODE -ne 0) {
        throw "deploy-fabric.ps1 failed; aborting notebook deploy."
    }
}

# ── Stage B: Resolve workspace + KQL DB ───────────────────────────────────
Write-Step "B/1" "Resolving Fabric workspace..."
if ($SubscriptionId -and -not $SkipInfra) {
    # already set by deploy-fabric.ps1
} elseif ($SubscriptionId) {
    az account set --subscription $SubscriptionId 2>&1 | Out-Null
}

if ($Workspace -match $guidRx) {
    $WorkspaceId = $Workspace
} else {
    $allWs = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces"
    $ws = $allWs.value | Where-Object { $_.displayName -eq $Workspace } | Select-Object -First 1
    if (-not $ws) { throw "Workspace '$Workspace' not found." }
    $WorkspaceId = $ws.id
}
$wsInfo = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId"
Write-OK "Workspace: $($wsInfo.displayName) ($WorkspaceId)"

Write-Step "B/2" "Resolving KQL database..."
$ehList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses"
$eh = $ehList.value | Where-Object { $_.displayName -eq $Eventhouse -or $_.id -eq $Eventhouse } | Select-Object -First 1
if (-not $eh) { throw "Eventhouse '$Eventhouse' not found in workspace." }
Write-OK "Eventhouse: $($eh.displayName) ($($eh.id))"

$dbList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases"
$db = $dbList.value | Where-Object { $_.displayName -eq $DatabaseName } | Select-Object -First 1
if (-not $db) { throw "KQL database '$DatabaseName' not found. Stage A should have created it." }
Write-OK "KQL database: $($db.displayName) ($($db.id))"

$queryUri = $eh.properties.queryServiceUri

# ── Stage B/2.5: Fabric Environment with pre-built source wheels ─────────
$EnvironmentId = $null
if (-not $SkipEnvironment) {
    Write-Step "B/2.5" "Building source wheels and publishing Fabric Environment '$EnvironmentName'..."

    $wheels = if ($BuildWheelsLocally) {
        Write-Info "Building wheels locally (-BuildWheelsLocally)..."
        Build-SourceWheels -Source $Source -RepoRoot $repoRoot
    } else {
        Write-Info "Downloading pre-built wheel bundle from GitHub release..."
        try {
            Get-PrebuiltWheels -Source $Source -Repo $Repo -WheelsBundleUrl $WheelsBundleUrl
        } catch {
            Write-Info "  bundle download failed; falling back to local build."
            Write-Info "  ($($_.Exception.Message))"
            Build-SourceWheels -Source $Source -RepoRoot $repoRoot
        }
    }
    Write-OK "Got $($wheels.Count) wheel(s):"
    foreach ($w in $wheels) { Write-Info "  $($w.Name)" }

    # Resolve-or-create the environment item.
    $envList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/environments"
    $envItem = $envList.value | Where-Object { $_.displayName -eq $EnvironmentName } | Select-Object -First 1
    if (-not $envItem) {
        Write-Info "Creating environment '$EnvironmentName'..."
        $createEnv = Invoke-FabricApi -Method POST -Url "$FabricApi/workspaces/$WorkspaceId/environments" `
            -Body @{ displayName = $EnvironmentName; description = "Pre-built libraries for $Source feeder notebook." }
        if ($createEnv -and $createEnv.id) {
            $envItem = $createEnv
        } else {
            $envList2 = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/environments"
            $envItem = $envList2.value | Where-Object { $_.displayName -eq $EnvironmentName } | Select-Object -First 1
            if (-not $envItem) { throw "Environment '$EnvironmentName' was not found after create." }
        }
    }
    $EnvironmentId = $envItem.id
    Write-OK "Environment: $EnvironmentName ($EnvironmentId)"

    Write-Info "Uploading wheels one at a time to staging libraries..."
    $fabricToken = Get-FabricToken
    foreach ($w in $wheels) {
        Write-Info "  uploading $($w.Name)"
        $sc = Upload-EnvironmentLibrary -WorkspaceId $WorkspaceId -EnvironmentId $EnvironmentId -Wheel $w -Token $fabricToken
        Write-Info "    -> HTTP $sc"
    }

    Write-Info "Setting Spark compute (runtime 1.3, Starter Pool)..."
    try {
        Update-EnvironmentSparkCompute -WorkspaceId $WorkspaceId -EnvironmentId $EnvironmentId
    } catch {
        Write-Info "  Spark compute update warning (non-fatal, defaults will be used): $($_.Exception.Message)"
    }

    Write-Info "Publishing environment (3-6 min — building Spark image with custom libraries)..."
    Invoke-FabricApiRaw -Method POST `
        -Url "$FabricApi/workspaces/$WorkspaceId/environments/$EnvironmentId/staging/publish" | Out-Null

    Wait-EnvironmentPublished -WorkspaceId $WorkspaceId -EnvironmentId $EnvironmentId
    Write-OK "Environment published."
} else {
    # Look it up to bind metadata.
    $envList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/environments"
    $envItem = $envList.value | Where-Object { $_.displayName -eq $EnvironmentName } | Select-Object -First 1
    if ($envItem) { $EnvironmentId = $envItem.id; Write-Info "Reusing environment '$EnvironmentName' ($EnvironmentId)" }
}

# ── Stage B/3: Patch notebook ─────────────────────────────────────────────
Write-Step "B/3" "Patching notebook parameters + KQL/Environment binding..."
$nbJson = Get-Content -LiteralPath $notebookPath -Raw -Encoding UTF8
$nb = $nbJson | ConvertFrom-Json

if (-not $nb.metadata)              { $nb | Add-Member -NotePropertyName metadata     -NotePropertyValue ([pscustomobject]@{}) -Force }
if (-not $nb.metadata.dependencies) { $nb.metadata | Add-Member -NotePropertyName dependencies -NotePropertyValue ([pscustomobject]@{}) -Force }
$kqlBinding = @(
    [pscustomobject]@{
        name        = $db.displayName
        displayName = $db.displayName
        workspaceId = $WorkspaceId
        itemId      = $db.id
    }
)
$nb.metadata.dependencies | Add-Member -NotePropertyName kqlDatabases -NotePropertyValue $kqlBinding -Force

# Resolve and bind a default Lakehouse so the notebook's /lakehouse/default/Files/... path works.
$lakehouseList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/lakehouses"
$lh = $null
if ($DefaultLakehouse) {
    $lh = $lakehouseList.value | Where-Object { $_.displayName -eq $DefaultLakehouse -or $_.id -eq $DefaultLakehouse } | Select-Object -First 1
    if (-not $lh) { throw "Default lakehouse '$DefaultLakehouse' not found in workspace." }
} elseif ($lakehouseList.value.Count -eq 1) {
    $lh = $lakehouseList.value[0]
    Write-Info "Auto-selected only lakehouse in workspace: $($lh.displayName)"
} elseif ($lakehouseList.value.Count -gt 1) {
    throw "Workspace has $($lakehouseList.value.Count) lakehouses. Pass -DefaultLakehouse <name> to choose one."
} else {
    # No Lakehouse — auto-create one for feeder state. Use a stable
    # workspace-scoped name so subsequent deploys to the same workspace
    # reuse it (the bridge writes per-source under Files/feeder-state/<src>).
    $newLakehouseName = 'feeder-state-lake'
    Write-Info "Workspace has no Lakehouse; creating '$newLakehouseName' for feeder state..."
    $createBody = @{ displayName = $newLakehouseName } | ConvertTo-Json
    $lh = Invoke-FabricApi -Method POST -Url "$FabricApi/workspaces/$WorkspaceId/lakehouses" -Body $createBody
    if (-not $lh -or -not $lh.id) {
        # Long-running operation: re-list and resolve by name.
        Start-Sleep -Seconds 5
        $lakehouseList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/lakehouses"
        $lh = $lakehouseList.value | Where-Object { $_.displayName -eq $newLakehouseName } | Select-Object -First 1
    }
    if (-not $lh) { throw "Failed to create default Lakehouse '$newLakehouseName'." }
    Write-OK "Created Lakehouse: $($lh.displayName) ($($lh.id))"
}
$nb.metadata.dependencies | Add-Member -NotePropertyName lakehouse -NotePropertyValue ([pscustomobject]@{
    default_lakehouse              = $lh.id
    default_lakehouse_name         = $lh.displayName
    default_lakehouse_workspace_id = $WorkspaceId
}) -Force
Write-OK "Default Lakehouse bound: $($lh.displayName) ($($lh.id))"

if ($EnvironmentId) {
    $envBinding = [pscustomobject]@{
        environmentId   = $EnvironmentId
        workspaceId     = $WorkspaceId
        environmentName = $EnvironmentName
    }
    $nb.metadata.dependencies | Add-Member -NotePropertyName environment -NotePropertyValue $envBinding -Force
}

$onceLiteral = if ($OnceMode) { "True" } else { "False" }

$paramsPatched = $false
foreach ($cell in $nb.cells) {
    if ($cell.cell_type -ne 'code') { continue }
    $tags = @()
    if ($cell.metadata -and $cell.metadata.tags) { $tags = @($cell.metadata.tags) }
    if ($tags -notcontains 'parameters') { continue }

    $srcLines = @($cell.source) | ForEach-Object { $_ }
    $newLines = foreach ($line in $srcLines) {
        if     ($line -match '^\s*EVENTSTREAM_NAME\s*=') { "EVENTSTREAM_NAME = `"$Source-ingest`"`n" }
        elseif ($line -match '^\s*STATE_FILE\s*=')       { "STATE_FILE       = `"$StatePath/state.json`"`n" }
        elseif ($line -match '^\s*POLLING_INTERVAL\s*=') { "POLLING_INTERVAL = $PollingInterval`n" }
        elseif ($line -match '^\s*ONCE_MODE\s*=')        { "ONCE_MODE        = $onceLiteral`n" }
        elseif ($line -match '^\s*WORKSPACE_ID\s*=')     { "WORKSPACE_ID     = `"$WorkspaceId`"`n" }
        elseif ($line -match '^\s*KUSTO_URI\s*=')        { "KUSTO_URI        = `"$queryUri`"`n" }
        elseif ($line -match '^\s*KUSTO_DATABASE\s*=')   { "KUSTO_DATABASE   = `"$($db.displayName)`"`n" }
        elseif ($line -match '^\s*SOURCE_REF\s*=')       { "SOURCE_REF       = `"$Branch`"`n" }
        else                                             { $line }
    }
    $cell.source = @($newLines)
    $paramsPatched = $true
    break
}
if (-not $paramsPatched) { throw "Notebook has no 'parameters'-tagged cell to patch." }
Write-OK "Parameters cell patched."

$tmpNb = Join-Path $TempDir "$Source`_feed_$(Get-Random).ipynb"
[System.IO.File]::WriteAllText($tmpNb, ($nb | ConvertTo-Json -Depth 50), [System.Text.UTF8Encoding]::new($false))

# ── Stage B/4: Upload notebook ────────────────────────────────────────────
Write-Step "B/4" "Uploading notebook to Fabric workspace..."
$nbBytes  = [System.IO.File]::ReadAllBytes($tmpNb)
$nbBase64 = [Convert]::ToBase64String($nbBytes)
$definition = @{
    format = "ipynb"
    parts  = @(@{ path = "notebook-content.ipynb"; payload = $nbBase64; payloadType = "InlineBase64" })
}

$nbList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/notebooks"
$existing = $nbList.value | Where-Object { $_.displayName -eq $NotebookName } | Select-Object -First 1

if ($existing) {
    Invoke-FabricApi -Method POST `
        -Url "$FabricApi/workspaces/$WorkspaceId/notebooks/$($existing.id)/updateDefinition" `
        -Body @{ definition = $definition } | Out-Null
    Write-OK "Updated existing notebook '$NotebookName' ($($existing.id))"
    $notebookId = $existing.id
} else {
    $createBody = @{ displayName = $NotebookName; definition = $definition }
    $createResp = Invoke-FabricApi -Method POST -Url "$FabricApi/workspaces/$WorkspaceId/notebooks" -Body $createBody
    if ($createResp -and $createResp.id) {
        $notebookId = $createResp.id
    } else {
        $nbList2 = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/notebooks"
        $created = $nbList2.value | Where-Object { $_.displayName -eq $NotebookName } | Select-Object -First 1
        if (-not $created) { throw "Notebook '$NotebookName' was not found after create." }
        $notebookId = $created.id
    }
    Write-OK "Created notebook '$NotebookName' ($notebookId)"
}

Remove-Item $tmpNb -ErrorAction SilentlyContinue

# ── Stage B/5: Trigger a first run + create a recurring schedule ─────────
if (-not $NoTriggerNow) {
    Write-Step "B/5a" "Triggering immediate notebook run..."
    $runResp = Invoke-FabricApiRaw -Method POST `
        -Url "$FabricApi/workspaces/$WorkspaceId/items/$notebookId/jobs/instances?jobType=RunNotebook"
    if ($runResp.ExitCode -eq 0) {
        Write-OK "Run triggered (202 Accepted)."
    } else {
        Write-Warning "Could not trigger immediate run (run it manually from the portal):`n$($runResp.Body)"
    }
}

if (-not $NoSchedule) {
    Write-Step "B/5b" "Creating recurring schedule (every $ScheduleIntervalMinutes min)..."
    $existingSchedules = $null
    try {
        $existingSchedules = Invoke-FabricApi -Method GET `
            -Url "$FabricApi/workspaces/$WorkspaceId/items/$notebookId/jobs/RunNotebook/schedules"
    } catch { }

    if ($existingSchedules -and $existingSchedules.value -and $existingSchedules.value.Count -gt 0) {
        Write-Info "Schedule already exists ($($existingSchedules.value.Count) entries); skipping create."
    } else {
        # Cron interval supports 5-60 minutes per Fabric scheduler docs.
        $startDt = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss")
        $endDt   = (Get-Date).ToUniversalTime().AddYears(5).ToString("yyyy-MM-ddTHH:mm:ss")
        $schedBody = @{
            enabled = $true
            configuration = @{
                type             = "Cron"
                interval         = $ScheduleIntervalMinutes
                startDateTime    = $startDt
                endDateTime      = $endDt
                localTimeZoneId  = "UTC"
            }
        }
        $schedResp = Invoke-FabricApiRaw -Method POST `
            -Url "$FabricApi/workspaces/$WorkspaceId/items/$notebookId/jobs/RunNotebook/schedules" `
            -Body $schedBody
        if ($schedResp.ExitCode -eq 0) {
            Write-OK "Schedule created (every $ScheduleIntervalMinutes min UTC)."
        } else {
            Write-Warning "Could not create schedule (create it manually from the portal):`n$($schedResp.Body)"
        }
    }
}

Write-Host "`n=== Notebook Feeder Deployment Complete ===" -ForegroundColor Cyan
Write-Host "  Notebook:     $NotebookName ($notebookId)" -ForegroundColor Gray
Write-Host "  Workspace:    $($wsInfo.displayName) ($WorkspaceId)" -ForegroundColor Gray
Write-Host "  KQL Database: $($db.displayName) ($($db.id))" -ForegroundColor Gray
if ($EnvironmentId) {
    Write-Host "  Environment:  $EnvironmentName ($EnvironmentId)" -ForegroundColor Gray
}
Write-Host "  State path:   $StatePath  (Lakehouse Files)" -ForegroundColor Gray
Write-Host ""
Write-Host "  Open in Fabric portal:" -ForegroundColor White
Write-Host "    https://app.fabric.microsoft.com/groups/$WorkspaceId/synapsenotebooks/$notebookId" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Next steps:" -ForegroundColor White
Write-Host "    1. Click 'Run all' to execute one polling cycle now, OR wait for the 15-min schedule." -ForegroundColor White
Write-Host "    2. For production scheduling, create a Data Factory pipeline that runs the notebook at the source's native cadence." -ForegroundColor White
