param location string = resourceGroup().location
param appName string
param acrName string
param skuName string = 'B1'

param vnetName string
param vnetAddressPrefix string
param appIntegrationSubnetName string
param appIntegrationSubnetPrefix string
param privateEndpointSubnetName string
param privateEndpointSubnetPrefix string
param sqlServerName string
param sqlDatabaseName string
param sqlAdminLogin string
@secure()
param sqlAdminPassword string
param privateEndpointName string
param privateDnsZoneName string

var appServicePlanName = '${appName}-plan'
var webAppName = '${appName}-web'
module sqlPrivateEndpoint 'modules/sql-private-endpoint.bicep' = {
  name: 'sqlPrivateEndpointDeployment'
  params: {
    sqlServerName: sqlServerName
    location: location
    privateEndpointName: privateEndpointName
    privateEndpointSubnetId: networking.outputs.privateEndpointSubnetId
    privateDnsZoneName: privateDnsZoneName
    vnetId: networking.outputs.vnetId
  }
}

module networking 'modules/networking.bicep' = {
  name: 'networkingDeployment'
  params: {
    vnetName: vnetName
    location: location
    vnetAddressPrefix: vnetAddressPrefix
    appIntegrationSubnetName: appIntegrationSubnetName
    appIntegrationSubnetPrefix: appIntegrationSubnetPrefix
    privateEndpointSubnetName: privateEndpointSubnetName
    privateEndpointSubnetPrefix: privateEndpointSubnetPrefix
  }
}
module sql 'modules/sql.bicep' = {
  name: 'sqlDeployment'
  params: {
    sqlServerName: sqlServerName
    sqlDatabaseName: sqlDatabaseName
    location: location
    sqlAdminLogin: sqlAdminLogin
    sqlAdminPassword: sqlAdminPassword
  }
}

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
