#!/bin/bash
# Deploys the European Water container group to Azure Container Instances.
#
# Usage:
#   ./deploy.sh <resource-group-name> <connection-string> [location]
#
# Arguments:
#   resource-group-name  - Azure resource group (created if it doesn't exist)
#   connection-string    - Kafka/Event Hub connection string for all containers
#   location             - Azure region (default: westeurope)

set -euo pipefail

RESOURCE_GROUP="${1:?Usage: $0 <resource-group> <connection-string> [location]}"
CONNECTION_STRING="${2:?Usage: $0 <resource-group> <connection-string> [location]}"
LOCATION="${3:-westeurope}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_FILE="$SCRIPT_DIR/azure-template.json"

# Ensure resource group exists
if ! az group show --name "$RESOURCE_GROUP" &>/dev/null; then
    echo "Creating resource group '$RESOURCE_GROUP' in '$LOCATION'..."
    az group create --name "$RESOURCE_GROUP" --location "$LOCATION" --output none
fi

echo "Deploying European Water container group..."
az deployment group create \
    --resource-group "$RESOURCE_GROUP" \
    --template-file "$TEMPLATE_FILE" \
    --parameters connectionStringSecret="$CONNECTION_STRING" \
    --verbose

echo "Deployment complete."
