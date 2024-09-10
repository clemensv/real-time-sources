#!/bin/bash

# Define variables
AppName="noaa-data-poller-app"
ResourceGroup="<your-resource-group>"
Location=""
RegistryName=""
ImageName="noaa-data-poller"
StorageAccountName="<your-storage-account-name>"
ConnectionStringSecret=""

# prompt to change or leave the $AppName
read -p $'\nDefault app name is "$AppName".\nProvide a new name or press ENTER to keep the current name: ' changeAppName
if [[ ! -z "$changeAppName" ]]; then
    AppName=$changeAppName
fi

# prompt for the $ConnectionStringSecret if empty
if [[ -z "$ConnectionStringSecret" ]]; then
    read -p $'\nProvide the Microsoft Fabric Event Stream custom input endpoint connection string: ' ConnectionStringSecret
fi

# validate and exit if the connection string is empty
if [[ -z "$ConnectionStringSecret" ]]; then
    echo "The connection string is required. Exiting."
    exit
fi

# validate the connection string for whether it's a valid Event Hubs connection string. Test for the presence of Endpoint and EntityPath
if [[ ! "$ConnectionStringSecret" =~ Endpoint=.*;EntityPath=.* ]]; then
    echo "The connection string is not valid. Exiting."
    exit
fi

# Login to Azure if not already logged in
if ! az account show >/dev/null; then
    az login
fi

# Prompt for the Location from a list of available locations
locations=$(az account list-locations --query "[?metadata.regionType == 'Physical'].{Name:name, DisplayName:displayName, Geo: metadata.geographyGroup}" --output json | jq -r '.[] | "\(.Name) \(.DisplayName) \(.Geo)"')
locationChoice=""
while [[ -z "$locationChoice" ]]; do
    echo -e "\nAvailable Locations:"
    priorGeo=""
    while IFS= read -r location; do
        geo=$(echo "$location" | awk '{print $3}')
        displayName=$(echo "$location" | awk '{print $2}')
        if [[ "$priorGeo" != "$geo" ]]; then
            echo
            echo
            echo "$geo"
            echo "------------------"
            priorGeo=$geo
        fi
        printf "%-30s" "$location"
        if ((++index % 3 == 0)); then
            echo
        fi
    done <<< "$locations"
    read -p $'\nEnter the number of the desired location: ' locationNumber
    if [[ "$locationNumber" =~ ^[0-9]+$ ]] && ((locationNumber >= 1 && locationNumber <= $(echo "$locations" | wc -l)+1)); then
        locationChoice=$((locationNumber - 1))
    else
        echo "Invalid input. Please enter a valid number."
    fi
done
Location=$(echo "$locations" | awk -v choice="$locationChoice" 'NR == choice+1 {print $1}')

# Prompt for the ResourceGroup if empty and validate input
while true; do
    read -p $'\nResource group is "$ResourceGroup".\nProvide a new name or press Enter to keep the current name: ' changeResourceGroup
    if [[ -z "$changeResourceGroup" ]]; then
        break
    fi
    if [[ "$changeResourceGroup" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        ResourceGroup=$changeResourceGroup
        break
    fi
done

# prompt for the StorageAccountName if empty and validate input
while true; do
    read -p $'\nStorage Account name is "$StorageAccountName".\nProvide a new name or press Enter to keep the current name: ' changeStorageAccountName
    if [[ -z "$changeStorageAccountName" ]]; then
        break
    fi
    if [[ "$changeStorageAccountName" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        StorageAccountName=$changeStorageAccountName
        break
    fi
done

# Prompt for the RegistryName if empty and validate input
if [[ -z "$RegistryName" ]]; then
    while true; do
        read -p $'\nEnter the Azure Container Registry name: ' RegistryName
        if [[ "$RegistryName" =~ ^[a-zA-Z0-9_-]+$ ]]; then
            break
        fi
    done
fi

# Check if the resource group already exists
existingResourceGroup=$(az group show --name $ResourceGroup --query name --output tsv)
# Create the resource group if it doesn't exist
if [[ -z "$existingResourceGroup" ]]; then
    az group create --name $ResourceGroup --location $Location
fi

AcrName="$RegistryName.azurecr.io"
# Create a container registry if it doesn't exist
existingRegistry=$(az acr show --name $RegistryName --query name --output tsv)
if [[ -z "$existingRegistry" ]]; then
    echo "Exiting."
    exit
fi

# Log in to the Azure Container Registry
az acr login --name $RegistryName

# Create a storage account and file share if not already created
existingStorageAccount=$(az storage account show --name $StorageAccountName --resource-group $ResourceGroup --query name --output tsv)
if [[ -z "$existingStorageAccount" ]]; then
    az storage account create --name $StorageAccountName --resource-group $ResourceGroup --location $Location --sku Standard_LRS --allow-blob-public-access false
fi
FileShareName=$StorageAccountName
existingFileShare=$(az storage share exists --name $FileShareName --account-name $StorageAccountName --query exists --output tsv)
if [[ "$existingFileShare" != "true" ]]; then
    echo "Creating file share $FileShareName"
    az storage share create --name $FileShareName --account-name $StorageAccountName
else
    echo "File share $FileShareName already exists"
fi

# get the storage account key
StorageAccountKey=$(az storage account keys list --account-name $StorageAccountName --resource-group $ResourceGroup --query "[0].value" --output tsv)

registryPassword=$(az acr credential show --name $RegistryName --query passwords[0].value --output tsv)
registryUsername=$(az acr credential show --name $RegistryName --query username --output tsv)

existingContainer=$(az container show --resource-group $ResourceGroup --name noaa-data-poller-app --query name --output tsv)
if [[ -z "$existingContainer" ]]; then
    az container create --resource-group $ResourceGroup \
        --name $AppName \
        --image "$AcrName/${ImageName}:latest" \
        --cpu .5 \
        --memory 1 \
        --restart-policy Always \
        --secure-environment-variables CONNECTION_STRING="$ConnectionStringSecret" \
        --environment-variables NOAA_LAST_POLLED_FILE="/mnt/fileshare/noaa_last_polled.json" \
        --azure-file-volume-account-name $StorageAccountName \
        --azure-file-volume-account-key $StorageAccountKey \
        --azure-file-volume-share-name $FileShareName \
        --azure-file-volume-mount-path /mnt/fileshare \
        --registry-password $registryPassword \
        --registry-username $registryUsername
else
    az container restart --resource-group $ResourceGroup --name $AppName
fi
