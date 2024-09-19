<#
.SYNOPSIS
    Installs Avrotize, a code generator for schematized data.

.DESCRIPTION
    This script automates the installation of Avrotize, which is utilized by various scripts within this repository. 
    Avrotize helps in generating code based on defined schemas, facilitating the management and manipulation of structured data.

.PARAMETER None
    This script does not take any parameters.

.EXAMPLE
    Run the script to install Avrotize for use in your projects.

.NOTES
    Author: [Your Name]
    Date: [Date]
    Version: 1.0
#>

# Get the user's profile directory
$userProfile = [System.Environment]::GetFolderPath('UserProfile')

# Define the path for the virtual environment
$venvPath = Join-Path $userProfile "avrotize"

# Define the path for the batch wrapper script
$avrotizeBatchPath = Join-Path $userProfile "avrotize.bat"

# Check if Python is installed
$pythonPath = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonPath) {
    Write-Host "Python is not installed. Installing Python using winget..."
    
    # Install Python using winget
    winget install Python.Python.3
    if ($?) {
        Write-Host "Python installed successfully."
    } else {
        Write-Host "Python installation failed."
        exit
    }
}

# Check if pip is installed
$pipPath = Get-Command pip -ErrorAction SilentlyContinue
if (-not $pipPath) {
    Write-Host "pip is not installed. Installing pip..."
    python -m ensurepip --upgrade  # Ensures pip is installed
    if ($?) {
        Write-Host "pip has been installed successfully."
    } else {
        Write-Host "Failed to install pip. Please install it manually."
        exit
    }
}

# Create a virtual environment in the "avrotize" subdir of the user profile
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating a virtual environment in $venvPath"
    python -m venv $venvPath
}

# Activate the virtual environment and install avrotize
$activateScript = "$venvPath\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    Write-Host "Activating virtual environment and installing avrotize..."
    & $activateScript
    pip install avrotize
    Write-Host "avrotize has been installed successfully in the virtual environment."
} else {
    Write-Host "Failed to activate virtual environment."
    exit
}

# Create a batch file wrapper for avrotize
$batchCommand = @"
@echo off
call "$venvPath\Scripts\activate.bat"
python -m avrotize %*
"@

# Write the avrotize wrapper batch file to the user profile directory
Write-Host "Creating a batch file wrapper at $avrotizeBatchPath..."
$batchCommand | Out-File -FilePath $avrotizeBatchPath -Encoding UTF8

# Make the script globally executable by adding its path to the PATH environment variable
$pathEnv = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::User)
if (-not $pathEnv.Contains($userProfile)) {
    Write-Host "Adding $userProfile to PATH..."
    [System.Environment]::SetEnvironmentVariable("Path", "$pathEnv;$userProfile", [System.EnvironmentVariableTarget]::User)
}

Write-Host "Setup complete. You can now run 'avrotize' from any PowerShell or command prompt session."
