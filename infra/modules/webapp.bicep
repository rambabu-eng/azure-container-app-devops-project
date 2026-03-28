param webAppName string
param location string
param planId string
param acrLoginServer string

resource webApp 'Microsoft.Web/sites@2022-09-01' = {
  name: webAppName
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: planId
    siteConfig: {
      linuxFxVersion: 'DOCKER|${acrLoginServer}/placeholder:latest'
    }
  }
}

output webAppName string = webApp.name
