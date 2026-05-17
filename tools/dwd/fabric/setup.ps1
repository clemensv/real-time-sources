<#
.SYNOPSIS
    DWD-specific Fabric setup. Layers DWD KQL assets, the dwd_ingest Spark
    notebook, and a Spark Notebook destination on top of the basic per-source
    setup produced by tools/deploy-fabric/deploy-fabric.ps1.

.DESCRIPTION
    Assumes deploy-fabric.ps1 has already been run for the DWD source and
    therefore:
      * The Fabric workspace + Eventhouse exist.
      * A KQL database (default name 'dwd') exists with a _cloudevents_dispatch
        landing table receiving DWD CloudEvents via the 'dwd-ingest' Eventstream.

    This script:
      1. Applies tools/dwd/fabric/dwd.kql to the KQL database (typed tables,
         update policies, materialized views, CogCatalog gold table, and the
         map.* KQL functions consumed by Fabric Maps vector layers).
      2. Resolves the default Lakehouse in the workspace (or one passed via
         -LakehouseName) so the dwd_ingest notebook can write to its Files
         section.
      3. Generates dwd_ingest.ipynb from notebook/build_notebook.py.
      4. Calls tools/deploy-fabric/deploy-fabric-notebook.ps1 to upload the
         notebook into the workspace bound to the KQL database (parameters cell
         is patched with KUSTO_URI / KUSTO_DATABASE / LAKEHOUSE_PATH).
      5. Adds the notebook as a 'Notebook' destination on the existing
         dwd-ingest Eventstream (preview feature) so the stream is consumed
         as a Spark Structured Streaming source.

.PARAMETER WorkspaceId
    Fabric workspace ID (GUID) — same one used by deploy-fabric.ps1.

.PARAMETER EventhouseId
    Fabric Eventhouse ID (GUID) — same one used by deploy-fabric.ps1.

.PARAMETER DatabaseName
    KQL database name. Default 'dwd'.

.PARAMETER EventStreamName
    Eventstream display name produced by deploy-fabric.ps1. Default 'dwd-ingest'.

.PARAMETER LakehouseName
    Display name of the Lakehouse where bronze/gold files are written. If not
    provided, the first Lakehouse in the workspace is used.

.PARAMETER NotebookName
    Display name for the uploaded notebook. Default 'dwd_ingest'.

.PARAMETER SkipNotebook
    Skip notebook upload and Eventstream destination wiring (KQL only).

.EXAMPLE
    ./setup.ps1 `
        -WorkspaceId  "c98acd97-4363-4296-8323-b6ab21e53903" `
        -EventhouseId "dbfd2819-2879-4ae7-bff2-95619ad7b8e7"
#>

param(
    [Parameter(Mandatory = $true)] [string] $WorkspaceId,
    [Parameter(Mandatory = $true)] [string] $EventhouseId,
    [string] $DatabaseName    = "dwd",
    [string] $EventStreamName = "dwd-ingest",
    [string] $LakehouseName,
    [string] $NotebookName    = "dwd_ingest",
    [switch] $SkipNotebook
)

$ErrorActionPreference = "Stop"
$ScriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot   = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $ScriptDir))
$FabricApi  = "https://api.fabric.microsoft.com/v1"
$StreamName = "$EventStreamName-stream"

function Invoke-FabricApi {
    param([string]$Method, [string]$Url, [object]$Body)
    $azArgs = @("rest", "--method", $Method, "--url", $Url, "--resource", "https://api.fabric.microsoft.com")
    if ($Body) {
        $bodyFile = Join-Path $env:TEMP "fab_$(Get-Random).json"
        $json = if ($Body -is [string]) { $Body } else { $Body | ConvertTo-Json -Depth 30 -Compress }
        [System.IO.File]::WriteAllText($bodyFile, $json, [System.Text.UTF8Encoding]::new($false))
        $azArgs += @("--body", "@$bodyFile", "--headers", "Content-Type=application/json")
    }
    $result = & az @azArgs 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Fabric API $Method $Url failed: $($result | Out-String)" }
    if ($result) { return $result | ConvertFrom-Json }
    return $null
}

function Invoke-KqlScript {
    param([string]$QueryUri, [string]$Database, [string]$ScriptPath)
    Write-Host "  Applying $(Split-Path -Leaf $ScriptPath)..." -ForegroundColor Yellow
    $scriptText = Get-Content -Path $ScriptPath -Raw
    $body = @{ csl = ".execute database script <|`n$scriptText"; db = $Database }
    $bodyFile = Join-Path $env:TEMP "kql_$(Get-Random).json"
    [System.IO.File]::WriteAllText($bodyFile, ($body | ConvertTo-Json -Compress), [System.Text.UTF8Encoding]::new($false))
    $result = az rest --method POST --url "$QueryUri/v1/rest/mgmt" --resource $QueryUri `
        --body "@$bodyFile" --headers "Content-Type=application/json" 2>&1
    if ($LASTEXITCODE -ne 0) { throw "KQL script failed for $ScriptPath`n$result" }
    $parsed = $result | ConvertFrom-Json
    $rows = @()
    if ($parsed.Tables.Count -gt 0) { $rows = $parsed.Tables[0].Rows }
    $failed = @($rows | Where-Object { $_[3] -ne "Completed" })
    if ($failed.Count -gt 0) { throw "KQL script reported failures for $ScriptPath" }
    Write-Host "    Completed." -ForegroundColor Green
}

Write-Host "=== DWD Fabric Extension Setup ===" -ForegroundColor Cyan
Write-Host "  WorkspaceId   = $WorkspaceId"
Write-Host "  EventhouseId  = $EventhouseId"
Write-Host "  DatabaseName  = $DatabaseName"
Write-Host "  EventStream   = $EventStreamName"
Write-Host "  Notebook      = $NotebookName"

# Resolve eventhouse + database
Write-Host "`n[1/4] Resolving Eventhouse + KQL database..." -ForegroundColor Yellow
$eh       = Invoke-FabricApi GET "$FabricApi/workspaces/$WorkspaceId/eventhouses/$EventhouseId"
$queryUri = $eh.properties.queryServiceUri
$dbList   = Invoke-FabricApi GET "$FabricApi/workspaces/$WorkspaceId/kqlDatabases"
$db       = $dbList.value | Where-Object { $_.displayName -eq $DatabaseName } | Select-Object -First 1
if (-not $db) { throw "KQL database '$DatabaseName' not found. Run tools/deploy-fabric/deploy-fabric.ps1 first." }
Write-Host "  Eventhouse: $($eh.displayName)"
Write-Host "  Database:   $($db.displayName) ($($db.id))"

# Apply DWD KQL
Write-Host "`n[2/4] Applying DWD KQL assets..." -ForegroundColor Yellow
Invoke-KqlScript -QueryUri $queryUri -Database $DatabaseName -ScriptPath (Join-Path $ScriptDir "dwd.kql")

if ($SkipNotebook) {
    Write-Host "`n=== Done (KQL only, -SkipNotebook). ===" -ForegroundColor Cyan
    return
}

# Resolve Lakehouse
Write-Host "`n[3/4] Resolving Lakehouse..." -ForegroundColor Yellow
$lhList = Invoke-FabricApi GET "$FabricApi/workspaces/$WorkspaceId/lakehouses"
if ($LakehouseName) {
    $lh = $lhList.value | Where-Object { $_.displayName -eq $LakehouseName } | Select-Object -First 1
} else {
    $lh = $lhList.value | Select-Object -First 1
}
if (-not $lh) { throw "No Lakehouse found in workspace; create one or pass -LakehouseName." }
$lakehousePath = "abfss://$WorkspaceId@onelake.dfs.fabric.microsoft.com/$($lh.id)"
Write-Host "  Lakehouse:  $($lh.displayName) ($($lh.id))"
Write-Host "  Path:       $lakehousePath"

# Build the notebook from build_notebook.py and upload via the shared script.
Write-Host "`n[4/4] Building + uploading notebook..." -ForegroundColor Yellow
$nbDir  = Join-Path $ScriptDir "notebook"
$nbPath = Join-Path $nbDir    "dwd_ingest.ipynb"
$build  = Join-Path $nbDir    "build_notebook.py"
python $build
if (-not (Test-Path $nbPath)) { throw "build_notebook.py did not produce $nbPath" }

# Patch LAKEHOUSE_PATH directly in the parameters cell — the shared
# deploy-fabric-notebook.ps1 only patches KUSTO_URI / KUSTO_DATABASE.
$nbJson = Get-Content -LiteralPath $nbPath -Raw -Encoding UTF8
$nbObj  = $nbJson | ConvertFrom-Json
foreach ($cell in $nbObj.cells) {
    if ($cell.cell_type -ne 'code' -or -not $cell.metadata.tags -or ($cell.metadata.tags -notcontains 'parameters')) { continue }
    $newLines = foreach ($line in @($cell.source)) {
        if ($line -match '^\s*LAKEHOUSE_PATH\s*=') { "LAKEHOUSE_PATH       = `"$lakehousePath`"`n" }
        else { $line }
    }
    $cell.source = @($newLines)
    break
}
[System.IO.File]::WriteAllText($nbPath, ($nbObj | ConvertTo-Json -Depth 50), [System.Text.UTF8Encoding]::new($false))

$deployScript = Join-Path $RepoRoot "tools\deploy-fabric\deploy-fabric-notebook.ps1"
& pwsh -NoLogo -NoProfile -File $deployScript `
    -Source       "dwd" `
    -Workspace    $WorkspaceId `
    -Eventhouse   $EventhouseId `
    -DatabaseName $DatabaseName `
    -NotebookName $NotebookName `
    -NotebookPath $nbPath
if ($LASTEXITCODE -ne 0) { throw "deploy-fabric-notebook.ps1 failed (exit $LASTEXITCODE)" }

# Wire the notebook as a Spark Notebook destination on the existing eventstream.
Write-Host "`n[5/5] Adding Notebook destination to Eventstream '$EventStreamName'..." -ForegroundColor Yellow
$esList = Invoke-FabricApi GET "$FabricApi/workspaces/$WorkspaceId/eventstreams"
$es     = $esList.value | Where-Object { $_.displayName -eq $EventStreamName } | Select-Object -First 1
if (-not $es) { throw "Eventstream '$EventStreamName' not found. Run tools/deploy-fabric/deploy-fabric.ps1 first." }
$nbList = Invoke-FabricApi GET "$FabricApi/workspaces/$WorkspaceId/notebooks"
$nbItem = $nbList.value | Where-Object { $_.displayName -eq $NotebookName } | Select-Object -First 1
if (-not $nbItem) { throw "Notebook '$NotebookName' missing after upload." }

$defResp = Invoke-FabricApi POST "$FabricApi/workspaces/$WorkspaceId/eventstreams/$($es.id)/getDefinition"
$part    = $defResp.definition.parts | Where-Object { $_.path -eq 'eventstream.json' } | Select-Object -First 1
if (-not $part) { throw "Eventstream definition missing eventstream.json part." }
$esDef   = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($part.payload)) | ConvertFrom-Json

$existingDest = $esDef.destinations | Where-Object { $_.name -eq 'dwd-ingest-notebook' }
if ($existingDest) {
    Write-Host "  Notebook destination already present — leaving as-is." -ForegroundColor DarkYellow
} else {
    $notebookDest = [pscustomobject]@{
        name       = "dwd-ingest-notebook"
        type       = "Notebook"
        properties = [pscustomobject]@{
            workspaceId = $WorkspaceId
            itemId      = $nbItem.id
        }
        inputNodes = @([pscustomobject]@{ name = $StreamName })
    }
    $esDef.destinations = @($esDef.destinations) + @($notebookDest)

    $updateJson = $esDef | ConvertTo-Json -Depth 30
    $payloadB64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($updateJson))
    try {
        Invoke-FabricApi POST "$FabricApi/workspaces/$WorkspaceId/eventstreams/$($es.id)/updateDefinition" -Body @{
            definition = @{
                parts = @(@{ path = "eventstream.json"; payload = $payloadB64; payloadType = "InlineBase64" })
            }
        } | Out-Null
        Write-Host "  Notebook destination added." -ForegroundColor Green
    } catch {
        # The Spark Notebook destination is a preview Eventstream feature (Dec 2025)
        # that is not yet available in every tenant / region. When the API rejects
        # the destination type, fall back to the KQL-source pattern: the notebook
        # reads from the _cloudevents_dispatch table via the Kusto Spark connector
        # (which is what the other feeders, e.g. eurowater/pugetsound, do).
        Write-Warning ("Could not add Spark Notebook destination to Eventstream " +
            "(preview feature may be unavailable in this tenant): $($_.Exception.Message)")
        Write-Warning ("Fallback: run the notebook '$NotebookName' on a schedule " +
            "or via a Data Activator rule; it will consume from the KQL table " +
            "'_cloudevents_dispatch' in database '$DatabaseName'.")
    }
}

Write-Host "`n=== DWD Fabric Extension Complete ===" -ForegroundColor Cyan
Write-Host "  KQL database:        $DatabaseName ($($db.id))"
Write-Host "  Lakehouse:           $($lh.displayName) ($($lh.id))"
Write-Host "  Notebook:            $NotebookName"
Write-Host "  Eventstream:         $EventStreamName"
Write-Host ""
Write-Host "Open the Eventstream in the Fabric portal, then Publish to start the"
Write-Host "Spark Notebook destination. The notebook will drain DWD events and write"
Write-Host "bronze/gold files to the Lakehouse + CogCatalog rows to KQL."
