---
title: "Add Graph Application Permissions to Managed Identity using Bicep Graph Extension"
date: 2024-05-23T07:48:18Z
draft: false
slug: "add-graph-application-permissions-to-managed-identity-using-bicep-graph-extension"
tags:
  - "Bicep"
  - "EntraID"
  - "Managed Identities"
categories:
  - "Automation"
  - "Entra ID"
  - "Infrastructure as Code"
  - "Microsoft Graph"
---

A while back I published a blog post on how you can add Microsoft Graph application role permissions to a Managed Identity, something that is useful if you have deployed Azure services that use managed identities, and need permission to access Graph API. [https://gotoguy.blog/](https://gotoguy.blog/2022/03/15/add-graph-application-permissions-to-managed-identity-using-graph-explorer/)[2022](https://gotoguy.blog/2022/03/15/add-graph-application-permissions-to-managed-identity-using-graph-explorer/)[/03/15/add-graph-application-permissions-to-managed-identity-using-graph-explorer/](https://gotoguy.blog/2022/03/15/add-graph-application-permissions-to-managed-identity-using-graph-explorer/)



The above blog post is currently the only "graphical" or UI based way that you can assign those permissions today, most people use Microsoft Graph SDK PowerShell for this. On the other hand, many also rely on Infrastructure as Code to deploy Azure resources, for example by using Bicep, and while Bicep can provision Managed Identities and Role Assignments to Azure resources, you cannot assign application role permissions to Microsoft Graph without using another more "imperative" method.



That changed now on May 21st, where the Public Preview of the Bicep support for Microsoft Graph was announced! [Announcing public preview of Bicep templates support for Microsoft Graph](https://techcommunity.microsoft.com/t5/azure-governance-and-management/announcing-public-preview-of-bicep-templates-support-for/ba-p/4141772?wt.mc_id=EM-MVP-5001872)



While there a a limit set of scenarios where we can use Bicep for Graph at this time, mostly focusing on applications, service principals and groups, there is also support for managing scopes and role permissions via oauth2PermissionGrants and [appRoleAssignedTo](https://learn.microsoft.com/nb-no/graph/templates/reference/approleassignedto?view=graph-bicep-beta&WT.mc_id=linkedin&sharingId=EM-MVP-5001872). And this caught my attention, as this was exactly the way I approached this via my blog post on how to add Graph application permissions using Graph Explorer.



Lets say that you have a Bicep deployment consisting of a Resource Group, User Assigned Managed Identity, and maybe a Function App or a Logic App or something similar that is assigned the managed identity, and you need to assign Graph application role permissions to that service principal. That can all be done now in Bicep, let me show you how!



## Walkthrough



The complete bicep code is available at my GitHub and the following repository:



<https://github.com/JanVidarElven/add-managed-identity-graph-permissions-via-bicep>



### bicepconfig.json



You need to enable experimental features by adding a bicepconfig.json file with the following content:



```json
{
    "experimentalFeaturesEnabled": {
        "extensibility": true
    }
}
```



### main.bicep



Then you can start building your bicep declarations. In my example I will start simple by using an existing Resource Group and User Assigned Managed Identity, and deploy at Subscription scope:



```bicep
targetScope = 'subscription'

// Main Parameters for Existing Resources
param resourceGroupName string = 'rg-<your-resource-group>'
param managedIdentityName string = 'mi-<your-managed-identity>'

// Get existing Azure resources for Resource Group and Managed Identity
resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' existing = {
  name: resourceGroupName
}
resource userManagedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' existing = {
  name: managedIdentityName
  scope: resourceGroup(rg.name)
}
```



Next I need to initalize the use of the MicrosoftGraph provider in the main.bicep file:



```bicep
// Initialize the Graph provider
provider microsoftGraph
```



I can now use the Bicep Graph and get the existing Service Principal for the Managed Identity:



```bicep
// Get the Principal Id of the Managed Identity resource
resource miSpn 'Microsoft.Graph/servicePrincipals@v1.0' existing = {
  appId: userManagedIdentity.properties.clientId
  // Tip! If using a System Assigned managed identity, you can refer to the resource symbolic name
  // directly and use <resourcesymbolicname>.identity.principalId for appId
}
```



I also need to get the existing Service Principal for Microsoft Graph, using the well know Graph appId:



```bicep
// Get the Resource Id of the Graph resource in the tenant
resource graphSpn 'Microsoft.Graph/servicePrincipals@v1.0' existing = {
  appId: '00000003-0000-0000-c000-000000000000'
}
```



All that remains now then is to create an array of all the application roles I want to assign, and loop through to assign each of the role permissions:



```bicep
// Define the App Roles to assign to the Managed Identity
param appRoles array = [
  'User.Read.All'
  'Device.Read.All'
]

// Looping through the App Roles and assigning them to the Managed Identity
resource assignAppRole 'Microsoft.Graph/appRoleAssignedTo@v1.0' = [for appRole in appRoles: {
  appRoleId: (filter(graphSpn.appRoles, role => role.value == appRole)[0]).id
  principalId: miSpn.id
  resourceId: graphSpn.id
}]
```



Basically I'm using the same logic here as my above mentioned blog post on using Graph Explorer, but in this case I'm able to use Bicep all the way.



### Deploy



Now all that remains is to deploy:



```bash
az deployment sub create --location NorwayEast --name "bicep-graph-demo" --template-file .\main.bicep
```



## Summary



This simple scenario shows how we now can use Bicep also for managing application role permissions together with Azure ressources that has assigned managed identities, and you no longer need to do this separately if you are using IaC. Note that the user running the deployment need permission to assign role permissions, see the documentation for details on that.
