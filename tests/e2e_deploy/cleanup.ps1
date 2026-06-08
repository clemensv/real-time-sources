<#
.SYNOPSIS
    Failsafe cleanup for E2E validation resources.

.DESCRIPTION
    Finds and deletes any leftover E2E resource groups and Fabric items
    that may remain from interrupted or failed test runs.

.PARAMETER Subscription
    Azure subscription name or ID.

.PARAMETER WorkspaceId
    Fabric workspace ID (optional — skips Fabric cleanup if not provided).

.PARAMETER Token
    Fabric bearer token (optional — required for Fabric cleanup).

.PARAMETER Prefix
    Resource group prefix to match (default: "e2e-").

.PARAMETER DryRun
    If set, lists resources without deleting them.
#>
param(
    [string]$Subscription,
    [string]$WorkspaceId,
    [string]$Token,
    [string]$Prefix = "e2e-",
    [switch]$DryRun
)

$ErrorActionPreference = "Continue"

Write-Host "=== E2E Cleanup ===" -ForegroundColor Cyan

# --- Azure Resource Groups ---
if ($Subscription) {
    Write-Host "`nAzure: Finding resource groups with prefix '$Prefix'..."
    $rgs = az group list --subscription $Subscription --query "[?starts_with(name, '$Prefix')].{name:name, location:location}" --output json | ConvertFrom-Json

    if ($rgs.Count -eq 0) {
        Write-Host "  No matching resource groups found." -ForegroundColor Green
    }
    else {
        foreach ($rg in $rgs) {
            if ($DryRun) {
                Write-Host "  [DRY RUN] Would delete: $($rg.name) ($($rg.location))" -ForegroundColor Yellow
            }
            else {
                Write-Host "  Deleting: $($rg.name)..."
                az group delete --name $rg.name --subscription $Subscription --yes --no-wait
                Write-Host "  Deletion initiated for $($rg.name)" -ForegroundColor Green
            }
        }
    }
}
else {
    Write-Host "Azure: Skipped (no subscription provided)"
}

# --- Fabric Items ---
if ($WorkspaceId -and $Token) {
    Write-Host "`nFabric: Finding E2E items in workspace..."
    $headers = @{
        "Authorization" = "Bearer $Token"
        "Content-Type"  = "application/json"
    }
    $fabricBase = "https://api.fabric.microsoft.com/v1"

    try {
        $items = Invoke-RestMethod -Uri "$fabricBase/workspaces/$WorkspaceId/items" -Headers $headers -Method Get
        # Look for items that might be E2E leftovers (notebooks with e2e in name or created recently)
        $e2eItems = $items.value | Where-Object {
            $_.displayName -match "^e2e-" -or $_.displayName -match "-e2e$"
        }

        if ($e2eItems.Count -eq 0) {
            Write-Host "  No E2E items found in workspace." -ForegroundColor Green
        }
        else {
            foreach ($item in $e2eItems) {
                if ($DryRun) {
                    Write-Host "  [DRY RUN] Would delete: $($item.displayName) ($($item.type))" -ForegroundColor Yellow
                }
                else {
                    Write-Host "  Deleting: $($item.displayName) ($($item.type))..."
                    Invoke-RestMethod -Uri "$fabricBase/workspaces/$WorkspaceId/items/$($item.id)" -Headers $headers -Method Delete -ErrorAction SilentlyContinue
                    Write-Host "  Deleted $($item.displayName)" -ForegroundColor Green
                }
            }
        }
    }
    catch {
        Write-Host "  Fabric API error: $($_.Exception.Message)" -ForegroundColor Red
    }
}
else {
    Write-Host "Fabric: Skipped (no workspace ID or token provided)"
}

Write-Host "`nCleanup complete." -ForegroundColor Cyan
