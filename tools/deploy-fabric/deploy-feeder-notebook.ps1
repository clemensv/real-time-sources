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
    Azure subscription ID or name used by Stage A.

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
    Bridge polling interval in seconds. If not specified, the value from the
    notebook's checked-in parameters cell is preserved.

.PARAMETER OnceMode
    If $true, the bridge exits after one polling cycle. If $false, the bridge
    loops continuously. If not specified, the value from the notebook's
    checked-in parameters cell is preserved.

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
    [int]$PollingInterval = -1,
    [string]$OnceMode = "",

    # Extra source-specific parameter overrides patched into the notebook's
    # 'parameters'-tagged cell (e.g. @{ FIRMS_MAP_KEY = '...' }). Use this for
    # feeder secrets/keys supplied at deploy time so they are never committed
    # to the notebook in the repo.
    [hashtable]$NotebookParam = @{},

    [string]$EnvironmentName,
    [switch]$SkipEnvironment,
    [switch]$BuildWheelsLocally,
    [string]$WheelsBundleUrl,

    [string]$DefaultLakehouse,
    [int]$ScheduleIntervalMinutes = 15,
    [switch]$NoSchedule,
    [switch]$NoTriggerNow,

    # Upstream secrets / env vars to inject into the notebook's parameters
    # cell at deploy time (e.g. ENTSOE_SECURITY_TOKEN=...). Each entry is a
    # KEY=VALUE string and may be specified multiple times. Values are written
    # into the deployed notebook (os.environ[...]) but are never committed to
    # the repo. Use this instead of hand-editing the notebook for sources that
    # require an upstream API token.
    [string[]]$EnvVar,

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
if (-not $EnvironmentName)         { $EnvironmentName = "feeder_env" }

$repoRoot     = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$notebookPath = Join-Path $repoRoot "feeders/$Source/notebook/$Source-feed.ipynb"
if (-not (Test-Path $notebookPath)) {
    # Cloud Shell / standalone usage: only the helper scripts were downloaded,
    # not the full repo. Try to fetch the notebook from GitHub raw.
    $rawNbUrl = "https://raw.githubusercontent.com/$Repo/$Branch/feeders/$Source/notebook/$Source-feed.ipynb"
    $localNb  = Join-Path $TempDir "$Source-feed_$(Get-Random).ipynb"
    Write-Host "Notebook not in working tree; downloading from $rawNbUrl" -ForegroundColor DarkYellow
    try {
        Invoke-WebRequest -Uri $rawNbUrl -OutFile $localNb -UseBasicParsing -ErrorAction Stop
        $notebookPath = $localNb
    } catch {
        throw "Notebook not found locally and could not be downloaded from $rawNbUrl. " +
              "Source '$Source' may not have a Fabric notebook published yet (expected " +
              "feeders/$Source/notebook/$Source-feed.ipynb in the repo). Underlying error: $($_.Exception.Message)"
    }
}

function Write-Step { param([string]$Step, [string]$Msg) Write-Host "`n[$Step] $Msg" -ForegroundColor Yellow }
function Write-OK   { param([string]$Msg) Write-Host "  $Msg" -ForegroundColor Green }
function Write-Info { param([string]$Msg) Write-Host "  $Msg" -ForegroundColor DarkYellow }

function ConvertFrom-AzCliJson {
    param(
        [AllowNull()]
        [object]$InputObject,
        [string]$Context = "Azure CLI output"
    )

    if ($null -eq $InputObject) { return $null }

    $text = if ($InputObject -is [string]) {
        $InputObject
    } else {
        $InputObject | Out-String
    }

    $trimmed = $text.Trim()
    if (-not $trimmed) { return $null }

    try {
        return $trimmed | ConvertFrom-Json
    } catch {
        # az rest sometimes prepends WARNING:/INFO: lines ahead of JSON.
        $jsonStarts = [regex]::Matches($trimmed, '(?m)^[\t ]*[\{\[]')
        foreach ($match in $jsonStarts) {
            $candidate = $trimmed.Substring($match.Index).Trim()
            try {
                return $candidate | ConvertFrom-Json
            } catch {
                continue
            }
        }
    }

    throw "Failed to parse JSON from $Context. Raw output:`n$trimmed"
}

function Resolve-AzSubscriptionContext {
    param(
        [Parameter(Mandatory = $true)] [string]$Subscription,
        [switch]$SkipSet
    )

    if (-not $SkipSet) {
        az account set --subscription $Subscription --only-show-errors 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to set subscription '$Subscription' (name or ID)."
        }
    }

    $account = az account show --only-show-errors --output json 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to resolve the active Azure subscription after selecting '$Subscription': $($account | Out-String)"
    }

    $parsed = ConvertFrom-AzCliJson -InputObject $account -Context "az account show output for subscription '$Subscription'"
    if ($Subscription -and $parsed.id -ine $Subscription -and $parsed.name -ine $Subscription) {
        throw "Active Azure subscription '$($parsed.name)' ($($parsed.id)) does not match requested subscription '$Subscription'."
    }

    return [pscustomobject]@{
        Id   = $parsed.id
        Name = $parsed.name
    }
}

function Invoke-FabricApi {
    param([string]$Method, [string]$Url, [object]$Body)
    $azArgs = @("rest", "--method", $Method, "--url", $Url, "--resource", "https://api.fabric.microsoft.com", "--only-show-errors", "--output", "json")
    if ($Body) {
        $bodyFile = Join-Path $TempDir "fabric_body_$(Get-Random).json"
        $json = if ($Body -is [string]) { $Body } else { $Body | ConvertTo-Json -Depth 30 -Compress }
        [System.IO.File]::WriteAllText($bodyFile, $json, [System.Text.UTF8Encoding]::new($false))
        $azArgs += @("--body", "@$bodyFile", "--headers", "Content-Type=application/json")
    }
    $result = & az @azArgs 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Fabric API error ($Method $Url): $($result | Out-String)" }
    if ($result) { return ConvertFrom-AzCliJson -InputObject $result -Context "Fabric API response ($Method $Url)" }
    return $null
}

function Invoke-FabricApiRaw {
    # Same as Invoke-FabricApi, but returns the raw response (so 202 LROs can be inspected).
    param([string]$Method, [string]$Url, [object]$Body)
    $azArgs = @("rest", "--method", $Method, "--url", $Url, "--resource", "https://api.fabric.microsoft.com", "--only-show-errors", "--output", "json")
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

    $srcDir = Join-Path $RepoRoot "feeders/$Source"
    if (-not (Test-Path $srcDir)) { throw "Source folder not found: $srcDir" }

    $producerRoot = Join-Path $srcDir "$($Source -replace '-', '_')_producer"
    if (-not (Test-Path $producerRoot)) { throw "Generated producer folder not found: $producerRoot. Run generate_producer.ps1 first." }

    $outDir = Join-Path $TempDir "feeder-wheels-$Source-$(Get-Random)"
    New-Item -ItemType Directory -Force -Path $outDir | Out-Null

    # Build the producer sub-packages first (each is a self-contained poetry project),
    # then the top-level source bridge package(s) which reference them via path-deps.
    $subPackages = Get-ChildItem -Directory $producerRoot |
        Where-Object { Test-Path (Join-Path $_.FullName "pyproject.toml") } |
        ForEach-Object { $_.FullName }

    # For multi-transport sources (no top-level pyproject.toml), find all buildable
    # sub-packages (_core, _kafka, _mqtt, _amqp) with pyproject.toml in the source dir.
    if (Test-Path (Join-Path $srcDir "pyproject.toml")) {
        $bridgePackages = @($srcDir)
    } else {
        $bridgePackages = Get-ChildItem -Directory $srcDir |
            Where-Object { (Test-Path (Join-Path $_.FullName "pyproject.toml")) -and ($_.Name -notlike "*_producer*") } |
            ForEach-Object { $_.FullName }
        if (-not $bridgePackages) { throw "No buildable packages found in $srcDir (no pyproject.toml at root or in subdirs)" }
    }
    $toBuild = @($subPackages) + @($bridgePackages)

    foreach ($pkgDir in $toBuild) {
        Write-Info "  pip wheel $($pkgDir | Split-Path -Leaf)"
        & python -m pip wheel --no-deps --no-build-isolation --wheel-dir $outDir $pkgDir 2>&1 | Out-Host
        if ($LASTEXITCODE -ne 0) { throw "pip wheel failed for $pkgDir" }
    }

    $wheels = Get-ChildItem -LiteralPath $outDir -Filter *.whl
    if (-not $wheels) { throw "No wheels produced in $outDir" }

    $stripper = Join-Path $PSScriptRoot "strip-wheel-pathdeps.py"
    & python $stripper --stamp-version @($wheels | ForEach-Object { $_.FullName }) | Out-Host
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
    If the library already exists (400), delete it first and retry.
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
        $statusCode = 0
        if ($_.Exception.Response) { $statusCode = [int]$_.Exception.Response.StatusCode }
        if ($statusCode -eq 400) {
            # Library likely already exists — delete and retry
            $delUrl = "$url/$($Wheel.Name)"
            try {
                Invoke-WebRequest -Uri $delUrl -Method Delete `
                    -Headers @{ Authorization = "Bearer $Token" } `
                    -UseBasicParsing -ErrorAction Stop | Out-Null
                Write-Info "    (replaced existing $($Wheel.Name))"
            } catch {
                # DELETE failed — maybe different error format; try encoded name
                $encodedName = [System.Uri]::EscapeDataString($Wheel.Name)
                $delUrl2 = "$url/$encodedName"
                try {
                    Invoke-WebRequest -Uri $delUrl2 -Method Delete `
                        -Headers @{ Authorization = "Bearer $Token" } `
                        -UseBasicParsing -ErrorAction Stop | Out-Null
                } catch {}
            }
            # Retry upload
            $resp2 = Invoke-WebRequest -Uri $url -Method Post `
                -Headers @{ Authorization = "Bearer $Token" } `
                -Form @{ file = $Wheel } `
                -UseBasicParsing -ErrorAction Stop
            return $resp2.StatusCode
        }
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
$pollingDisplay = if ($PollingInterval -eq -1) { "(from notebook)" } else { "$PollingInterval s" }
$onceDisplay = if ($OnceMode -eq "") { "(from notebook)" } else { "once-mode=$OnceMode" }
Write-Host "  Polling interval: $pollingDisplay ($onceDisplay)" -ForegroundColor White

# ── Stage A: Fabric infra (Eventhouse + KQL DB + Event Stream) ────────────
# The notebook resolves the Event Stream connection string at runtime via
# the Topology API using its workspace/user identity, so Stage A only needs
# to ensure the Fabric infra exists. No connection string is required here.
if (-not $SkipInfra) {
    Write-Step "A" "Setting up Fabric infra via deploy-fabric.ps1..."
    $deployFabric = Join-Path $PSScriptRoot "deploy-fabric.ps1"
    if (-not (Test-Path $deployFabric)) {
        # Script was likely fetched standalone (e.g. into Cloud Shell). Pull
        # the sibling deploy-fabric.ps1 from the same repo/branch.
        $rawDfUrl = "https://raw.githubusercontent.com/$Repo/$Branch/tools/deploy-fabric/deploy-fabric.ps1"
        $deployFabric = Join-Path $TempDir "deploy-fabric.ps1"
        Write-Host "deploy-fabric.ps1 not alongside script; downloading from $rawDfUrl" -ForegroundColor DarkYellow
        try {
            Invoke-WebRequest -Uri $rawDfUrl -OutFile $deployFabric -UseBasicParsing
        } catch {
            throw "deploy-fabric.ps1 not found alongside this script and could not be downloaded from $rawDfUrl. Error: $($_.Exception.Message)"
        }
    }

    $fwdArgs = @{
        Source        = $Source
        Workspace     = $Workspace
        Eventhouse    = $Eventhouse
        DatabaseName  = $DatabaseName
        Repo          = $Repo
        Branch        = $Branch
    }
    if ($SubscriptionId) { $fwdArgs['SubscriptionId'] = $SubscriptionId }

    & $deployFabric @fwdArgs
    if ($LASTEXITCODE -ne 0) {
        throw "deploy-fabric.ps1 failed; aborting notebook deploy."
    }
}

# ── Stage B: Resolve workspace + KQL DB ───────────────────────────────────
Write-Step "B/1" "Resolving Fabric workspace..."
if ($SubscriptionId -and -not $SkipInfra) {
    $selectedSubscription = Resolve-AzSubscriptionContext -Subscription $SubscriptionId -SkipSet
    $SubscriptionId = $selectedSubscription.Id
    Write-OK "Subscription set: $($selectedSubscription.Name) ($SubscriptionId)"
} elseif ($SubscriptionId) {
    $selectedSubscription = Resolve-AzSubscriptionContext -Subscription $SubscriptionId
    $SubscriptionId = $selectedSubscription.Id
    Write-OK "Subscription set: $($selectedSubscription.Name) ($SubscriptionId)"
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

Write-Step "B/2" "Resolving Eventhouse and KQL database..."
$ehList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses"
$eh = $ehList.value | Where-Object { $_.displayName -eq $Eventhouse -or $_.id -eq $Eventhouse } | Select-Object -First 1
if (-not $eh) {
    if ($Eventhouse -match '^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$') {
        throw "Eventhouse with id '$Eventhouse' not found in workspace (cannot auto-create by GUID)."
    }
    Write-Host "  Creating Eventhouse '$Eventhouse'..." -ForegroundColor Yellow
    Invoke-FabricApi -Method POST -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses" -Body @{ displayName = $Eventhouse } | Out-Null
    for ($i = 0; $i -lt 12 -and -not $eh; $i++) {
        Start-Sleep -Seconds 5
        $ehList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses"
        $eh = $ehList.value | Where-Object { $_.displayName -eq $Eventhouse } | Select-Object -First 1
    }
    if (-not $eh) { throw "Failed to create Eventhouse '$Eventhouse'." }
}
$ehDetails = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses/$($eh.id)"
for ($i = 0; $i -lt 6 -and (-not $ehDetails -or -not $ehDetails.properties.queryServiceUri); $i++) {
    Start-Sleep -Seconds 5
    $ehDetails = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/eventhouses/$($eh.id)"
}
if ($ehDetails) { $eh = $ehDetails }
Write-OK "Eventhouse: $($eh.displayName) ($($eh.id))"

$dbList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases"
$db = $dbList.value | Where-Object { $_.displayName -eq $DatabaseName } | Select-Object -First 1
if (-not $db) {
    Write-Host "  Creating KQL database '$DatabaseName'..." -ForegroundColor Yellow
    $dbProps = @{ databaseType = "ReadWrite"; parentEventhouseItemId = $eh.id; oneLakeCachingPeriod = "P36500D"; oneLakeStandardStoragePeriod = "P36500D" }
    try {
        Invoke-FabricApi -Method POST -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases" -Body @{ displayName = $DatabaseName; creationPayload = $dbProps } | Out-Null
    } catch {
        if ($_.Exception.Message -match 'ItemDisplayNameAlreadyInUse|409') {
            Write-Host "  Database '$DatabaseName' already exists (auto-created with Eventhouse); waiting for it to appear..." -ForegroundColor Yellow
        } else { throw }
    }
    for ($i = 0; $i -lt 24 -and -not $db; $i++) {
        Start-Sleep -Seconds 5
        $dbList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/kqlDatabases"
        $db = $dbList.value | Where-Object { $_.displayName -eq $DatabaseName } | Select-Object -First 1
    }
    if (-not $db) { throw "Failed to create KQL database '$DatabaseName'." }
}
Write-OK "KQL database: $($db.displayName) ($($db.id))"

$queryUri = $eh.properties.queryServiceUri

# ── Stage B/2.1: Apply KQL schema ────────────────────────────────────────
# Find and apply the source's .kql schema script. This ensures tables exist
# regardless of whether -SkipInfra was used (Stage A is the only other path
# that applies schema, via deploy-fabric.ps1).
$kqlFile = $null
$kqlCandidates = @(
    (Join-Path $repoRoot "feeders/$Source/kql/$($Source -replace '-','_').kql"),
    (Join-Path $repoRoot "feeders/$Source/kql/$Source.kql")
)
foreach ($c in $kqlCandidates) {
    if (Test-Path $c) { $kqlFile = $c; break }
}
if ($kqlFile) {
    Write-Step "B/2.1" "Applying KQL schema ($([System.IO.Path]::GetFileName($kqlFile)))..."
    $kqlContent = Get-Content -LiteralPath $kqlFile -Raw -Encoding UTF8
    $kqlBody = @{
        csl = ".execute database script <|`n$kqlContent"
        db  = $db.displayName
    }
    $kqlBodyFile = Join-Path $TempDir "kql_schema_$(Get-Random).json"
    [System.IO.File]::WriteAllText(
        $kqlBodyFile,
        ($kqlBody | ConvertTo-Json -Compress),
        [System.Text.UTF8Encoding]::new($false)
    )
    $kqlAttempts = 3
    $kqlApplied = $false
    for ($ka = 1; $ka -le $kqlAttempts; $ka++) {
        $kqlResult = az rest `
            --method POST `
            --url "$queryUri/v1/rest/mgmt" `
            --resource $queryUri `
            --body "@$kqlBodyFile" `
            --headers "Content-Type=application/json" `
            --only-show-errors `
            --output json 2>&1
        if ($LASTEXITCODE -eq 0) {
            $kqlApplied = $true
            break
        }
        if ($ka -lt $kqlAttempts) {
            Write-Host "  Schema apply attempt $ka failed; retrying in 15s..." -ForegroundColor DarkYellow
            Start-Sleep -Seconds 15
        }
    }
    if ($kqlApplied) {
        Write-OK "KQL schema applied."
    } else {
        Write-Warning "KQL schema apply failed after $kqlAttempts attempts. Tables may be missing.`n$kqlResult"
    }
    Remove-Item -LiteralPath $kqlBodyFile -ErrorAction SilentlyContinue
} else {
    Write-Step "B/2.1" "No KQL schema found — skipping"
}

# ── Stage B/2.5: Build wheels and upload to Lakehouse Files ──────────────
# Python notebooks cannot bind Fabric Environments; dependencies are loaded
# at runtime via `%pip install /lakehouse/default/Files/wheels/<source>/*.whl`.
# We upload the built wheels to the feeder_state_lake Lakehouse that is already
# bound as the default Lakehouse for state/log storage.
if (-not $SkipEnvironment) {
    Write-Step "B/2.5" "Building source wheels and uploading to Lakehouse Files..."

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

    # We need the Lakehouse ID for OneLake upload. Resolve it early (the same
    # Lakehouse is bound to the notebook later in Stage B/3).
    $lakehouseList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/lakehouses"
    $lhForWheels = $null
    if ($DefaultLakehouse) {
        $lhForWheels = $lakehouseList.value | Where-Object { $_.displayName -eq $DefaultLakehouse -or $_.id -eq $DefaultLakehouse } | Select-Object -First 1
    } elseif ($lakehouseList.value.Count -eq 1) {
        $lhForWheels = $lakehouseList.value[0]
    } elseif ($lakehouseList.value.Count -gt 1) {
        $lhForWheels = $lakehouseList.value | Where-Object { $_.displayName -eq 'feeder_state_lake' } | Select-Object -First 1
        if (-not $lhForWheels) { $lhForWheels = $lakehouseList.value[0] }
    } else {
        $newLakehouseName = 'feeder_state_lake'
        Write-Info "Workspace has no Lakehouse; creating '$newLakehouseName'..."
        $createBody = @{ displayName = $newLakehouseName } | ConvertTo-Json
        $lhForWheels = Invoke-FabricApi -Method POST -Url "$FabricApi/workspaces/$WorkspaceId/lakehouses" -Body $createBody
        if (-not $lhForWheels -or -not $lhForWheels.id) {
            Start-Sleep -Seconds 5
            $lakehouseList = Invoke-FabricApi -Method GET -Url "$FabricApi/workspaces/$WorkspaceId/lakehouses"
            $lhForWheels = $lakehouseList.value | Where-Object { $_.displayName -eq $newLakehouseName } | Select-Object -First 1
        }
        if (-not $lhForWheels) { throw "Failed to create Lakehouse for wheel storage." }
    }
    $LakehouseId = $lhForWheels.id
    Write-Info "Using Lakehouse '$($lhForWheels.displayName)' ($LakehouseId) for wheel storage."

    # Upload wheels to OneLake: Files/wheels/<source>/<wheel>.whl
    $oneLakeDfs = "https://onelake.dfs.fabric.microsoft.com"
    # OneLake DFS requires the storage audience token, not the Fabric API token
    $oneLakeToken = (az account get-access-token --resource https://storage.azure.com --query accessToken -o tsv 2>&1)
    if ($LASTEXITCODE -ne 0) { throw "Failed to acquire OneLake token: $oneLakeToken" }
    $oneLakeToken = ($oneLakeToken | Out-String).Trim()
    $wheelsDir = "wheels/$Source"

    # Create the directory (PUT with resource=directory)
    $dirUrl = "$oneLakeDfs/$WorkspaceId/$LakehouseId/Files/$wheelsDir`?resource=directory"
    try {
        Invoke-RestMethod -Method PUT -Uri $dirUrl -Headers @{ Authorization = "Bearer $oneLakeToken" } -ErrorAction Stop | Out-Null
    } catch {
        # 409 = already exists, that's fine
        if ($_.Exception.Response.StatusCode.value__ -ne 409) { throw }
    }

    foreach ($w in $wheels) {
        $fileUrl = "$oneLakeDfs/$WorkspaceId/$LakehouseId/Files/$wheelsDir/$($w.Name)"
        Write-Info "  uploading $($w.Name) to OneLake..."
        # OneLake DFS: Create file then append+flush
        $createUrl = "$fileUrl`?resource=file"
        Invoke-RestMethod -Method PUT -Uri $createUrl -Headers @{ Authorization = "Bearer $oneLakeToken" } -ErrorAction Stop | Out-Null
        $content = [System.IO.File]::ReadAllBytes($w.FullName)
        $appendUrl = "$fileUrl`?position=0&action=append"
        Invoke-RestMethod -Method PATCH -Uri $appendUrl -Headers @{ Authorization = "Bearer $oneLakeToken"; "Content-Type" = "application/octet-stream" } -Body $content -ErrorAction Stop | Out-Null
        $flushUrl = "$fileUrl`?position=$($content.Length)&action=flush"
        Invoke-RestMethod -Method PATCH -Uri $flushUrl -Headers @{ Authorization = "Bearer $oneLakeToken" } -ErrorAction Stop | Out-Null
        Write-Info "    -> uploaded ($($content.Length) bytes)"
    }

    # Also upload PyPI dependency wheels (avro, dataclasses_json) that the
    # generated producer_data package needs but doesn't declare. The notebook's
    # %pip install cell handles these from PyPI directly, so no upload needed.
    Write-OK "Wheels uploaded to Lakehouse Files/$wheelsDir/"
}

# ── Stage B/3: Patch notebook ─────────────────────────────────────────────
Write-Step "B/3" "Patching notebook parameters + KQL/Environment binding..."
$nbJson = Get-Content -LiteralPath $notebookPath -Raw -Encoding UTF8
$nb = $nbJson | ConvertFrom-Json

# ── Read checked-in POLLING_INTERVAL and ONCE_MODE from the notebook when
#    the user didn't explicitly pass them on the command line. This ensures
#    the deploy script respects the source-specific cadence committed in the
#    notebook (set by the notebook-retrofit workflow).
if ($PollingInterval -eq -1 -or $OnceMode -eq "") {
    foreach ($cell in $nb.cells) {
        if ($cell.cell_type -ne 'code') { continue }
        $tags = @()
        if ($cell.metadata -and $cell.metadata.tags) { $tags = @($cell.metadata.tags) }
        if ($tags -notcontains 'parameters') { continue }
        $srcLines = @($cell.source) | ForEach-Object { $_ }
        foreach ($line in $srcLines) {
            if ($PollingInterval -eq -1 -and $line -match '^\s*POLLING_INTERVAL\s*=\s*(\d+)') {
                $PollingInterval = [int]$matches[1]
            }
            if ($OnceMode -eq "" -and $line -match '^\s*ONCE_MODE\s*=\s*(True|False)') {
                $OnceMode = $matches[1]
            }
        }
        break
    }
    # Fallback if notebook doesn't declare the values
    if ($PollingInterval -eq -1) { $PollingInterval = 900 }
    if ($OnceMode -eq "") { $OnceMode = "True" }
}
# Normalize OnceMode to bool for downstream logic
if ($OnceMode -is [string]) {
    $OnceModeFlag = $OnceMode -eq "True"
} else {
    $OnceModeFlag = [bool]$OnceMode
}

Write-Host "  Resolved cadence: POLLING_INTERVAL=$PollingInterval, ONCE_MODE=$(if ($OnceModeFlag) { 'True' } else { 'False' })" -ForegroundColor DarkGray

if (-not $nb.metadata)              { $nb | Add-Member -NotePropertyName metadata     -NotePropertyValue ([pscustomobject]@{}) -Force }
if (-not $nb.metadata.dependencies) { $nb.metadata | Add-Member -NotePropertyName dependencies -NotePropertyValue ([pscustomobject]@{}) -Force }

# Force the pure-Python (jupyter_python) notebook kernel regardless of what the
# committed .ipynb declares. Feeder notebooks are single-node Python pollers and
# do no distributed Spark compute; the Python runtime is cheaper and faster to
# start. Dependencies are loaded via %pip install from Lakehouse Files at runtime.
$nb.metadata | Add-Member -NotePropertyName kernelspec -NotePropertyValue ([pscustomobject]@{
    name         = 'jupyter_python'
    display_name = 'Python (Jupyter)'
    language     = 'python'
}) -Force
$nb.metadata | Add-Member -NotePropertyName language_info -NotePropertyValue ([pscustomobject]@{ name = 'python' }) -Force
if (-not $nb.metadata.microsoft) { $nb.metadata | Add-Member -NotePropertyName microsoft -NotePropertyValue ([pscustomobject]@{}) -Force }
$nb.metadata.microsoft | Add-Member -NotePropertyName language       -NotePropertyValue 'python'         -Force
$nb.metadata.microsoft | Add-Member -NotePropertyName language_group -NotePropertyValue 'jupyter_python' -Force
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
    $newLakehouseName = 'feeder_state_lake'
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

# Python notebooks do not support Environment binding. Dependencies are loaded
# via %pip install from Lakehouse Files at runtime (see the pip install cell in
# each notebook). No environment metadata is needed.

$onceLiteral = if ($OnceModeFlag) { "True" } else { "False" }

$paramsPatched = $false
foreach ($cell in $nb.cells) {
    if ($cell.cell_type -ne 'code') { continue }
    $tags = @()
    if ($cell.metadata -and $cell.metadata.tags) { $tags = @($cell.metadata.tags) }
    if ($tags -notcontains 'parameters') { continue }

    $srcLines = @($cell.source) | ForEach-Object { $_ }
    $newLines = foreach ($line in $srcLines) {
        $ovName = $null
        if ($line -match '^\s*([A-Za-z_]\w*)\s*=') {
            $cand = $matches[1]
            if ($NotebookParam.ContainsKey($cand)) { $ovName = $cand }
        }
        if     ($ovName)                                 { "{0,-16} = `"{1}`"`n" -f $ovName, $NotebookParam[$ovName] }
        elseif ($line -match '^\s*EVENTSTREAM_NAME\s*=') { "EVENTSTREAM_NAME = `"$Source-ingest`"`n" }
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
    if ($EnvVar -and $EnvVar.Count -gt 0) {
        $envInjection = @("`n", "import os as _os  # injected by deploy-feeder-notebook.ps1 -EnvVar (not committed)`n")
        foreach ($kv in $EnvVar) {
            $eq = $kv.IndexOf('=')
            if ($eq -lt 1) { throw "-EnvVar entries must be 'KEY=VALUE'; got '$kv'." }
            $k = $kv.Substring(0, $eq).Trim()
            $v = $kv.Substring($eq + 1)
            $vEsc = ($v -replace '\\', '\\\\') -replace '"', '\"'
            $envInjection += "_os.environ[`"$k`"] = `"$vEsc`"`n"
        }
        $cell.source = @($newLines) + $envInjection
        Write-OK ("Injected {0} env var(s) into parameters cell: {1}" -f $EnvVar.Count, (($EnvVar | ForEach-Object { ($_ -split '=', 2)[0] }) -join ', '))
    }
    $paramsPatched = $true
    break
}
if (-not $paramsPatched) { throw "Notebook has no 'parameters'-tagged cell to patch." }
Write-OK "Parameters cell patched."

$tmpNb = Join-Path $TempDir "$Source`_feed_$(Get-Random).ipynb"
[System.IO.File]::WriteAllText($tmpNb, ($nb | ConvertTo-Json -Depth 50), [System.Text.UTF8Encoding]::new($false))

# ── Stage B/4: Upload notebook in Fabric-native .py format ────────────────
# Fabric ignores the standard Jupyter kernelspec in .ipynb uploads and defaults
# to synapse_pyspark. To guarantee the pure-Python (jupyter) kernel we convert
# the patched ipynb to Fabric's internal notebook-content.py format which has
# META blocks that Fabric DOES respect.
Write-Step "B/4" "Uploading notebook to Fabric workspace (native .py format)..."

# --- Convert ipynb cells to Fabric notebook-content.py ---
$pyLines = [System.Collections.Generic.List[string]]::new()
$pyLines.Add("# Fabric notebook source")
$pyLines.Add("")

# METADATA block: kernel_info + dependencies
$metaObj = [ordered]@{
    kernel_info  = [ordered]@{
        name               = 'jupyter'
        jupyter_kernel_name = 'python3.11'
    }
    dependencies = [ordered]@{}
}
# Transfer dependencies from ipynb metadata
if ($nb.metadata.dependencies) {
    if ($nb.metadata.dependencies.lakehouse) {
        $lhDep = $nb.metadata.dependencies.lakehouse
        $metaObj.dependencies['lakehouse'] = [ordered]@{
            default_lakehouse              = $lhDep.default_lakehouse
            default_lakehouse_name         = $lhDep.default_lakehouse_name
            default_lakehouse_workspace_id = $lhDep.default_lakehouse_workspace_id
        }
    }
    $metaObj.dependencies['environment'] = @{}
    if ($nb.metadata.dependencies.kqlDatabases) {
        $kqlDbs = @($nb.metadata.dependencies.kqlDatabases | ForEach-Object {
            [ordered]@{ name = $_.name; displayName = $_.displayName; workspaceId = $_.workspaceId; itemId = $_.itemId }
        })
        $metaObj.dependencies['kqlDatabases'] = $kqlDbs
    }
}
$metaJson = $metaObj | ConvertTo-Json -Depth 10
$pyLines.Add("# METADATA ********************")
$pyLines.Add("")
foreach ($mLine in ($metaJson -split "`n")) {
    $pyLines.Add("# META $($mLine.TrimEnd())")
}
$pyLines.Add("")

# Convert each cell
foreach ($cell in $nb.cells) {
    $cellSource = ($cell.source -join '').TrimEnd()

    if ($cell.cell_type -eq 'markdown') {
        $pyLines.Add("# MARKDOWN ********************")
        $pyLines.Add("")
        foreach ($mdLine in ($cellSource -split "`n")) {
            $pyLines.Add("# $($mdLine.TrimEnd())")
        }
        $pyLines.Add("")
    } elseif ($cell.cell_type -eq 'code') {
        # Check if this is the parameters cell
        $isParams = $false
        if ($cell.metadata -and $cell.metadata.tags) {
            $isParams = @($cell.metadata.tags) -contains 'parameters'
        }
        if ($isParams) {
            $pyLines.Add("# PARAMETERS CELL ********************")
        } else {
            $pyLines.Add("# CELL ********************")
        }
        $pyLines.Add("")
        foreach ($codeLine in ($cellSource -split "`n")) {
            $pyLines.Add($codeLine.TrimEnd())
        }
        $pyLines.Add("")
        # Cell-level metadata
        $cellMeta = [ordered]@{
            language       = 'python'
            language_group = 'jupyter_python'
        }
        $cellMetaJson = $cellMeta | ConvertTo-Json -Depth 5
        $pyLines.Add("")
        $pyLines.Add("# METADATA ********************")
        $pyLines.Add("")
        foreach ($cmLine in ($cellMetaJson -split "`n")) {
            $pyLines.Add("# META $($cmLine.TrimEnd())")
        }
        $pyLines.Add("")
    }
}

$pyContent = ($pyLines -join "`n")
$pyBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($pyContent))

# .platform part
$platformObj = [ordered]@{
    '$schema' = 'https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json'
    metadata  = [ordered]@{ type = 'Notebook'; displayName = $NotebookName }
    config    = [ordered]@{ version = '2.0'; logicalId = '00000000-0000-0000-0000-000000000000' }
}
$platformJson = $platformObj | ConvertTo-Json -Depth 5
$platformBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($platformJson))

$definition = @{
    parts = @(
        @{ path = "notebook-content.py"; payload = $pyBase64; payloadType = "InlineBase64" }
        @{ path = ".platform"; payload = $platformBase64; payloadType = "InlineBase64" }
    )
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
    # For continuous-mode notebooks (ONCE_MODE=False), the notebook runs for
    # RUN_DURATION seconds (~55 min). Schedule every 60 min so the next run
    # starts shortly after the previous one exits. For once-mode notebooks,
    # use the configured ScheduleIntervalMinutes (default 15).
    $effectiveScheduleMin = [int]$ScheduleIntervalMinutes
    if (-not $OnceModeFlag) {
        # Read RUN_DURATION from the notebook to compute schedule interval
        $runDuration = 3300
        foreach ($cell in $nb.cells) {
            if ($cell.cell_type -ne 'code') { continue }
            $tags = @()
            if ($cell.metadata -and $cell.metadata.tags) { $tags = @($cell.metadata.tags) }
            if ($tags -notcontains 'parameters') { continue }
            $srcLines = @($cell.source) | ForEach-Object { $_ }
            foreach ($line in $srcLines) {
                if ($line -match '^\s*RUN_DURATION\s*=\s*(\d+)') {
                    $runDuration = [int]$matches[1]
                }
            }
            break
        }
        # Schedule = RUN_DURATION + 5 min buffer, rounded up to nearest minute
        $effectiveScheduleMin = [int][math]::Ceiling(($runDuration + 300) / 60)
        # Fabric scheduler minimum is 5 minutes
        if ($effectiveScheduleMin -lt 5) { $effectiveScheduleMin = 5 }
    }
    Write-Step "B/5b" "Creating recurring schedule (every $effectiveScheduleMin min)..."
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
                interval         = $effectiveScheduleMin
                startDateTime    = $startDt
                endDateTime      = $endDt
                localTimeZoneId  = "UTC"
            }
        }
        $schedResp = Invoke-FabricApiRaw -Method POST `
            -Url "$FabricApi/workspaces/$WorkspaceId/items/$notebookId/jobs/RunNotebook/schedules" `
            -Body $schedBody
        if ($schedResp.ExitCode -eq 0) {
            Write-OK "Schedule created (every $effectiveScheduleMin min UTC)."
        } else {
            Write-Warning "Could not create schedule (create it manually from the portal):`n$($schedResp.Body)"
        }
    }
}

Write-Host "`n=== Notebook Feeder Deployment Complete ===" -ForegroundColor Cyan
Write-Host "  Notebook:     $NotebookName ($notebookId)" -ForegroundColor Gray
Write-Host "  Workspace:    $($wsInfo.displayName) ($WorkspaceId)" -ForegroundColor Gray
Write-Host "  KQL Database: $($db.displayName) ($($db.id))" -ForegroundColor Gray
if ($LakehouseId) {
    Write-Host "  Wheels:       Files/wheels/$Source/ (Lakehouse)" -ForegroundColor Gray
}
Write-Host "  State path:   $StatePath  (Lakehouse Files)" -ForegroundColor Gray
Write-Host ""
Write-Host "  Open in Fabric portal:" -ForegroundColor White
Write-Host "    https://app.fabric.microsoft.com/groups/$WorkspaceId/synapsenotebooks/$notebookId" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Next steps:" -ForegroundColor White
Write-Host "    1. Click 'Run all' to execute one polling cycle now, OR wait for the 15-min schedule." -ForegroundColor White
Write-Host "    2. For production scheduling, create a Data Factory pipeline that runs the notebook at the source's native cadence." -ForegroundColor White
