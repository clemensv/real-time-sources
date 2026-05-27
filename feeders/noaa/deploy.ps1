# PowerShell version: 7.1

# Define variables
$AppName = "noaa-data-poller-app"
$ResourceGroup = "noaa-data-poller"
$Location = ""
$RegistryName = ""
$ImageName = "noaa-data-poller"
$StorageAccountName = "noaadatapoller"
$ConnectionStringSecret = ""

# prompt to change or leave the $AppName
$changeAppName = Read-Host "`r`nDefault app name is '$AppName'.`r`nProvide a new name or press ENTER to keep the current name"
if (-not [string]::IsNullOrEmpty($changeAppName)) {
    $AppName = $changeAppName
}

# prompt for the $ConnectionStringSecret if empty
if ([string]::IsNullOrEmpty($ConnectionStringSecret)) {
    $ConnectionStringSecret = Read-Host "`r`nProvide the Microsoft Fabric Event Stream custom input endpoint connection string"
}

# validate and exit if the connection string is empty
if ([string]::IsNullOrEmpty($ConnectionStringSecret)) {
    Write-Host "The connection string is required. Exiting."
    exit
}

# validate the connection string for whether it's a valid Event Hubs connection string. Test for the presence of Endpoint and EntityPath
if (-not ($ConnectionStringSecret -match "Endpoint=.*;EntityPath=.*")) {
    Write-Host "The connection string is not valid. Exiting."
    exit
}

# Login to Azure if not already logged in
if (-not (az account show)) {
    az login
}

# Prompt for the Location from a list of available locations
$locations = az account list-locations --query "[?metadata.regionType == 'Physical'].{Name:name, DisplayName:displayName, Geo: metadata.geographyGroup}" --output json | ConvertFrom-Json | Sort-Object Geo, DisplayName
$locationChoice = $null
do {
    Write-Host "`r`nAvailable Locations:"
    $priorGeo = ""
    $locations | ForEach-Object {
        $index = [array]::IndexOf($locations, $_)
        $number = $index + 1
        if ($priorGeo -ne $_.Geo) {
            Write-Host
            Write-Host
            Write-Host $_.Geo
            Write-Host "------------------"
            $priorGeo = $_.Geo
        }
        $displayName = $_.DisplayName
        Write-Host -NoNewLine ("{0,-30}" -f "$number. $displayName")
        if ($index % 3 -eq 2) {
            Write-Host
        }
    }
    $locationNumber = Read-Host "`r`nEnter the number of the desired location"
    if ([int]::TryParse($locationNumber, [ref]$locationChoice) -and $locationChoice -ge 1 -and $locationChoice -le $locations.Count+1) {
        $locationChoice -= 1
    } else {
        Write-Host "Invalid input. Please enter a valid number."
    }
} while ($null -eq $locationChoice)
$Location = $locations[$locationChoice].Name


# Prompt for the ResourceGroup if empty and validate input
do {
    $changeResourceGroup = Read-Host "`r`nResource group is '$ResourceGroup'.`r`nProvide a new name or press Enter to keep the current name"
    if ([string]::IsNullOrEmpty($changeResourceGroup)) {
        break
    }
} while (-not ($changeResourceGroup -match "^[a-zA-Z0-9_-]+$"))
if (-not [string]::IsNullOrEmpty($changeResourceGroup)) {
    $ResourceGroup = $changeResourceGroup
}

#prompt for the StorageAccountName if empty and validate input
do {
    $changeStorageAccountName = Read-Host "`r`nStorage Account name is '$StorageAccountName'.`r`nProvide a new name or press Enter to keep the current name"
    if ([string]::IsNullOrEmpty($changeStorageAccountName)) {
        break
    }
} while (-not ($changeStorageAccountName -match "^[a-zA-Z0-9_-]+$"))
if (-not [string]::IsNullOrEmpty($changeStorageAccountName)) {
    $StorageAccountName = $changeStorageAccountName
}

#Prompt for the RegistryName if empty and validate input
if ([string]::IsNullOrEmpty($RegistryName)) {
    do {
        $RegistryName = Read-Host "`r`nEnter the Azure Container Registry name"
    } while (-not ($RegistryName -match "^[a-zA-Z0-9_-]+$"))
}

# Check if the resource group already exists
$existingResourceGroup = az group show --name $ResourceGroup --query name --output tsv
# Create the resource group if it doesn't exist
if (-not $existingResourceGroup) {
    az group create --name $ResourceGroup --location $Location
}

$AcrName = "$RegistryName.azurecr.io"
# Create a container registry if it doesn't exist
$existingRegistry = az acr show --name $RegistryName --query name --output tsv
if (-not $existingRegistry) {
    Write-Host "Exiting."
    exit
}

# Log in to the Azure Container Registry
az acr login --name $RegistryName

# Create a storage account and file share if not already created
$existingStorageAccount = az storage account show --name $StorageAccountName --resource-group $ResourceGroup --query name --output tsv
if (-not $existingStorageAccount) {
    az storage account create --name $StorageAccountName --resource-group $ResourceGroup --location $Location --sku Standard_LRS --allow-blob-public-access false
}
$FileShareName = $StorageAccountName
$existingFileShare = az storage share exists --name $FileShareName --account-name $StorageAccountName --query exists --output tsv
if ($existingFileShare -ne "true") {
    Write-Host "Creating file share $FileShareName"
    az storage share create --name $FileShareName --account-name $StorageAccountName
}
else {
    Write-Host "File share $FileShareName already exists"
}

# get the storage account key
$StorageAccountKey = az storage account keys list --account-name $StorageAccountName --resource-group $ResourceGroup --query "[0].value" --output tsv

$registryPassword = az acr credential show --name $RegistryName --query passwords[0].value --output tsv
$registryUsername = az acr credential show --name $RegistryName --query username --output tsv

$existingContainer = az container show --resource-group $ResourceGroup --name noaa-data-poller-app --query name --output tsv
if  (-not $existingContainer) {
    az container create --resource-group $ResourceGroup `
        --name $AppName `
        --image "$AcrName/${ImageName}:latest" `
        --cpu .5 `
        --memory 1 `
        --restart-policy Always `
        --secure-environment-variables CONNECTION_STRING="$ConnectionStringSecret" `
        --environment-variables NOAA_LAST_POLLED_FILE="/mnt/fileshare/noaa_last_polled.json" `
        --azure-file-volume-account-name $StorageAccountName `
        --azure-file-volume-account-key $StorageAccountKey `
        --azure-file-volume-share-name $FileShareName `
        --azure-file-volume-mount-path /mnt/fileshare `
        --registry-password $registryPassword `
        --registry-username $registryUsername
} else {
    az container restart --resource-group $ResourceGroup --name $AppName
}

