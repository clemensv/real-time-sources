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
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..\..")).Path
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
    & $deployScript -Source $Source -Workspace $WorkspaceName -OnceMode "True" -BuildWheelsLocally -NoSchedule
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

    # Step 4: Validate KQL data (reusable module)
    # Wait for EventStream → KQL ingestion pipeline to flush (typically 60-120s latency)
    Write-Host "[4/6] Waiting 120s for EventStream ingestion before querying KQL..."
    Start-Sleep -Seconds 120
    Write-Host "[4/6] Validating KQL data..."
    # Fabric REST needs api.fabric.microsoft.com audience; Kusto REST needs kusto.kusto.windows.net audience
    $kustoToken = az account get-access-token --resource "https://kusto.kusto.windows.net" --query accessToken --output tsv
    $validateKqlPath = Join-Path $repoRoot ".github/skills/e2e-deployment-validation/references/validate_kql.ps1"
    $kqlValidation = & $validateKqlPath `
        -Source $Source `
        -WorkspaceId $WorkspaceId `
        -Token $Token `
        -KustoToken $kustoToken `
        -MinRows $MinKqlRows

    $result.kql_rows = $kqlValidation.dispatch_count
    if ($kqlValidation.dispatch_count -ge $MinKqlRows) {
        $result.steps["kql_dispatch_rows"] = $true
    }
    if ($kqlValidation.typed_tables.Values | Where-Object { $_ -gt 0 }) {
        $result.steps["typed_tables_rows"] = $true
    }
    if ($kqlValidation.errors.Count -gt 0) {
        Write-Host "  KQL errors: $($kqlValidation.errors -join '; ')" -ForegroundColor Yellow
    }

    # Step 5: Validate Map/Dashboard items (reusable module)
    Write-Host "[5/6] Validating Map/Dashboard items..."
    $validateMapPath = Join-Path $repoRoot ".github/skills/e2e-deployment-validation/references/validate_map.ps1"
    $mapValidation = & $validateMapPath `
        -Source $Source `
        -WorkspaceId $WorkspaceId `
        -Token $Token `
        -QueryUri $kqlValidation.query_uri `
        -DatabaseName $kqlValidation.database_name

    if ($null -eq $mapValidation.pass) {
        $result.steps["map_verified"] = "n/a"
    }
    elseif ($mapValidation.pass) {
        $result.steps["map_verified"] = $true
    }
    else {
        $result.steps["map_verified"] = $false
    }
    $result.steps["dashboard_verified"] = "n/a"  # Dashboards checked via same workspace scan

    # Mark pass if dispatch table has rows and typed tables have data
    if ($kqlValidation.pass) {
        $result.result = "pass"
    }
}
catch {
    $result.error = $_.Exception.Message
    Write-Host "FAIL: $($_.Exception.Message)" -ForegroundColor Red

    # File issue
    & (Join-Path $scriptDir "issue_tracker.ps1") `
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
