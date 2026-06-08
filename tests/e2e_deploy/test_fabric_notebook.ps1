<#
.SYNOPSIS
    Runs E2E validation for a single source on Microsoft Fabric (Notebook + KQL).

.DESCRIPTION
    1. Deploys notebook via deploy-feeder-notebook.ps1
    2. Triggers a notebook run via Fabric REST API
    3. Waits for completion
    4. Queries KQL for row counts
    5. Checks Map/Dashboard items (if present)
    6. Cleans up all Fabric items

.PARAMETER Source
    Source directory name (e.g. "noaa-ndbc").

.PARAMETER SessionDir
    Path to the session directory for logging results.

.PARAMETER WorkspaceName
    Fabric workspace name.

.PARAMETER WorkspaceId
    Fabric workspace ID.

.PARAMETER Token
    Fabric bearer token.

.PARAMETER TimeoutSeconds
    Max seconds to wait for notebook completion (default: 900).

.PARAMETER MinKqlRows
    Minimum KQL rows expected (default: 1).
#>
param(
    [Parameter(Mandatory)][string]$Source,
    [Parameter(Mandatory)][string]$SessionDir,
    [Parameter(Mandatory)][string]$WorkspaceName,
    [Parameter(Mandatory)][string]$WorkspaceId,
    [Parameter(Mandatory)][string]$Token,
    [int]$TimeoutSeconds = 900,
    [int]$MinKqlRows = 1
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = (Resolve-Path "$scriptDir/../..").Path
$sourceDir = Join-Path $repoRoot "feeders" $Source
$sessionId = Split-Path -Leaf $SessionDir

$headers = @{
    "Authorization" = "Bearer $Token"
    "Content-Type"  = "application/json"
}
$fabricBase = "https://api.fabric.microsoft.com/v1"

# Validate source has a notebook
$notebookDir = Join-Path $sourceDir "notebook"
if (-not (Test-Path $notebookDir)) {
    Write-Warning "Source '$Source' has no notebook/ directory — skipping Fabric test."
    return @{ result = "skip"; reason = "no-notebook" }
}

Write-Host "=== Fabric E2E: $Source ===" -ForegroundColor Cyan

$result = @{
    source = $Source
    target = "fabric"
    result = "fail"
    steps = @{}
    kql_rows = 0
    error = $null
    notebook_id = $null
}

try {
    # Step 1: Deploy notebook
    Write-Host "[1/6] Deploying notebook..."
    $deployScript = Join-Path $repoRoot "tools/deploy-fabric/deploy-feeder-notebook.ps1"
    & $deployScript -Source $Source -WorkspaceName $WorkspaceName -Once
    $result.steps["notebook_deployed"] = $true

    # Find the notebook item ID
    $items = Invoke-RestMethod -Uri "$fabricBase/workspaces/$WorkspaceId/items?type=Notebook" -Headers $headers -Method Get
    $notebook = $items.value | Where-Object { $_.displayName -match $Source } | Select-Object -First 1
    if (-not $notebook) {
        throw "Notebook for '$Source' not found in workspace after deployment"
    }
    $result.notebook_id = $notebook.id
    Write-Host "  Notebook ID: $($notebook.id)"

    # Step 2: Trigger notebook run
    Write-Host "[2/6] Triggering notebook run..."
    $runResponse = Invoke-RestMethod `
        -Uri "$fabricBase/workspaces/$WorkspaceId/items/$($notebook.id)/jobs/instances?jobType=RunNotebook" `
        -Headers $headers `
        -Method Post
    $result.steps["run_triggered"] = $true

    # Get the job instance location from response headers or poll
    $jobLocation = $runResponse # May need to parse Location header

    # Step 3: Wait for completion
    Write-Host "[3/6] Waiting for notebook completion (timeout: ${TimeoutSeconds}s)..."
    $startTime = Get-Date
    $completed = $false
    $jobStatus = "Unknown"

    while (((Get-Date) - $startTime).TotalSeconds -lt $TimeoutSeconds) {
        Start-Sleep -Seconds 30
        try {
            $statusResponse = Invoke-RestMethod `
                -Uri "$fabricBase/workspaces/$WorkspaceId/items/$($notebook.id)/jobs/instances?jobType=RunNotebook" `
                -Headers $headers `
                -Method Get
            $latestJob = $statusResponse.value | Sort-Object -Property startTimeUtc -Descending | Select-Object -First 1
            if ($latestJob) {
                $jobStatus = $latestJob.status
                Write-Host "  Job status: $jobStatus"
                if ($jobStatus -in @("Completed", "Failed", "Cancelled")) {
                    $completed = $true
                    break
                }
            }
        }
        catch {
            Write-Host "  Status poll error: $($_.Exception.Message)" -ForegroundColor Yellow
        }
    }

    if (-not $completed) {
        throw "Notebook did not complete within ${TimeoutSeconds}s (last status: $jobStatus)"
    }
    if ($jobStatus -ne "Completed") {
        throw "Notebook run failed with status: $jobStatus"
    }
    $result.steps["run_completed"] = $true

    # Step 4: Query KQL for row counts
    Write-Host "[4/6] Querying KQL for data..."
    # Find the KQL database for this source
    $kqlDatabases = Invoke-RestMethod -Uri "$fabricBase/workspaces/$WorkspaceId/items?type=KQLDatabase" -Headers $headers -Method Get
    $sourceDb = $kqlDatabases.value | Where-Object { $_.displayName -match $Source } | Select-Object -First 1

    if ($sourceDb) {
        # Get the query URI from database properties
        $dbProps = Invoke-RestMethod -Uri "$fabricBase/workspaces/$WorkspaceId/items/$($sourceDb.id)" -Headers $headers -Method Get
        $queryUri = $dbProps.properties.queryUri

        if ($queryUri) {
            # Query dispatch table
            $kqlBody = @{ db = $sourceDb.displayName; csl = "_cloudevents_dispatch | count" } | ConvertTo-Json
            $kqlHeaders = @{ "Authorization" = "Bearer $Token"; "Content-Type" = "application/json" }
            try {
                $kqlResult = Invoke-RestMethod -Uri "$queryUri/v1/rest/query" -Headers $kqlHeaders -Method Post -Body $kqlBody
                $rowCount = $kqlResult.Tables[0].Rows[0][0]
                $result.kql_rows = [int]$rowCount
                Write-Host "  _cloudevents_dispatch rows: $rowCount"

                if ($rowCount -ge $MinKqlRows) {
                    $result.steps["kql_dispatch_rows"] = $true
                }
                else {
                    throw "KQL dispatch table has $rowCount rows (expected >= $MinKqlRows)"
                }
            }
            catch {
                Write-Host "  KQL query error: $($_.Exception.Message)" -ForegroundColor Yellow
                throw "KQL query failed: $($_.Exception.Message)"
            }

            # Query typed tables
            $tablesBody = @{ db = $sourceDb.displayName; csl = ".show tables | where TableName != '_cloudevents_dispatch' | project TableName" } | ConvertTo-Json
            try {
                $tablesResult = Invoke-RestMethod -Uri "$queryUri/v1/rest/query" -Headers $kqlHeaders -Method Post -Body $tablesBody
                $tables = $tablesResult.Tables[0].Rows | ForEach-Object { $_[0] }
                $typedTableHasRows = $false
                foreach ($table in $tables) {
                    $countBody = @{ db = $sourceDb.displayName; csl = "['$table'] | count" } | ConvertTo-Json
                    $countResult = Invoke-RestMethod -Uri "$queryUri/v1/rest/query" -Headers $kqlHeaders -Method Post -Body $countBody
                    $tCount = [int]$countResult.Tables[0].Rows[0][0]
                    if ($tCount -gt 0) {
                        Write-Host "  Table '$table': $tCount rows" -ForegroundColor Green
                        $typedTableHasRows = $true
                        break
                    }
                }
                if ($typedTableHasRows) {
                    $result.steps["typed_tables_rows"] = $true
                }
                else {
                    Write-Host "  No typed tables have rows" -ForegroundColor Yellow
                }
            }
            catch {
                Write-Host "  Typed table query error: $($_.Exception.Message)" -ForegroundColor Yellow
            }
        }
    }
    else {
        Write-Host "  No KQL database found for $Source" -ForegroundColor Yellow
    }

    # Step 5: Check Map/Dashboard items
    Write-Host "[5/6] Checking Map/Dashboard items..."
    $allItems = Invoke-RestMethod -Uri "$fabricBase/workspaces/$WorkspaceId/items" -Headers $headers -Method Get
    $mapItems = $allItems.value | Where-Object { $_.type -eq "Map" -and $_.displayName -match $Source }
    $dashItems = $allItems.value | Where-Object { $_.type -eq "Dashboard" -and $_.displayName -match $Source }

    if ($mapItems) {
        Write-Host "  Map item found: $($mapItems[0].displayName)"
        $result.steps["map_verified"] = $true
    }
    else {
        $result.steps["map_verified"] = "n/a"
    }

    if ($dashItems) {
        Write-Host "  Dashboard item found: $($dashItems[0].displayName)"
        $result.steps["dashboard_verified"] = $true
    }
    else {
        $result.steps["dashboard_verified"] = "n/a"
    }

    # Mark pass if dispatch table has rows
    if ($result.steps["kql_dispatch_rows"]) {
        $result.result = "pass"
    }
}
catch {
    $result.error = $_.Exception.Message
    Write-Host "FAIL: $($_.Exception.Message)" -ForegroundColor Red

    # File issue
    & "$scriptDir/issue_tracker.ps1" `
        -Source $Source `
        -Target fabric `
        -ErrorMessage $_.Exception.Message `
        -SessionId $sessionId `
        -Repo "clemensv/real-time-sources"
}
finally {
    # Step 6: Cleanup
    Write-Host "[6/6] Cleaning up Fabric items..."
    try {
        # Delete the notebook
        if ($result.notebook_id) {
            Invoke-RestMethod -Uri "$fabricBase/workspaces/$WorkspaceId/items/$($result.notebook_id)" -Headers $headers -Method Delete -ErrorAction SilentlyContinue
            Write-Host "  Deleted notebook"
        }
        $result.steps["cleanup"] = $true
    }
    catch {
        Write-Host "  Cleanup warning: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

# Write result
$resultFile = Join-Path $SessionDir "$Source-fabric-result.json"
$result | ConvertTo-Json -Depth 5 | Set-Content $resultFile
Write-Host "Result: $($result.result)" -ForegroundColor $(if ($result.result -eq "pass") { "Green" } else { "Red" })

return $result
