param webAppName string
param location string
param planId string
param acrLoginServer string
param imageName string = 'secure-webapp'
param imageTag string = 'latest'

resource webApp 'Microsoft.Web/sites@2022-09-01' = {
  name: webAppName
  location: location
  kind: 'app,linux'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: planId
    siteConfig: {
      linuxFxVersion: 'DOCKER|${acrLoginServer}/${imageName}:${imageTag}'
      acrUseManagedIdentityCreds: false
    }
  }
}

output webAppName string = webApp.name
