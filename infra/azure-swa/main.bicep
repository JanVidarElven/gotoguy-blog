@description('Name of the Azure Static Web App resource.')
param staticWebAppName string

@description('Azure region for the Static Web App.')
param location string = resourceGroup().location

@description('SKU for the Static Web App.')
@allowed([
  'Free'
  'Standard'
])
param skuName string = 'Standard'

@description('Optional tags for the Static Web App.')
param tags object = {}

resource staticWebApp 'Microsoft.Web/staticSites@2023-12-01' = {
  name: staticWebAppName
  location: location
  tags: tags
  sku: {
    name: skuName
    tier: skuName
  }
  properties: {}
}

output staticWebAppId string = staticWebApp.id
output defaultHostname string = staticWebApp.properties.defaultHostname
