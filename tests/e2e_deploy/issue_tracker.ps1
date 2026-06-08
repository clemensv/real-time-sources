<#
.SYNOPSIS
    Files or amends GitHub issues for E2E validation failures.

.DESCRIPTION
    Creates a new issue if no open issue with the same title pattern exists.
    Appends a comment to the existing issue if one is found (deduplication).

.PARAMETER Source
    The source name (e.g. "noaa-ndbc").

.PARAMETER Target
    The deployment target: "azure" or "fabric".

.PARAMETER ErrorMessage
    Description of the failure.

.PARAMETER SessionId
    The session timestamp identifier.

.PARAMETER Repo
    GitHub repository (default: clemensv/real-time-sources).

.PARAMETER Label
    Issue label (default: e2e-validation).
#>
param(
    [Parameter(Mandatory)][string]$Source,
    [Parameter(Mandatory)][ValidateSet("azure","fabric")][string]$Target,
    [Parameter(Mandatory)][string]$ErrorMessage,
    [Parameter(Mandatory)][string]$SessionId,
    [string]$Repo = "clemensv/real-time-sources",
    [string]$Label = "e2e-validation"
)

$ErrorActionPreference = "Stop"

$titlePattern = "[E2E] $Source - $Target"

# Search for existing open issue with same title
$existingIssues = gh issue list --repo $Repo --label $Label --state open --search "`"$titlePattern`"" --json number,title | ConvertFrom-Json

$matchingIssue = $existingIssues | Where-Object { $_.title -eq $titlePattern } | Select-Object -First 1

if ($matchingIssue) {
    # Amend: add a comment
    $comment = @"
## Session: $SessionId

**Error**: $ErrorMessage

_Appended by E2E validation runner._
"@
    gh issue comment $matchingIssue.number --repo $Repo --body $comment
    Write-Host "Amended issue #$($matchingIssue.number): $titlePattern"
    return @{ action = "amended"; number = $matchingIssue.number }
}
else {
    # Create new issue
    $body = @"
## E2E Validation Failure

**Source**: ``$Source``
**Target**: $Target
**Session**: $SessionId

### Error

$ErrorMessage

---
_Filed automatically by the E2E validation runner._
"@
    $result = gh issue create --repo $Repo --title $titlePattern --body $body --label $Label | Out-String
    $issueNumber = if ($result -match '#(\d+)') { $Matches[1] } elseif ($result -match '/issues/(\d+)') { $Matches[1] } else { "unknown" }
    Write-Host "Created issue #$issueNumber`: $titlePattern"
    return @{ action = "created"; number = $issueNumber }
}
