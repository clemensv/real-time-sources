// Antwerp City Reports — Azure App Service + supporting resources
// Deploys: App Service Plan (B1 Linux), Web App (Python 3.10), client secret

@description('Deployment name prefix')
param deploymentName string = 'antwerp-reports'

@description('Azure region')
param location string = resourceGroup().location

@description('App Service Plan SKU')
param appServicePlanSku string = 'B1'

@description('Azure AD Client ID for the SPA app registration')
param azureAdClientId string

@description('Azure AD Tenant ID')
param azureAdTenantId string

@description('KQL Cluster URI')
param kqlCluster string

@description('KQL Database name')
param kqlDatabase string = 'antwerp'

@description('Azure Maps subscription key')
@secure()
param azureMapsKey string = ''

// ── App Service Plan ──────────────────────────────────────────────────────
resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: '${deploymentName}-plan'
  location: location
  kind: 'linux'
  sku: {
    name: appServicePlanSku
  }
  properties: {
    reserved: true // Linux
  }
}

// ── Web App ───────────────────────────────────────────────────────────────
resource webApp 'Microsoft.Web/sites@2023-12-01' = {
  name: deploymentName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.10'
      appCommandLine: 'startup.sh'
      alwaysOn: true
      ftpsState: 'Disabled'
      appSettings: [
        { name: 'AZURE_TENANT_ID', value: azureAdTenantId }
        { name: 'AZURE_CLIENT_ID', value: azureAdClientId }
        { name: 'KQL_CLUSTER', value: kqlCluster }
        { name: 'KQL_DATABASE', value: kqlDatabase }
        { name: 'AZURE_MAPS_KEY', value: azureMapsKey }
        { name: 'SCM_DO_BUILD_DURING_DEPLOYMENT', value: 'true' }
        { name: 'ENABLE_ORYX_BUILD', value: 'true' }
      ]
    }
  }
}

// ── Outputs ───────────────────────────────────────────────────────────────
output webAppName string = webApp.name
output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output managedIdentityPrincipalId string = webApp.identity.principalId
