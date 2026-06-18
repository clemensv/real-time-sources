param(
    [Parameter(Mandatory = $true)]
    [hashtable] $Context
)

$ErrorActionPreference = "Stop"

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

function Invoke-AzRestJson {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,
        [string]$Context = "az rest"
    )

    $raw = & az @Arguments 2>&1
    return ConvertFrom-AzCliJson -InputObject $raw -Context $Context
}

function Resolve-PythonCommand {
    foreach ($candidate in @("python", "py")) {
        $cmd = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($null -ne $cmd) {
            return $cmd.Source
        }
    }

    throw "Python is required to wire the siri Fabric Map but was not found on PATH."
}

function Get-KustoAccessToken {
    param(
        [Parameter(Mandatory = $true)]
        [string]$KustoUri
    )

    $resources = @(
        "https://kusto.kusto.windows.net",
        $KustoUri
    ) | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique

    foreach ($resource in $resources) {
        $token = az account get-access-token --resource $resource --query accessToken -o tsv 2>$null
        if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($token)) {
            return $token.Trim()
        }
    }

    throw "Failed to acquire a Kusto access token for $KustoUri."
}

if (-not $Context.WorkspaceId) {
    throw "Context.WorkspaceId is required."
}
if (-not $Context.DatabaseId) {
    throw "Context.DatabaseId is required."
}
if (-not $Context.DatabaseName) {
    throw "Context.DatabaseName is required."
}
if (-not $Context.EventhouseClusterUri) {
    throw "Context.EventhouseClusterUri is required."
}

$mapName = if ($env:SIRI_FABRIC_MAP_NAME) { $env:SIRI_FABRIC_MAP_NAME } else { "siri-map" }
$existingMapId = if ($env:SIRI_FABRIC_MAP_ID) { $env:SIRI_FABRIC_MAP_ID } else { $null }

if (-not $existingMapId) {
    Write-Host "=== siri post-deploy: ensuring Fabric Map '$mapName' ==="
    $items = Invoke-AzRestJson -Arguments @(
        "rest",
        "--method", "GET",
        "--url", "https://api.fabric.microsoft.com/v1/workspaces/$($Context.WorkspaceId)/items?type=Map",
        "--resource", "https://api.fabric.microsoft.com",
        "--only-show-errors",
        "--output", "json"
    ) -Context "listing Fabric Map items"

    if ($items.value) {
        $match = $items.value | Where-Object { $_.displayName -eq $mapName } | Select-Object -First 1
        if ($match) {
            $existingMapId = $match.id
            Write-Host "Reusing existing Fabric Map '$mapName' ($existingMapId)"
        }
    }
}

if (-not $existingMapId) {
    Write-Host "Creating Fabric Map '$mapName'"
    $body = @{
        displayName = $mapName
        type = "Map"
    } | ConvertTo-Json -Depth 10 -Compress
    $bodyFile = Join-Path ([System.IO.Path]::GetTempPath()) ("siri-map-create-{0}.json" -f ([Guid]::NewGuid().ToString("N")))
    Set-Content -Path $bodyFile -Value $body -Encoding utf8NoBOM

    try {
        $null = Invoke-AzRestJson -Arguments @(
            "rest",
            "--method", "POST",
            "--url", "https://api.fabric.microsoft.com/v1/workspaces/$($Context.WorkspaceId)/items",
            "--resource", "https://api.fabric.microsoft.com",
            "--headers", "Content-Type=application/json",
            "--body", "@$bodyFile",
            "--only-show-errors",
            "--output", "json"
        ) -Context "creating Fabric Map item"
    } finally {
        Remove-Item $bodyFile -ErrorAction SilentlyContinue
    }

    for ($attempt = 0; $attempt -lt 30 -and -not $existingMapId; $attempt++) {
        Start-Sleep -Seconds 2
        $items = Invoke-AzRestJson -Arguments @(
            "rest",
            "--method", "GET",
            "--url", "https://api.fabric.microsoft.com/v1/workspaces/$($Context.WorkspaceId)/items?type=Map",
            "--resource", "https://api.fabric.microsoft.com",
            "--only-show-errors",
            "--output", "json"
        ) -Context "listing Fabric Map items after create"
        $match = $items.value | Where-Object { $_.displayName -eq $mapName } | Select-Object -First 1
        if ($match) {
            $existingMapId = $match.id
        }
    }

    if (-not $existingMapId) {
        throw "Fabric Map creation for '$mapName' did not surface an item id after 60 seconds."
    }

    Write-Host "Created Fabric Map '$mapName' ($existingMapId)"
}

$python = Resolve-PythonCommand
$wireScript = Join-Path $PSScriptRoot "wire_siri_map.py"
if (-not (Test-Path $wireScript)) {
    throw "Expected wiring script at $wireScript"
}

$fabricToken = az account get-access-token --resource https://api.fabric.microsoft.com --query accessToken -o tsv
if (-not $fabricToken) {
    throw "Failed to acquire a Fabric API access token from Azure CLI."
}

$kustoToken = Get-KustoAccessToken -KustoUri $Context.EventhouseClusterUri

$env:FABRIC_TOKEN = $fabricToken
$env:KUSTO_TOKEN = $kustoToken

try {
    & $python $wireScript `
        --workspace-id $Context.WorkspaceId `
        --map-id $existingMapId `
        --kql-db-id $Context.DatabaseId `
        --kql-db-name $Context.DatabaseName `
        --kusto-uri $Context.EventhouseClusterUri `
        --map-name $mapName

    if ($LASTEXITCODE -ne 0) {
        throw "wire_siri_map.py failed with exit code $LASTEXITCODE"
    }
} catch {
    Write-Warning "Map wiring failed (non-fatal): $($_.Exception.Message)"
    Write-Warning "Core SIRI notebook/Event Stream/KQL deployment remains successful; rerun feeders/siri/fabric/post-deploy.ps1 to retry the Fabric Map wiring."
    $global:LASTEXITCODE = 0
} finally {
    Remove-Item Env:FABRIC_TOKEN -ErrorAction SilentlyContinue
    Remove-Item Env:KUSTO_TOKEN -ErrorAction SilentlyContinue
}
