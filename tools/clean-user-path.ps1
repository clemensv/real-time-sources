<#
.SYNOPSIS
    Removes user-scoped PATH entries that already exist in the machine-scoped PATH.

.DESCRIPTION
    This script compares the user-scoped PATH and machine-scoped PATH environment variables.
    Any entries in the user-scoped PATH that are also present in the machine-scoped PATH will be removed from the user scope.

.NOTES
    This script requires PowerShell to run with sufficient privileges to modify user environment variables.
    It does not require Administrator privileges, as it only modifies the user scope.

.EXAMPLE
    ./Clean-UserPath.ps1
#>

# Get the machine-scoped and user-scoped PATH environment variables
$machinePath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine) -split ";"
$userPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::User) -split ";"

# Find all elements in the user PATH that are also present in the machine PATH
$cleanedUserPath = $userPath | Where-Object { $_ -and -not ($machinePath -contains $_) }

# Join the cleaned user path back into a single string
$updatedUserPath = ($cleanedUserPath -join ";").TrimEnd(";")

# Set the new user PATH
[System.Environment]::SetEnvironmentVariable("Path", $updatedUserPath, [System.EnvironmentVariableTarget]::User)

# Output the result
Write-Host "User PATH cleaned. Redundant entries removed."
Write-Host "Updated user PATH: $updatedUserPath"
