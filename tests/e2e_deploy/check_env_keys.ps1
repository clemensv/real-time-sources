<#
.SYNOPSIS
    Checks whether required source-specific environment variables/API keys are set.

.DESCRIPTION
    Returns a hashtable with:
      - missing: array of env var names that are required but not set
      - present: array of env var names that are set
    
    If no keys are required for the source, returns $null.

.PARAMETER Source
    Source directory name (e.g. "aisstream").

.PARAMETER Target
    Deployment target: "azure" or "fabric".
#>
param(
    [Parameter(Mandatory)][string]$Source,
    [string]$Target = "azure"
)

# Map of sources to their required environment variables.
# Only sources that need external API keys or credentials beyond what
# the ARM template self-provisions (e.g. Event Hubs connection strings)
# need entries here.
$requiredKeys = @{
    "aisstream"     = @("AISSTREAM_API_KEY")
    "bluesky"       = @()  # no key needed (public firehose)
    "entsoe"        = @("ENTSOE_SECURITY_TOKEN")
    "billetto"      = @("BILLETTO_API_KEYPAIR")
    "nasa-firms"    = @("FIRMS_MAP_KEY")
    "uk-bods-siri"  = @("BODS_API_KEY")
}

$keys = $requiredKeys[$Source]
if ($null -eq $keys -or $keys.Count -eq 0) {
    return $null
}

$missing = @()
$present = @()
foreach ($k in $keys) {
    $val = [System.Environment]::GetEnvironmentVariable($k)
    if ([string]::IsNullOrWhiteSpace($val)) {
        $missing += $k
    } else {
        $present += $k
    }
}

if ($missing.Count -eq 0) {
    return $null
}

return @{ missing = $missing; present = $present }
