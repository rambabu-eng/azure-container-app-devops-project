param location string = resourceGroup().location
param appName string
param acrName string
param skuName string = 'B1'

var appServicePlanName = '${appName}-plan'
var webAppName = '${appName}-web'

module acr 'modules/acr.bicep' = {
  name: 'acrDeployment'
  params: {
    acrName: acrName
    location: location
  }
}

module appServicePlan 'modules/appserviceplan.bicep' = {
  name: 'aspDeployment'
  params: {
    planName: appServicePlanName
    location: location
    skuName: skuName
  }
}

module webApp 'modules/webapp.bicep' = {
  name: 'webAppDeployment'
  params: {
    webAppName: webAppName
    location: location
    planId: appServicePlan.outputs.planId
    acrLoginServer: acr.outputs.loginServer
  }
}
