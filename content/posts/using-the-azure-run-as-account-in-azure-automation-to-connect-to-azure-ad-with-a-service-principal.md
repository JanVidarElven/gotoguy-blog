---
title: "Using the Azure Run As Account in Azure Automation to Connect to Azure AD with a Service Principal"
date: 2018-07-11T11:08:35Z
draft: false
slug: "using-the-azure-run-as-account-in-azure-automation-to-connect-to-azure-ad-with-a-service-principal"
categories:
  - "Azure"
  - "Azure AD"
  - "Azure Automation"
  - "Enterprise Mobility + Security"
  - "PowerShell"
---

If you are using Azure Automation and working with Runbooks for automating against your Azure subscription, you can create an Azure Run As Account for authenticating and logging in to your subscription. The Azure Run As Account is configured in your Automation Account, and will do the following:

- Creates an Azure AD application with a self-signed certificate, creates a service principal account for the application in Azure AD, and assigns the Contributor role for the account in your current subscription.
- Creates an Automation certificate asset named AzureRunAsCertificate in the specified Automation account. The certificate asset holds the certificate private key that's used by the Azure AD application.
- Creates an Automation connection asset named AzureRunAsConnection in the specified Automation account. The connection asset holds the applicationId, tenantId, subscriptionId, and certificate thumbprint.

You can read more about setting up Azure Run As Accounts here, including how to do a more customized setup with PowerShell: [https://docs.microsoft.com/en-us/azure/automation/automation-create-runas-account](https://docs.microsoft.com/en-us/azure/automation/automation-create-runas-account "https://docs.microsoft.com/en-us/azure/automation/automation-create-runas-account").
Something worth noting is that this Azure Run As Account will by default have the Contributor role to your entire subscription, so it would make sense to look into changing RBAC settings for the subcription or resource groups if you want to limit that. Also, all users that have access to the Automation Account will also have the opprotunity to use this Azure Run As Account.
Having said that, the Azure Run As Account is a great way to authenticate securely with certificates and a service principal name without needing to store a username and password in a credential object.
So I thought, wouldn’t it be great if we could use this same Azure Run As Account to log in to your Azure AD tenant for the possibility to run Azure AD PowerShell commands? The reason I thought of this is because of this article showing how to authenticate with Azure AD v2 PowerShell and Service Principal: [https://docs.microsoft.com/en-us/powershell/azure/active-directory/signing-in-service-principal?view=azureadps-2.0](https://docs.microsoft.com/en-us/powershell/azure/active-directory/signing-in-service-principal?view=azureadps-2.0 "https://docs.microsoft.com/en-us/powershell/azure/active-directory/signing-in-service-principal?view=azureadps-2.0"). In this short blog post will show you how to do this.

## Getting the Azure Run As Account details

First, look into your Automation Account and Account Settings to find any Run as accounts:
[![image](/uploads/2018/07/image_thumb27.png "image")](/uploads/2018/07/image27.png)
Click on the Azure Run As Account to see the details (or to create one if you haven’t before). Take a note of the Service Principal Object Id, we will use that later:
[![image](/uploads/2018/07/image_thumb28.png "image")](/uploads/2018/07/image28.png)

## Creating a Runbook that Authenticates with Service Principal to Azure AD

Now, let’s create a PowerShell runbook using the Azure Run As Account for connecting to Azure AD.
First, I set the connection name  “AzureRunAsConnection”, and then save that as a variable for holding my service principal details using the Get-AutomationConnection cmdlet.
Then, logging in to Azure AD is done with specifiying TenantId, ApplicationId and CertificateThumbprint parameters, as shown below:
[![image](/uploads/2018/07/image_thumb29.png "image")](/uploads/2018/07/image29.png)
This will log in my service principal to Azure AD and I’m ready to run some commands, for example getting some organization details for the tenant, or counting different types of user objects:
[![image](/uploads/2018/07/image_thumb30.png "image")](/uploads/2018/07/image30.png)
Running this runbook will for example show me this output for my tenant. This shows that I successfully authenticated with the Azure Run As Account service principal:
[![image](/uploads/2018/07/image_thumb31.png "image")](/uploads/2018/07/image31.png)
Here is a link to a Gist where I have included the above PowerShell runbook script:
https://gist.github.com/skillriver/175aad353e0311378068f5191a04587d

## Role Permissions for the Service Principal

Depending on what kind of automation you want to do against Azure AD, especially if you want to write data, you will have to add the Service Principal to an Azure AD Role. Here is a couple of examples, using the object id for the service principal I told you to note earlier from the Azure Run As Account:

```powershell
# Get the associated Service Principal for the Azure Run As Account
$runAsServicePrincipal = Get-AzureADServicePrincipal -ObjectId ""

# Add the Service Principal to the Directory Readers Role
Add-AzureADDirectoryRoleMember -ObjectId (Get-AzureADDirectoryRole | where-object {$_.DisplayName -eq "Directory Readers"}).Objectid -RefObjectId $runAsServicePrincipal.ObjectId

# Add the Service Principal to the User Administrator Role
Add-AzureADDirectoryRoleMember -ObjectId (Get-AzureADDirectoryRole | where-object {$_.DisplayName -eq "User Account Administrator"}).Objectid -RefObjectId $aaAadUser.ObjectId

# Add the Service Principal to the Global Administrator Role
Add-AzureADDirectoryRoleMember -ObjectId (Get-AzureADDirectoryRole | where-object {$_.DisplayName -eq "Company Administrator"}).Objectid -RefObjectId $runAsServicePrincipal.ObjectId
```

That concludes this short blog post, hope it has been helpful! Thanks for reading and remember to share if it was useful ![Smile](/uploads/2018/07/wlemoticon-smile.png)
