# PowerShell version: 7.1

# Define variables
$RegistryName = ""
$ImageName = "noaa-data-poller"
$DockerfilePath = "./Dockerfile"  # Path to the Dockerfile
$ContextDirectory = "./"  # Context directory for Docker build

# Login to Azure if not already logged in
if (-not (az account show)) {
    az login
}

#Prompt for the RegistryName if empty and validate input
if ([string]::IsNullOrEmpty($RegistryName)) {
    do {
        $RegistryName = Read-Host "`r`nEnter the Azure Container Registry name"
    } while (-not ($RegistryName -match "^[a-zA-Z0-9_-]+$"))
}

$AcrName = "$RegistryName.azurecr.io"
# Create a container registry if it doesn't exist
$existingRegistry = az acr show --name $RegistryName --query name --output tsv
if (-not $existingRegistry) {
    Write-Host "The Azure Container Registry $RegistryName does not exist."
    exit
}

# Log in to the Azure Container Registry
az acr login --name $RegistryName

# Build the Docker image and push it to the Azure Container Registry
docker build -f $DockerfilePath -t "$AcrName/${ImageName}:latest" $ContextDirectory
if ($? -eq $true) {
    Write-Host "Docker image built successfully."
} else {
    Write-Host "Docker image build failed. Exiting."
    exit
}

docker push "$AcrName/${ImageName}:latest"
if ($? -eq $true) {
    Write-Host "Docker image pushed to the Azure Container Registry successfully."
} else {
    Write-Host "Docker image push failed. Exiting."
    exit
}
