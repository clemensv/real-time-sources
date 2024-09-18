<#
.SYNOPSIS
    Automates the installation of Kusto CLI by installing the Microsoft.Azure.Kusto.Tools package and extracting the required files.

.DESCRIPTION
    This script installs the Kusto CLI by downloading and extracting the Microsoft.Azure.Kusto.Tools package.
    For Windows PowerShell, it uses the net472 version of the CLI tool.
    For PowerShell 7+, it uses the net6.0 version.

.NOTES
    Elevated privileges (run as Administrator) are not required unless permissions are needed to modify the PATH.

.EXAMPLE
    ./Install-KustoCLI.ps1
#>


# Step 0: Check if Kusto CLI is already installed and available
if (Get-Command kusto.cli -ErrorAction SilentlyContinue) {
    Write-Host "Kusto CLI is already installed. Exiting..."
    exit 0
}

# Ensure NuGet provider is available for Install-Package
Write-Host "Checking for the NuGet package provider..."
$nugetProvider = Get-PackageProvider -Name "NuGet" -ErrorAction SilentlyContinue

if (-not $nugetProvider) {
    Write-Host "NuGet provider not found. Installing NuGet provider..."
    Install-PackageProvider -Name "NuGet" -Force -Scope CurrentUser
}

# Step 1: Install Kusto CLI via Install-Package
Write-Host "Installing Kusto CLI..."

# Define target folder for Kusto CLI
$targetFolder = "$env:USERPROFILE\KustoCLI"  # You can change this to any desired path

# Install the Microsoft.Azure.Kusto.Tools package via Install-Package
Install-Package -Name "Microsoft.Azure.Kusto.Tools" -Source "nuget.org" -ProviderName "NuGet" -Destination $targetFolder -Force

# Step 2: Determine the correct tools directory based on PowerShell version
$psVersion = $PSVersionTable.PSVersion.Major

# Find the actual tools folder by searching for the first match of the package version
$toolsFolder = Get-ChildItem -Path (Join-Path -Path $targetFolder -ChildPath "Microsoft.Azure.Kusto.Tools*") -Directory | Select-Object -First 1
if (-not $toolsFolder) {
    Write-Host "Failed to locate the tools folder. Exiting..."
    exit 1
}
$toolsFolder = $toolsFolder.FullName

if ($psVersion -ge 7) {
    # PowerShell 7+ uses the net6.0 directory
    $toolsFolder = Join-Path -Path $toolsFolder -ChildPath "tools\net6.0"
    Write-Host "PowerShell 7+ detected. Using net6.0 version of the Kusto CLI."
} else {
    # Windows PowerShell uses the net472 directory
    $toolsFolder = Join-Path -Path $toolsFolder -ChildPath "tools\net472"
    Write-Host "Windows PowerShell detected. Using net472 version of the Kusto CLI."
}

# Check if the tools folder exists
if (-not (Test-Path $toolsFolder)) {
    Write-Host "Failed to locate the tools folder. Exiting..."
    exit 1
}

# Step 3: Add the tools folder to PATH if not already present
$userPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::User)
if (-not $userPath.Contains($toolsFolder)) {
    Write-Host "Adding Kusto CLI tools folder to PATH..."
    [Environment]::SetEnvironmentVariable("Path", $userPath + ";$toolsFolder", [EnvironmentVariableTarget]::User)
    Write-Host "Please restart your terminal for changes to take effect."
} else {
    Write-Host "Kusto CLI tools folder is already in your PATH."
}

# step 4: update this session's path if the folder is not in the path
if (-not $env:PATH.Contains($toolsFolder)) {
    Write-Host "Adding Kusto CLI tools folder to PATH for this session..."
    $env:PATH += ";$toolsFolder"
}


Write-Host "Installation complete. The Kusto CLI tool is now ready for use."
