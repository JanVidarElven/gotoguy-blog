---
title: "Connect to Microsoft Graph in Azure DevOps Pipelines using Workload Identity Federation"
date: 2023-09-15T12:31:36Z
draft: false
slug: "connect-to-microsoft-graph-in-azure-devops-pipelines-using-workload-identity-federation"
tags:
  - "Azure Pipelines"
  - "EntraID"
  - "Security"
  - "Workload Identities"
categories:
  - "Automation"
  - "Azure"
  - "Azure DevOps"
  - "DevOps"
  - "Entra ID"
  - "Microsoft Entra"
  - "Microsoft Graph"
---

Microsoft recently announced that Workload Identity Federation for Azure Pipelines now is in Public Preview: <https://devblogs.microsoft.com/devops/public-preview-of-workload-identity-federation-for-azure-pipelines/>.



This opens for a lot of scenarios for Azure service connections, without the need to manage secrets for service principals and more security as there are no secrets that can be exposed or exfiltrated.



As I work a lot with Microsoft Graph and automation, I wanted to see if and how I could use Workload Identity Federation to connect to and send queries to Microsoft Graph using Azure Pipelines.



## Create the Workload Identity Federation Service Connection



First of all, I need to create a service connection in my Azure DevOps project that will use the new Workload Identity Federation. To be able to do this, you need to have access to the preview functionality, see details here in this learn article: [Create an Azure Resource Manager service connection using workload identity federation](https://learn.microsoft.com/nb-no/azure/devops/pipelines/library/connect-to-azure?view=azure-devops&WT.mc_id=linkedin&sharingId=EM-MVP-5001872).



When you have access to the feature, you can create a new Workload Identity federation either by manual or automatic configuration:


[![](/uploads/2023/09/image.png?w=914)](/uploads/2023/09/image.png)



I will now choose the Azure Subscription, and optionally a Resource Group. Choosing a resource group is a good idea, as the service connection will be given Contributor access only to that Resource Group, and not the whole subscription. But it also depends on what you want to use your Service Connection for, in my case it is a demo scenario for Microsoft Graph Access, so it makes sense to scope the permissions down:


[![](/uploads/2023/09/image-1.png?w=450)](/uploads/2023/09/image-1.png)



After creating the Service Connection, I can find it my Entra ID tenant. Let's look at the role assignments for the Resource Group first:


[![](/uploads/2023/09/image-2.png?w=1024)](/uploads/2023/09/image-2.png)



The service principal has been given the name of <DevOps Org>-<DevOps Project>-<guid>, and been assigned with Contributor access to that RG.



Next, let's find the App Registration for the Service Connection. As you can see from below there has been **no** (0) credentials of secrets or certificates created, but there has been created a Federated credential:


[![](/uploads/2023/09/image-3.png?w=1024)](/uploads/2023/09/image-3.png)



If we look at the detail for the federated credential, we can se the issuer, subject and audience, and confirm that this service principal only can be access by the service connection in Azure DevOps:


[![](/uploads/2023/09/image-4.png?w=1024)](/uploads/2023/09/image-4.png)



Next, go to API permissions. Here I will add a Microsoft Graph permission, so that we can use that for queries in the pipeline later. In my case I add the Application permission User.Read.All, so I can look up user information:


[![](/uploads/2023/09/image-5.png?w=1024)](/uploads/2023/09/image-5.png)



We are now ready to set up an Azure Pipeline to use this service connection.



## Create the Azure Pipeline to access Microsoft Graph API



In your DevOps project, if this is a new project, make sure that you initialize the Repository, and that you have at least a Basic or Visual Studio access level, then head to Pipelines and create a "New Pipeline". For my environment I will just choose the following steps:



1. Select Azure Repos Git (YAML)
2. Select my repository
3. Use a starter pipeline (or you can choose an existing if you have)



This is a sample YAML code that will use the service connection (se below picture) to get an access token for Microsoft Graph, and the use that access token to connect to Graph PowerShell SDK. In my example I'm just showing how to get some simple user information:


[![](/uploads/2023/09/image-8.png?w=808)](/uploads/2023/09/image-8.png)



There are different ways you can go about this, in my case I was just using Azure CLI in one task to get the access token for the resource type that is Graph. (You can also use Az PowerShell task for this by the way). I also set and secure the variable for use in later steps in the pipeline job.



In the next task I use PowerShell Core to convert the token to a secure string, and then install the required Microsoft Graph PowerShell modules. I can then connect to Graph and get user information. Here is the complete YAML code:



```powershell
# Pipeline for accessing Microsoft Graph using Federated Workload Identity Credential
# Created by Jan Vidar Elven, Evidi, 15.09.2023

trigger:
- none

pool:
  vmImage: windows-latest

steps:
- task: AzureCLI@2
  displayName: 'Get Graph Token for Workload Federated Credential'
  inputs:
    azureSubscription: 'wi-fed-sconn-ado-to-msgraph'
    scriptType: 'pscore'
    scriptLocation: 'inlineScript'
    inlineScript: |
      $token = az account get-access-token --resource-type ms-graph
      $accessToken = ($token | ConvertFrom-Json).accessToken
      Write-Host "##vso[task.setvariable variable=secretToken;issecret=true]$accessToken"
- task: PowerShell@2
  displayName: 'Connect to Graph PowerShell with Token'
  inputs:
    targetType: 'inline'
    script: |
      # Convert the secure variable to a secure string
      $secureToken = ConvertTo-SecureString -String $(secretToken) -AsPlainText

      # Install Microsoft Graph Modules required
      Install-Module Microsoft.Graph.Authentication -Force
      Install-Module Microsoft.Graph.Users -Force

      # Connect to MS Graph
      Connect-MgGraph -AccessToken $secureToken

      # Get User Info
      Get-MgUser -UserId "jan.vidar@elven.no"
      
    pwsh: true
```



I can now try to run the pipeline. At first run you will have to validate and permit access to the service connection from the pipeline:


[![](/uploads/2023/09/image-6.png?w=1024)](/uploads/2023/09/image-6.png)



And then I can verify that it indeed can connect to the Graph via PowerShell SDK and get my resources via the Workload Identity Federation service connection:


[![](/uploads/2023/09/image-7.png?w=1024)](/uploads/2023/09/image-7.png)



## Summary and Usage Scenarios



Most will use the new Workload Identity Federation for Azure Pipelines that access Azure subscriptions and resources, but I have shown as as long as this is using the Entra ID authentication platform and OIDC, it is possible to get access tokens for other API's as well, in this case Microsoft Graph API.



You can use Graph API to get information about your tenant, to enrich and complement your exisiting CI/CD pipelines, or in some case automate consistent deployments also for Graph resources, like for example important settings and policies.
