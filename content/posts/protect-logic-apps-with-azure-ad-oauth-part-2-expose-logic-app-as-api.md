---
title: "Protect Logic Apps with Azure AD OAuth - Part 2 Expose Logic App as API"
date: 2021-01-11T14:08:05Z
draft: false
slug: "protect-logic-apps-with-azure-ad-oauth-part-2-expose-logic-app-as-api"
tags:
  - "OAuth2"
  - "OpenID Connect"
  - "Security"
categories:
  - "Azure AD"
  - "Logic Apps"
  - "Microsoft Graph"
---

This blog article will build on the previous blog post published, [Protect Logic Apps with Azure AD OAuth – Part 1 Management Access | GoToGuy Blog](https://gotoguy.blog/2020/12/31/protect-logic-apps-with-azure-ad-oauth-part-1-management-access/), which provided some basic understanding around authorizing to Logic Apps request triggers using OAuth and Access Tokens.



In this blog I will build on that, creating a scenario where a Logic App will be exposed as an API to end users. In this API, I will call another popular API: Microsoft Graph.



My scenario will use a case where end users does not have access themselves to certain Microsoft Graph requests, but where the Logic App does. Exposing the Logic App as an API will let users be able to authenticate and authorize, requesting and consenting to the custom Logic App API permissions I choose. Some of these permissions can users consent to themselves, while other must be admin consented. This way I can use some authorizing inside the Logic App, and only let the end users be able to request what they are permitted to.



I will also look into assigning users and groups, and using scopes and roles for additional fine graining end user and principal access to the Logic App.



A lot of topics to cover, so let's get started by first creating the scenario for the Logic App.



## Logic App calling Microsoft Graph API



A Logic App can run requests against the Microsoft Graph API using the HTTP action and specifying the method (GET, POST, etc) and resource URI. For authentication against Graph from the Logic App you can use either:



- Using Azure Active Directory OAuth and Client Credentials Flow with Client Id and Secret.
- Using System or User Assigned Managed Identity.



Permissions for Microsoft Graph API are either using "delegated" (in context of logged in user) or "application" (in context of application/deamon service). These scenarios using Logic App will use application permissions for Microsoft Graph.



PS! Using Logic Apps Custom Connectors ([Custom connectors overview | Microsoft Docs](https://docs.microsoft.com/en-us/connectors/custom-connectors/?WT.mc_id=AZ-MVP-5001872)) you can also use delegated permissions by creating a connection with a logged in user, but this outside of the scope of this article.



### Scenario for using Microsoft Graph in Logic App



There are a variety of usage scenarios for Microsoft Graph, so for the purpose of this Logic App I will focus on one of the most popular: Device Management (Intune API) resources. This is what I want the Logic App to do in this first phase:



- Listing a particular user's managed devices.
- Listing all of the organization's managed devices.
- Filtering managed devices based on operating system and version.



In addition to the above I want to implement the custom API such that any assigned user can list their own devices through end-user consent, but to be able to list all devices or any other user than your self you will need an admin consented permission for the custom API.



### Creating the Logic App



In your Azure subscription, add a new Logic App to your chosen resource group and name it according to your naming standard. After the Logic App is created, you will need add the trigger. As this will be a custom API, you will need it to use HTTP as trigger, and you will also need a response back to the caller, so the easiest way is to use the template for HTTP Request-Response as shown below:


[![](/uploads/2021/01/image.png?w=1024)](/uploads/2021/01/image.png)



Your Logic App will now look like this:


[![](/uploads/2021/01/image-1.png?w=647)](/uploads/2021/01/image-1.png)



Save the Logic App before proceeding.



### Create a Managed Identity for the Logic App



Exit the designer and go to the Identity section of the Logic App. We need a managed identity, either system assigned or user assigned, to let the Logic App authenticate against Microsoft Graph.


[![](/uploads/2021/01/image-2.png?w=939)](/uploads/2021/01/image-2.png)



A system assigned managed identity will follow the lifecycle of this Logic App, while a user assigned managed identity will have it's own lifecycle, and can be used by other resources also. I want that flexibility, so I will create a user assigned managed identity for this scenario. In the Azure Portal, select to create a new resource and find User Assigned Managed Identity:


[![](/uploads/2021/01/image-3.png?w=521)](/uploads/2021/01/image-3.png)



Create a new User Assigned Managed Identity in your selected resource group and give it a name based on your naming convention:


[![](/uploads/2021/01/image-4.png?w=719)](/uploads/2021/01/image-4.png)



After creating the managed identity, go back to your Logic App, and then under Identity section, add the newly created managed identity under User Assigned Managed Identity:


[![](/uploads/2021/01/image-5.png?w=1024)](/uploads/2021/01/image-5.png)



Before we proceed with the Logic App, we need to give the Managed Identity the appropriate Microsoft Graph permissions.



### Adding Microsoft Graph Permissions to the Managed Identity



Now, if we wanted the Logic App to have permissions to the Azure Rest API, we could have easily added Azure role assignments to the managed identity directly:


[![](/uploads/2021/01/image-6.png?w=919)](/uploads/2021/01/image-6.png)



But, as we need permissions to Microsoft Graph, there are no GUI to do this for now. The permissions needed for listing managed devices are documented here: [List managedDevices - Microsoft Graph v1.0 | Microsoft Docs](https://docs.microsoft.com/en-us/graph/api/intune-devices-manageddevice-list?view=graph-rest-1.0&WT.mc_id=M365-MVP-5001872).



So we need a minimum of: DeviceManagementManagedDevices.Read.All.



To add these permissions we need to run some PowerShell commands using the AzureAD module. If you have that installed locally, you can connect and proceed with the following commands, for easy of access you can also use the Cloud Shell in the Azure Portal, just run Connect-AzureAD first:


[![](/uploads/2021/01/image-7.png?w=527)](/uploads/2021/01/image-7.png)



PS! You need to be a Global Admin to add Graph Permissions.



You can run each of these lines separately, or run it as a script:



```powershell
# Microsoft Graph App Well Known App Id
$msGraphAppId = "00000003-0000-0000-c000-000000000000"

# Display Name if Managed Identity
$msiDisplayName="msi-ops-manageddevices" 

# Microsoft Graph Permission required
$msGraphPermission = "DeviceManagementManagedDevices.Read.All" 

# Get Managed Identity Service Principal Name
$msiSpn = (Get-AzureADServicePrincipal -Filter "displayName eq '$msiDisplayName'")

# Get Microsoft Graph Service Principal
$msGraphSpn = Get-AzureADServicePrincipal -Filter "appId eq '$msGraphAppId'"

# Get the Application Role for the Graph Permission
$appRole = $msGraphSpn.AppRoles | Where-Object {$_.Value -eq $msGraphPermission -and $_.AllowedMemberTypes -contains "Application"}

# Assign the Application Role to the Managed Identity
New-AzureAdServiceAppRoleAssignment -ObjectId $msiSpn.ObjectId -PrincipalId $msiSpn.ObjectId -ResourceId $msGraphSpn.ObjectId -Id $appRole.Id
```



Verify that it runs as expected:


[![](/uploads/2021/01/image-8.png?w=1024)](/uploads/2021/01/image-8.png)



As mentioned earlier, adding these permissions has to be done using script commands, but there is a way to verify the permissions by doing the following:



1. Find the Managed Identity, and copy the Client ID:


[![](/uploads/2021/01/image-9.png?w=1024)](/uploads/2021/01/image-9.png)



2. Under Azure Active Directory and Enterprise Applications, make sure you are in the Legacy Search Experience and paste in the Client ID:


[![](/uploads/2021/01/image-10.png?w=838)](/uploads/2021/01/image-10.png)



3. Which you then can click into, and under permissions you will see the admin has consented to Graph permissions:


[![](/uploads/2021/01/image-11.png?w=1024)](/uploads/2021/01/image-11.png)



The Logic App can now get Intune Managed Devices from Microsoft Graph API using the Managed Identity.



### Calling Microsoft Graph from the Logic App



Let's start by adding some inputs to the Logic App. I'm planning to trigger the Logic App using an http request body like the following:



```json
{
 "userUpn": "someuser@elven.no",
 "operatingSystem": "Windows",
 "osVersion": "10"
}
```



In the Logic App request trigger, paste as a sample JSON payload:


[![](/uploads/2021/01/image-12.png?w=816)](/uploads/2021/01/image-12.png)



The request body schema will be updated accordingly, and the Logic App is prepared to receive inputs:


[![](/uploads/2021/01/image-13.png?w=623)](/uploads/2021/01/image-13.png)



Next, add a Condition action, where we will check if we should get a users' managed devices, or all. Use an expression with the empty function to check for userUpn, and another expression for the true value, like below:


[![](/uploads/2021/01/image-14.png?w=636)](/uploads/2021/01/image-14.png)



We will add more logic and conditions later for the filtering of the operating system and version, but for now add an HTTP action under True like the following:


[![](/uploads/2021/01/image-15.png?w=656)](/uploads/2021/01/image-15.png)



Note the use of the Managed Identity and Audience, which will have permission for querying for managed devices.



Under False, we will get the managed devices for a specific user. So add the following, using the userUpn input in the URI:


[![](/uploads/2021/01/image-16.png?w=650)](/uploads/2021/01/image-16.png)



Both these actions should be able to run successfully now, but we will leave the testing for a bit later. First I want to return the managed devices found via the Response action.



Add an Initialize Variable action before the Condition action. Set the Name and Type to Array as shown below, but the value can be empty for now:


[![](/uploads/2021/01/image-17.png?w=629)](/uploads/2021/01/image-17.png)



Next, under True and Get All Managed Devices, add a Parse JSON action, adding the output body from the http action and using either the sample response from the Microsoft Graph documentation, or your own to create the schema.


[![](/uploads/2021/01/image-18.png?w=622)](/uploads/2021/01/image-18.png)



PS! Note that if you have over 1000 managed devices, Graph will page the output, so you should test for odata.nextLink to be present as well. You can use the following anonymized sample response for schema which should work in most cases:



```json
{
     "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#deviceManagement/managedDevices",
     "@odata.count": 1000,
     "@odata.nextLink": "https://graph.microsoft.com/v1.0/deviceManagement/managedDevices?$skiptoken=",
     "value": [
         {
             "id": "id Value",
             "userId": "User Id value",
             "deviceName": "Device Name value",
             "managedDeviceOwnerType": "company",
             "operatingSystem": "Operating System value",
             "complianceState": "compliant",
             "managementAgent": "mdm",
             "osVersion": "Os Version value",
             "azureADRegistered": true,
             "deviceEnrollmentType": "userEnrollment",
             "azureADDeviceId": "Azure ADDevice Id value",
             "deviceRegistrationState": "registered",
             "isEncrypted": true,
             "userPrincipalName": "User Principal Name Value ",
             "model": "Model Value",
             "manufacturer": "Manufacturer Value",
             "userDisplayName": "User Display Name Value",
             "managedDeviceName": "Managed Device Name Value"
         }
     ]
 }
```



PS! Remove any sample response output from schema if values will be null or missing from your output. For example I needed to remove the configurationManagerClientEnabledFeatures from my schema, as this is null in many cases.



Add another Parse JSON action under the get user managed devices action as well:


[![](/uploads/2021/01/image-19.png?w=645)](/uploads/2021/01/image-19.png)



Now we will take that output and do a For Each loop for each value. On both sides of the conditon, add a For Each action, using the value from the previous HTTP action:


[![](/uploads/2021/01/image-20.png?w=1024)](/uploads/2021/01/image-20.png)



Inside that For Each loop, add an Append to Array variable action. In this action we will build a JSON object, returning our chosen attributes (you can change to whatever you want), and selecting the properties from the value that was parsed:


[![](/uploads/2021/01/image-21.png?w=645)](/uploads/2021/01/image-21.png)



Do the exact same thing for the user devices:


[![](/uploads/2021/01/image-22.png?w=651)](/uploads/2021/01/image-22.png)



Now, on each side of the condition, add a response action, that will return the ManagedDevices array variable, this will be returned as a JSON som set the Content-Type to application/json:


[![](/uploads/2021/01/image-24.png?w=1024)](/uploads/2021/01/image-24.png)



Finally, remove the default response action that is no longer needed:


[![](/uploads/2021/01/image-25.png?w=1024)](/uploads/2021/01/image-25.png)



The complete Logic App should look like the following now:


[![](/uploads/2021/01/image-26.png?w=1024)](/uploads/2021/01/image-26.png)



As I mentioned earlier, we'll get to the filtering parts later, but now it's time for some testing.



### Testing the Logic App from Postman



In the first part of this blog post article series, [Protect Logic Apps with Azure AD OAuth – Part 1 Management Access | GoToGuy Blog](https://gotoguy.blog/2020/12/31/protect-logic-apps-with-azure-ad-oauth-part-1-management-access/), I described how you could use Postman, PowerShell or Azure CLI to test against REST API's.



Let's test this Logic App now with Postman. Copy the HTTP POST URL:


[![](/uploads/2021/01/image-27.png?w=603)](/uploads/2021/01/image-27.png)



And paste it to Postman, remember to change method to POST:


[![](/uploads/2021/01/image-28.png?w=1024)](/uploads/2021/01/image-28.png)



You can now click Send, and the Logic App will trigger, and should return all your managed devices.



If you want a specific users' managed devices, then you need to go to the Body parameter, and add like the following with an existing user principal name in your organization:


[![](/uploads/2021/01/image-29.png?w=746)](/uploads/2021/01/image-29.png)



You should then be able to get this users' managed devices, for example for my test user this was just a virtual machine with Window 10:


[![](/uploads/2021/01/image-30.png?w=416)](/uploads/2021/01/image-30.png)



And I can verify a successful run from the Logic App history:


[![](/uploads/2021/01/image-31.png?w=927)](/uploads/2021/01/image-31.png)



### Summary so far



We've built a Logic App that uses it's own identity (User Assigned Managed Identity) to access the Microsoft Graph API using Application Permissions to get managed devices for all users or a selected user by UPN. Now it's time to exposing this Logic App as an API son end users can call this securely using Azure AD OAuth.



## Building the Logic App API



When exposing the Logic App as an API, this will be the resource that end users will access and call as a REST API. Consider the following diagram showing the flow for OpenID Connect and OAuth, where Azure AD will be the Authorization Server from where end users can request access tokens where the audience will be the Logic App resource:


[![](/uploads/2021/01/image-32.png?w=619)](/uploads/2021/01/image-32.png)



Our next step will be to create Azure AD App Registrations, and we will start with the App Registration for the resource API.



### Creating App Registration for Logic App API



In your Azure AD tenant, create a new App Registration, and call it something like (YourName) LogicApp API:


[![](/uploads/2021/01/image-33.png?w=822)](/uploads/2021/01/image-33.png)



I will use single tenant for this scenario, leave the other settings as it is and create.



Next, go to Expose an API:


[![](/uploads/2021/01/image-34.png?w=759)](/uploads/2021/01/image-34.png)



Click on Set right next to Application ID URI, and save the App ID URI to your choice. You can keep the GUID if you want, but you can also type any URI value you like here (using api:// or https://). I chose to set the api URI to this:


[![](/uploads/2021/01/image-35.png?w=486)](/uploads/2021/01/image-35.png)



Next we need to add scopes that will be the permissions that delegated end users can consent to. This will be the basis of the authorization checks we can do in the Logic App later.



Add a scope with the details shown below. This will be a scope end users can consent to themselves, but it will only allow them to read their own managed devices:


[![](/uploads/2021/01/image-36.png?w=579)](/uploads/2021/01/image-36.png)



Next, add another Scope, with the following details. This will be a scope that only Admins can consent to, and will be authorized to read all devices:


[![](/uploads/2021/01/image-37.png?w=590)](/uploads/2021/01/image-37.png)



You should now have the following scopes defined:


[![](/uploads/2021/01/image-38.png?w=980)](/uploads/2021/01/image-38.png)



Next, go to the Manifest and change the accessTokenAcceptedVersion from null to 2, this will configure so that Tokens will use the OAuth2 endpoints:


[![](/uploads/2021/01/image-39.png?w=722)](/uploads/2021/01/image-39.png)



That should be sufficient for now. In the next section we will prepare for the OAuth client.



### Create App Registration for the Logic App Client



I choose to create a separate App Registration in Azure AD for the Logic App Client. This will represent the OAuth client that end users will use for OAuth authentication flows and requesting permissions for the Logic App API. I could have configured this in the same App Registration as the API created in the previous section, but this will provide better flexibility and security if I want to share the API with other clients also later, or if I want to separate the permission grants between clients.



Go to App Registrations in Azure AD, and create a new registration calling it something like (yourname) LogicApp Client:


[![](/uploads/2021/01/image-40.png?w=826)](/uploads/2021/01/image-40.png)



Choose single tenant and leave the other settings for now.



After registering, go to API permissions, and click on Add a permission. From there you can browse to "My APIs" and you should be able to locate the (yourname) Logic API. Select to add the delegated permissions as shown below:


[![](/uploads/2021/01/image-41.png?w=841)](/uploads/2021/01/image-41.png)



These delegated permissions reflect the scopes we defined in the API earlier. Your App registration and API permission should now look like below. NB! Do NOT click to Grant admin consent for your Azure AD! This will grant consent on behalf of all your users, which will work against our intended scenario later.


[![](/uploads/2021/01/image-42.png?w=1024)](/uploads/2021/01/image-42.png)



Next, we need to provide a way for clients to authenticate using Oauth flows, so go to the Certificates & secrets section. Click to create a Client secret, I will name my secret after where I want to use it for testing later (Postman):


[![](/uploads/2021/01/image-43.png?w=537)](/uploads/2021/01/image-43.png)



Make sure you copy the secret value for later:


[![](/uploads/2021/01/image-44.png?w=730)](/uploads/2021/01/image-44.png)



(Don't worry, I've already invalidated the secret above and created a new one).



Next, go to Authentication. We need to add a platform for authentication flows, so click Add a platform and choose Web. For using Postman later for testing, add the following as Redirect URI: **https://oauth.pstmn.io/v1/callback**


[![](/uploads/2021/01/image-45.png?w=581)](/uploads/2021/01/image-45.png)



Next, we will also provide another test scenario using PowerShell or Azure CLI client, so click on Add a platform one more time, this time adding Mobile desktop and apps as platform and use the following redirect URI: **urn:ietf:wg:oauth:2.0:oob**


[![](/uploads/2021/01/image-46.png?w=571)](/uploads/2021/01/image-46.png)



Your platform configuration should now look like this:


[![](/uploads/2021/01/image-47.png?w=1016)](/uploads/2021/01/image-47.png)



Finally, go to advanced and set yes to allow public client flows, as this will aid in testing from PowerShell or Azure CLI clients later:


[![](/uploads/2021/01/image-48.png?w=701)](/uploads/2021/01/image-48.png)



Now that we have configured the necessary App registrations, we can set up the Azure AD OAuth Authorization Policy for the Logic App.



### Configuring Azure AD OAuth Authorization Policy for Logic App



Back in the Logic App, create an Azure AD Authorization Policy with issuer and audience as shown below:


[![](/uploads/2021/01/image-62.png?w=924)](/uploads/2021/01/image-62.png)



Note the Claims values:



- Issuer: https://login.microsoftonline.com/{tenantId}/v2.0
- Audience: {app id for logic app api app registration}



We are using the v2.0 endpoint as we configured in the manifest of the App Registration that accessTokenAcceptedVersion should be 2. (as opposed to v1.0 issuer that would be in the format https://sts.windows.net/{tenantId}/). And the Audience claim would be our configured API App ID. (for v1.0 the audience would be the App ID URI, like api://elven-logicapp-api).



Save the Logic App, and we can now start to do some testing where we will use the client app registration to get an access token for the Logic App API resource.



### Testing with Postman Client



The first test scenario we will explore is using Postman Client and the Authorization Code flow for getting the correct v2.0 Token.



A recommended practice when using Postman and reusing variable values is to create an Environment. I've created this Environment for storing my Tenant ID, Client ID (App ID for the Client App Registration) and Client Secret (the secret I created for using Postman):


[![](/uploads/2021/01/image-50.png?w=609)](/uploads/2021/01/image-50.png)



Previously in this blog article, we tested the Logic App using Postman. On that request, select the Authorization tab, and set type to OAuth 2.0:


[![](/uploads/2021/01/image-51.png?w=305)](/uploads/2021/01/image-51.png)



Next, under Token configuration add the values like the following. Give the Token a recognizable name, this is just for Postman internal refererence. Make sure that the Grant Type is Authorization Code. Note the Callback URL, this is the URL we configured for the App registration and Callback Url. In the Auth and Access Token URL, configure the use of the v2.0 endpoints, using TenantID from the environment variables. (Make sure to set the current environment top right). And for Client ID and Client Secret these will also refer to the environment variables:


[![](/uploads/2021/01/image-52.png?w=920)](/uploads/2021/01/image-52.png)



One important step remains, and that is to correctly set the scope for the access token. Using something like user.read here will only produce an Access Token for Microsoft Graph as audience. So we need to change to the Logic App API, and the scope for ManagedDevices.Read in this case:


[![](/uploads/2021/01/image-53.png?w=794)](/uploads/2021/01/image-53.png)



Let's get the Access Token, click on the Get New Access Token button:


[![](/uploads/2021/01/image-55.png?w=1024)](/uploads/2021/01/image-55.png)



A browser window launches, and if you are not already logged in, you must log in first. Then you will be prompted to consent to the permission as shown below. The end user is prompted to consent for the LogicApp API, as well as basic OpenID Connect consents:


[![](/uploads/2021/01/image-63.png?w=442)](/uploads/2021/01/image-63.png)



After accepting, a popup will try to redirect you to Postman, so make sure you don't block that:


[![](/uploads/2021/01/image-57.png?w=1024)](/uploads/2021/01/image-57.png)



Back in Postman, you will see that we have got a new Access Token:


[![](/uploads/2021/01/image-58.png?w=582)](/uploads/2021/01/image-58.png)



Copy that Access Token, and paste it into a JWT debugger like [jwt.ms](https://jwt.ms) or [jwt.io](https://jwt.io). You should see in the data payload that the claims for audience and issuer is the same values we configured in the Logic App Azure AD OAuth policy:


[![](/uploads/2021/01/image-59.png?w=548)](/uploads/2021/01/image-59.png)



Note also the token version is 2.0.



Click to use the Token in the Postman request, it should populate this field:


[![](/uploads/2021/01/image-60.png?w=940)](/uploads/2021/01/image-60.png)



Before testing the request, remember to remove the SAS query parameters from the request, so that sv, sp and sig are not used with the query for the Logic App:


[![](/uploads/2021/01/image-54.png?w=610)](/uploads/2021/01/image-54.png)



Now, we can test. Click Send on the Request. It should complete successfully with at status of 200 OK, and return the managed device details:


[![](/uploads/2021/01/image-61.png?w=1024)](/uploads/2021/01/image-61.png)



Let's add to the permission scopes, by adding the ManagedDevices.Read.All:


[![](/uploads/2021/01/image-64.png?w=1024)](/uploads/2021/01/image-64.png)



Remember just to have a blank space between the scopes, and then click Get New Access Token:


[![](/uploads/2021/01/image-65.png?w=456)](/uploads/2021/01/image-65.png)



If I'm logged on with a normal end user, I will get the prompt above that I need admin privileges. If I log in with an admin account, this will be shown:


[![](/uploads/2021/01/image-66.png?w=428)](/uploads/2021/01/image-66.png)



Note that I can now do one of two actions:



1. I can consent only on behalf of myself (the logged in admin user), OR..
2. I can consent on behalf of the organization, by selecting the check box. This way all users will get that permission as well.



Be very conscious when granting consents on behalf of your organization.



At this point the Logic App will authorize if the Token is from the correct issuer and for the correct audience, but the calling user can still request any managed device or all devices. Before we get to that, I will show another test scenario using a public client like PowerShell.



### Testing with PowerShell and MSAL.PS



MSAL.PS is a perfect companion for using MSAL (Microsoft Authentication Library) to get Access Tokens in PowerShell. You can install MSAL.PS from PowerShellGallery using `Install-Module MSAL.PS`.



The following commands show how you can get an Access Token using MSAL.PS:



```powershell
# Set Client and Tenant ID
$clientID = "cd5283d0-8613-446f-bfd7-8eb1c6c9ac19"
$tenantID = "104742fb-6225-439f-9540-60da5f0317dc"

# Get Access Token using Interactive Authentication for Specified Scope and Redirect URI (Windows PowerShell)
$tokenResponse = Get-MsalToken -ClientId $clientID -TenantId $tenantID -Interactive -Scope 'api://elven-logicapp-api/ManagedDevices.Read' -RedirectUri 'urn:ietf:wg:oauth:2.0:oob'

# Get Access Token using Interactive Authentication for Specified Scope and Redirect URI (PowerShell Core)
$tokenResponse = Get-MsalToken -ClientId $clientID -TenantId $tenantID -Interactive -Scope 'api://elven-logicapp-api/ManagedDevices.Read' -RedirectUri 'http://localhost'
```



MSAL.PS can be used both for Windows PowerShell, and for PowerShell Core, so in the above commands, I show both. Note that the redirect URI for MSAL.PS on PowerShell Core need to be http://localhost. You also need to add that redirect URI to the App Registration:


[![](/uploads/2021/01/image-67.png?w=521)](/uploads/2021/01/image-67.png)



Running the above command will prompt an interactive logon, and should return a successful response saved in the $tokenResponse variable.



We can verify the response, for example checking scopes or copying the Access Token to the clipboard so that we can check the token in a JWT debugger:



```powershell
# Check Token Scopes
$tokenResponse.Scopes

# Copy Access Token to Clipboard
$tokenResponse.AccessToken | Clip
```



In the first blog post of this article series I covered how you can use Windows PowerShell and Core to use Invoke-RestMethod for calling the Logic App, here is an example where I call my Logic App using the Access Token (in PowerShell Core):



```powershell
# Set variable for Logic App URL
$logicAppUrl = "https://prod-05.westeurope.logic.azure.com:443/workflows/d429c07002b44d63a388a698c2cee4ec/triggers/request/paths/invoke?api-version=2016-10-01"

# Convert Access Token to a Secure String for Bearer Token
$bearerToken = ConvertTo-SecureString ($tokenResponse.AccessToken) -AsPlainText -Force

# Invoke Logic App using Bearer Token
Invoke-RestMethod -Method Post -Uri $logicAppUrl -Authentication OAuth -Token $bearerToken
```



And I can verify that it works:


[![](/uploads/2021/01/image-68.png?w=960)](/uploads/2021/01/image-68.png)



Great. I now have a couple of alternatives for calling my Logic App securely using Azure AD OAuth. In the next section we will get into how we can do authorization checks inside the Logic App.



## Authorization inside Logic App



While the Logic App can have an authorization policy that verifies any claims like issuer and audience, or other custom claims, we cannot use that if we want to authorize inside the logic app based on scopes, roles etc.



In this section we will look into how we can do that.



### Include Authorization Header in Logic Apps



First we need to include the Authorization header from the OAuth access token in the Logic App. To do this, open the Logic App in code view, and add the operationOptions to IncludeAuthorizationHeadersInOutputs for the trigger like this:



```json
        "triggers": {
            "manual": {
                "inputs": {
                    "schema": {}
                },
                "kind": "Http",
                "type": "Request",
                "operationOptions": "IncludeAuthorizationHeadersInOutputs"
            }
        }
```



This will make the Bearer Token accessible inside the Logic App, as explained in detail in my previous post: [Protect Logic Apps with Azure AD OAuth – Part 1 Management Access | GoToGuy Blog](https://gotoguy.blog/2020/12/31/protect-logic-apps-with-azure-ad-oauth-part-1-management-access/). There I also showed how to decode the token to get the readable JSON payload, so I need to apply the same steps here:


[![](/uploads/2021/01/image-69.png?w=651)](/uploads/2021/01/image-69.png)



After applying the above steps, I can test the Logic App again, and get the details of the decoded JWT token, for example of interest will be to check the scopes:


[![](/uploads/2021/01/image-70.png?w=637)](/uploads/2021/01/image-70.png)



### Implement Logic to check the Scopes



When I created the LogicApp API app registration, I added two scopes: ManagedDevices.Read and ManagedDevices.Read.All. The authorization logic I want to implement now is to only let users calling the Logic App and that has the scope ManagedDevices.Read.All to be able to get ALL managed devices, or to get managed devices other than their own devices.



The first step will be to check if the JWT payload for scope "scp" contains the ManagedDevices.Read.All. Add a Compose action with the following expression:


[![](/uploads/2021/01/image-71.png?w=635)](/uploads/2021/01/image-71.png)



```text
contains(outputs('Base64_to_String_Json').scp,'ManagedDevices.Read.All')
```



This expression will return either **true** or **false** depending on the scp value.



Next after this action, add a Condition action, where we will do some authorization checks. I have created two groups of checks, where one OR the other needs to be true.


[![](/uploads/2021/01/image-72.png?w=679)](/uploads/2021/01/image-72.png)



Here are the details for these two groups:



- Group 1 (checks if scp does not contain ManagedDevices.Read.All and calling user tries to get All managed devices):
  - `Outputs('Check_Scopes') = false`
  - `empty(triggerBody()?['userUpn']) = true`
- Group 2 (checks if scp does not contain ManagedDevices.Read.All, and tries to get managed devices for another user than users' own upn):
  - `Outputs('Check_Scopes') = false`
  - `triggerBody()?['userUpn'] != Outputs('Base64_to_String_Json')['preferred_username']`



If either of those two groups is True, then we know that the calling user tries to do something the user is not authorized to do. This is something we need to give a customized response for. So inside the True condition, add a new Response action with something like the following:


[![](/uploads/2021/01/image-74.png?w=616)](/uploads/2021/01/image-74.png)



I'm using a status code of 403, meaning that the request was successfully authenticated but was missing the required authorization for the resource.



Next, add a Terminate action, so that the Logic App stops with a successful status. Note also that on the False side of the condition, I leave it blank because I want it to proceed with the next steps in the Logic Apps.


[![](/uploads/2021/01/image-73.png?w=1024)](/uploads/2021/01/image-73.png)



### Test the Authorization Scope Logic



We can now test the authorization scopes logic implemented above. In Postman, either use an existing Access Token or get a new Token that only include the ManagedDevices.Read scope.



Then, send a request with an empty request body. You should get the following response:


[![](/uploads/2021/01/image-75.png?w=998)](/uploads/2021/01/image-75.png)



Then, try another test, this time specifying another user principal name than your own, which also should fail:


[![](/uploads/2021/01/image-76.png?w=999)](/uploads/2021/01/image-76.png)



And then test with your own user principal name, which will match the 'preferred\_username' claim in the Access Token, this should be successful and return your devices:


[![](/uploads/2021/01/image-77.png?w=975)](/uploads/2021/01/image-77.png)



Perfect! It works as intended, normal end users can now only request their own managed devices.



Let's test with an admin account and the ManagedDevices.Read.All scope. In Postman, add that scope, and get a new Access Token:


[![](/uploads/2021/01/image-78.png?w=891)](/uploads/2021/01/image-78.png)



When logging in with a user that has admin privileges you will now get a Token that has the scope for getting all devices, for which your testing should return 200 OK for all or any users devices:


[![](/uploads/2021/01/image-79.png?w=999)](/uploads/2021/01/image-79.png)



### Adding Custom Claims to Access Token



In addition to the default claims and scopes in the Access Token, you can customize a select set of additional claims to be included in the JWT data payload. Since the Access Token is for the resource, you will need to customize this on the App Registration for the LogicApp API.



In Azure AD, select the App Registration for the API, and go to API permissions first. You need to add the OpenID scopes first. Add the following OpenID permissions:


[![](/uploads/2021/01/image-80.png?w=418)](/uploads/2021/01/image-80.png)



Your API App Registration should look like this:


[![](/uploads/2021/01/image-81.png?w=811)](/uploads/2021/01/image-81.png)



Next, go to Token configuration. Click Add optional claim, and select Access Token. For example you can add the ipaddr and upn claims as I have done below:


[![](/uploads/2021/01/image-82.png?w=570)](/uploads/2021/01/image-82.png)



Note the optional claims listed for the resource API registration:


[![](/uploads/2021/01/image-83.png?w=1024)](/uploads/2021/01/image-83.png)



Next time I get a new access token, I can see that the claims are there:


[![](/uploads/2021/01/image-84.png?w=517)](/uploads/2021/01/image-84.png)



### Summary of User Authorization so far



What we have accomplished now is that users can get an Access Token for the Logic App API resource. This is the first requirement for users to be able to call the Logic App, that they indeed have a Bearer Token in the Authorization Header that includes the configured issuer and audience.



In my demos I have shown how to get an access token using Postman (Authorization Code Flow) and a Public Client using MSAL.PS. But you can use any kind of Web application, browser/SPA or, Client App, using any programming libraries that either support MSAL or OpenID Connect and OAuth2. Your solution, your choice ;)



After that I showed how you can use scopes for delegated permissions, and how you can do internal authorization logic in the Logic App depending on what scope the user has consented to/allowed to.



We will now build on this, by looking into controlling access and using application roles for principals.



## Assigning Users and Restricting Access



One of the most powerful aspects of exposing your API using Microsoft Identity Platform and Azure AD is that you now can control who can access your solution, in this case call the Logic App.



Better yet, you can use Azure AD Conditional Access to apply policies for requiring MFA, devices to be compliant, require locations or that sign-ins are under a certain risk level, to name a few.



Let's see a couple of examples of that.



### Require User Assignment



The first thing we need to do is to change the settings for the Enterprise Application. We created an App registration for the LogicApp Client, for users to able to authenticate and access the API. From that LogicApp Client, you can get to the Enterprise Application by clicking on the link for Managed application:


[![](/uploads/2021/01/image-85.png?w=939)](/uploads/2021/01/image-85.png)



In the Enterprise App, go to Properties, and select **User assignment required**:


[![](/uploads/2021/01/image-86.png?w=696)](/uploads/2021/01/image-86.png)



We can now control which users, or groups, that can authenticate to and get access to the Logic App API via the Client:


[![](/uploads/2021/01/image-88.png?w=557)](/uploads/2021/01/image-88.png)



If I try to log in with a user that is not listed under Users and groups, I will get an error message that the "signed in user is not assigned to a role for the application":


[![](/uploads/2021/01/image-87.png?w=964)](/uploads/2021/01/image-87.png)



PS! The above error will show itself a little different based on how you authenticate, the above image is using a public client, if you use Postman, the error will be in the postman console log, if you use a web application you will get the error in the browser etc.



### Configuring Conditional Access for the Logic App



In addition to controlling which users and groups that can access the Logic App, I can configure a Conditional Access policy in Azure AD for more fine grained access and security controls.



In your Azure AD blade, go to Security and Conditional Access. If you already have a CA policy that affects all Applications and Users, for example requiring MFA, your LogicApp API would already be affected by that.



Note that as we are protecting the resource here, your Conditional Access policy must be targeted to the LogicApp API Enterprise App.



Click to create a new policy specific for the Logic App API, as shown below:


[![](/uploads/2021/01/image-91.png?w=600)](/uploads/2021/01/image-91.png)



For example I can require that my Logic App API only can be called from a managed and compliant device, or a Hybrid Azure AD Joined device as shown below:


[![](/uploads/2021/01/image-90.png?w=1024)](/uploads/2021/01/image-90.png)



If I create that policy, and then tries to get an access token using a device that are not registered or compliant with my organization, I will get this error:


[![](/uploads/2021/01/image-92.png?w=454)](/uploads/2021/01/image-92.png)



### Summary of Restricting Access for Users and Groups



With the above steps we can see that by adding an Azure AD OAuth authorization policy to the Logic App, we can control which users and groups that can authenticate to and get an Access Token required for calling the Logic App, and we can use Conditional Access for applying additional fine grained access control and security policies.



So far we have tested with interactive users and delegated permission acccess scenarios, in the next section we will dive into using application access and roles for authorization scenarios.



## Adding Application Access and Roles



Sometimes you will have scenarios that will let application run as itself, like a deamon or service, without requiring an interactive user present.



Comparing that to the OIDC and OAuth flow from earlier the Client will access the Resource directly, by using an Access Token aquired from Azure AD using the Client Credentials Flow:


[![](/uploads/2021/01/clientcredentialsflow.png?w=619)](/uploads/2021/01/clientcredentialsflow.png)



### Using the Client Credentials Flow from Postman



Back in the Postman client, under the Authorization tab, just change the Grant Type to Client Credentials like the following. NB! When using application access, there are no spesific delegated scopes, so you need to change the scope so that it refers to **.default** after the scope URI:


[![](/uploads/2021/01/image-95.png?w=907)](/uploads/2021/01/image-95.png)



Click Get New Access Token, and after successfully authenticating click to Use Token. Copy the Token to the Clipboard, and paste to a JWT debugger. Let's examine the JWT payload:


[![](/uploads/2021/01/image-96.png?w=743)](/uploads/2021/01/image-96.png)



Note that the audience and issuer is the same as when we got an access token for an end user, but also that the JWT payload does not contain any scopes (scp) or any other user identifiable claims.



### Using the Client Credentials Flow from MSAL.PS



To get an Access Token for an application client in MSAL.PS, run the following commands:



```powershell
# Set Client and Tenant ID
$clientID = "cd5283d0-8613-446f-bfd7-8eb1c6c9ac19"
$tenantID = "104742fb-6225-439f-9540-60da5f0317dc"
# Set Client Secret as Secure String (keep private)
$clientSecret = ConvertTo-SecureString ("<your secret in plain text") -AsPlainText -Force

# Get Access Token using Client Credentials Flow and Default Scope
$tokenResponse = Get-MsalToken -ClientId $clientID -ClientSecret $clientSecret -TenantId $tenantID -Scopes 'api://elven-logicapp-api/.default'
```



You can then validate this Token and copy it to a JWT debugger:



```powershell
# Copy Access Token to Clipboard
$tokenResponse.AccessToken | Clip
```


[![](/uploads/2021/01/image-97.png?w=955)](/uploads/2021/01/image-97.png)



### Calling the Logic App using Client Application



We can send requests to the Logic App using an Access Token in an application by including it as a Bearer Token in the Authorization Header exactly the same way we did previously, however it might fail internally if the Logic App processing of the access token fails because it now contains a different payload with claims:


[![](/uploads/2021/01/image-99.png?w=963)](/uploads/2021/01/image-99.png)



Looking into the run history of the Logic App I can see that the reason it fails is that it is missing scp (scopes) in the token.


[![](/uploads/2021/01/image-100.png?w=631)](/uploads/2021/01/image-100.png)



This is expected when authenticating as an application, so we will fix that a little later.



### A few words on Scopes vs. Roles



In delegated users scenarios, permissions are defined as Scopes. When using application permissions, we will be using Roles. Role permissions will always be granted by an admin, and every role permission granted for the application will be included in the token, and they will be provided by the .default scope for the API.



### Adding Application Roles for Applications



Now, let's look into adding Roles to our LogicApp API. Locate the App registration for the API, and go to the **App roles | Preview blade**. (this new preview let us define roles in the GUI, where until recently you had to go to the manifest to edit).


[![](/uploads/2021/01/image-101.png?w=599)](/uploads/2021/01/image-101.png)



Next, click on **Create app role**. Give the app role a display name and value. PS! The value must be unique, so if you already have that value as a scope name, then you need to distinguish it eg. by using Role in the value as I have here:


[![](/uploads/2021/01/image-102.png?w=569)](/uploads/2021/01/image-102.png)



The allowed member types give you a choice over who/what can be assigned the role. You can select either application or user/groups, or both.



Add another App Role as shown below:


[![](/uploads/2021/01/image-103.png?w=573)](/uploads/2021/01/image-103.png)



You should now have the following two roles:


[![](/uploads/2021/01/image-104.png?w=864)](/uploads/2021/01/image-104.png)



### Assigning Roles to Application



I recommend that you create a new App Registration for application access scenarios. This way you can avoid mixing delegated and application permissions in the same app registration, it will make it easier to differentiate user and admins consents, and secret credentials will be easier to separate, and you can use different settings for restricting access using Azure AD Users/Groups and Conditional Access.



So create a new App registration, call it something like (Yourname) LogicApp Application Client:


[![](/uploads/2021/01/image-105.png?w=1024)](/uploads/2021/01/image-105.png)



Choose single tenant and leave the other settings as default. Click Register and copy the Application (Client ID) and store it for later:


[![](/uploads/2021/01/image-106.png?w=1024)](/uploads/2021/01/image-106.png)



Next, go to Certificates & secrets, and create a new Client secret:


[![](/uploads/2021/01/image-107.png?w=1024)](/uploads/2021/01/image-107.png)



Copy the secret and store it for later.



Go to API permissions, click Add a permission, and from My APIs, find the LogicApp API. Add the Application permissions as shown below, these are the App Roles we added to the API earlier:


[![](/uploads/2021/01/image-108.png?w=1024)](/uploads/2021/01/image-108.png)



Under API permissions you can remove the Microsoft Graph user.read permission, it won't be needed here, the two remaining permissions should be:


[![](/uploads/2021/01/image-109.png?w=1024)](/uploads/2021/01/image-109.png)



These you NEED to grant admin consent for, as no interactive user will be involved in consent prompt:


[![](/uploads/2021/01/image-110.png?w=928)](/uploads/2021/01/image-110.png)



The admin consent are granted as shown below:


[![](/uploads/2021/01/image-111.png?w=1024)](/uploads/2021/01/image-111.png)



Now we can test getting access token via this new app registration, either use Postman or MSAL.PS , remember to use the new app (client) id and app (client) secret. I chose to add the two values to my Postman environment like this:


[![](/uploads/2021/01/image-113.png?w=947)](/uploads/2021/01/image-113.png)



Next, change the token settings for Client Credentials flow so that the Client ID and Secret use the new variable names. Click to Get New Access Token:


[![](/uploads/2021/01/image-114.png?w=1024)](/uploads/2021/01/image-114.png)



After successfully getting the access token, click Use Token and copy it to clipboard so we can analyze it in the JWT debugger. From there we can indeed see that the roles claims has been added:


[![](/uploads/2021/01/image-115.png?w=830)](/uploads/2021/01/image-115.png)



We will look for these roles claims in the Logic App later. But first we will take a look at how we can add these roles to users as well.



### Assigning Roles to Users/Groups



Adding roles to users or groups can be used for authorizing access based on the roles claim. Go to the Enterprise App for the Logic App API registration, you can get to the Enterprise App by clicking on the Managed application link:


[![](/uploads/2021/01/image-116.png?w=1024)](/uploads/2021/01/image-116.png)



In the Enterprise App, under Users and Groups, you will already see the ServicePrincipal's for the LogicApp Application Client with the Roles assigned. This is because these role permissions were granted by admin consent:


[![](/uploads/2021/01/image-117.png?w=1024)](/uploads/2021/01/image-117.png)



Click on Add user/group, add for a user in your organization the selected role:


[![](/uploads/2021/01/image-118.png?w=1024)](/uploads/2021/01/image-118.png)



You can add more users or groups to assigned roles:


[![](/uploads/2021/01/image-119.png?w=1024)](/uploads/2021/01/image-119.png)



Lets do a test for this user scenario. We need to do an interactive user login again, so change to using Authorization Code Flow in Postman, and change to the originial ClientID and ClientSecret:


[![](/uploads/2021/01/image-120.png?w=1024)](/uploads/2021/01/image-120.png)



Click to Get New Access Token, authenticate with your user in the browser (the user you assigned a role to), and then use the token and copy it to clipboard. If we now examine that token and look at the JWT data payload, we can see that the user has now a role claim, as well as the scope claim:


[![](/uploads/2021/01/image-121.png?w=804)](/uploads/2021/01/image-121.png)



We can now proceed to adjust the authorization checks in the Logic App.



### Customizing Logic App to handle Roles Claims



Previously in the Logic App we did checks against the scopes (scp claim). We need to do some adjustment to this steps, as it will fail if there are no scp claim in the Token:


[![](/uploads/2021/01/image-122.png?w=941)](/uploads/2021/01/image-122.png)



Change to the following expression, with a if test that returns false if no scp claim, in addition to the original check for scope to be ManagedDevices.Read.All:


[![](/uploads/2021/01/image-123.png?w=1024)](/uploads/2021/01/image-123.png)



This is the expression used above:



```text
if(empty(outputs('Base64_to_String_Json')?['scp']),false,contains(outputs('Base64_to_String_Json').scp,'ManagedDevices.Read.All'))
```



Similary, add a new Compose action, where we will check for any Roles claim.


[![](/uploads/2021/01/image-124.png?w=1024)](/uploads/2021/01/image-124.png)



This expression will also return false if either the roles claim is empty, or does not contain the ManagedDevices.Role.Read.All:



```text
if(empty(outputs('Base64_to_String_Json')?['roles']),false,contains(outputs('Base64_to_String_Json').roles,'ManagedDevices.Role.Read.All'))
```



Next we need to add more checks to the authorization logic. Add a new line to the first group, where we also check the output of the Check Roles action to be false:


[![](/uploads/2021/01/image-125.png?w=675)](/uploads/2021/01/image-125.png)



In the above image I've also updated the action name and comment to reflect new checks.



To the second group, add two more lines, where line number 3 is checking outputs from Check Roles to be false (same as above), and line 4 do a check if the roles claim contains the role ManagedDevices.Role.Read:


[![](/uploads/2021/01/image-126.png?w=630)](/uploads/2021/01/image-126.png)



The complete authorization checks logic should now be:


[![](/uploads/2021/01/image-127.png?w=679)](/uploads/2021/01/image-127.png)



And this is the summary of conditions:



- Group 1 (checks if scp does not contain ManagedDevices.Read.All and roles does not contain ManagedDevices.Role.Read.All and calling user tries to get All managed devices):
  - `Outputs('Check_Scopes') = false`
  - `empty(triggerBody()?['userUpn']) = true`
  - `Outputs('Check_Roles') = false`
- Group 2 (checks if scp does not contain ManagedDevices.Read.All and roles does not contain ManagedDevices.Role.Read.All, and tries to get managed devices for another user than users' own upn, and roles does not contain ManagedDevices.Role.Read):
  - `Outputs('Check_Scopes') = false`
  - `triggerBody()?['userUpn'] != Outputs('Base64_to_String_Json')['preferred_username']`
  - `Outputs('Check_Roles') = false`
  - `contains(outputs('Base64_to_String_Json')?['roles'],'ManagedDevices.Role.Read') = false`



If any of the two groups of checks above returns true, then it means that the request was not authorized. To give a more customized response, change the response action like the following:


[![](/uploads/2021/01/image-128.png?w=650)](/uploads/2021/01/image-128.png)



In the above action I have changed that response is returned as a JSON object, and then changed the body so that it returns JSON data. I have also listed the values from the token that the user/application use when calling the Logic App. The dynamic expression for getting roles claim (for which will be in an array if there are any roles claim) is:  
`if(empty(outputs('Base64_to_String_Json')?['roles']),'',join(outputs('Base64_to_String_Json')?['roles'],' '))`  
And for getting any scopes claim, which will be a text string or null:  
`outputs('Base64_to_String_Json')?['scp']`



### Test Scenario Summary



I'll leave the testing over to you, but if you have followed along and customized the Logic App as I described above, you should now be able to verify the following test scenarios:




| User/App | Scope | Roles | Result |
| --- | --- | --- | --- |
| User | ManagedDevices.Read |  | Can get own managed devices. Not authorized to get all devices or other users' managed devices. |
| User (Admin) | ManagedDevices.Read.All |  | Can get any or all devices. |
| User | ManagedDevices,Read | ManagedDevices.Role.Read | Can get own managed devices. Can get other users' managed devices by userUpn. Not authorized to get all devices. |
| User | ManagedDevices.Read | ManagedDevices.Role.Read.All | Can get any or all devices. |
| Application |  | ManagedDevices.Role.Read | Can any users' managed devices by userUpn. Not authorized to get all devices. |
| Application |  | ManagedDevices.Role.Read.All | Can get any or all devices. |




When testing the above scenarios, you need a new access token using either authorization code flow (user) or client credentials (application). For testing with roles and user scenarios, you can change the role assignments for the user at the Enterprise Application for the LogicAPI API. For testing with roles with application scenarios, make sure that you only grant admin consent for the applicable roles you want to test.



## Final Steps and Summary



This has been quite the long read. The goal of this blog post was to show how your Logic App workflows can be exposed as an API, and how Azure AD OAuth Authorization Policies can control who can send requests to the Logic App as well as how you can use scopes and roles in the Access Token to make authorization decisions inside the Logic App. And even of more importance, integrating with Azure AD let's you control user/group access, as well as adding additional security layer with Conditional Access policies!



My demo scenario was to let the Logic App call Microsoft Graph and return managed devices, which require privileged access to Graph API, and by exposing the Logic App as an API I can now let end users/principals call that Logic App as long as they are authorized to do so using my defined scopes and/or roles. I can easily see several other Microsoft Graph API (or Azure Management APIs, etc) scenarios using Logic App where I can control user access similarly.



Note also that any callers of the Logic App that now will try to call the Logic App using SAS access scheme will fail, as a Bearer Token is expected in the Authorization Header and the custom authorization actions that has been implemented. You might want to implement some better error handling if you like.



There's an added bonus at the end of this article, where I add the filters for getting managed devices. But for now I want to thank you for reading and more article in this series will come later, including:



- Calling Logic Apps protected by Azure AD from Power Platform
- Protecting Logic App APIs using Azure API Management (APIM)



### Bonus read



To complete the filtering of Managed Devices from Microsoft Graph, the Logic App prepared inputs of operatingSystem and osVersion in addition to userUpn. Let's how we can implement that support as well.



After the initialize variable ManagedDevices action, add a Compose action. In this action, which I rename to operatingSystemFilter, I add a long dynamic expression:


[![](/uploads/2021/01/image-129.png?w=860)](/uploads/2021/01/image-129.png)



This expression will check if the request trigger has an operatingSystem value, it not this value will be a empty string, but if not empty the I start building a text string using concat function where I build the filter string. There are some complexities here, amongs others using escaping of single apostroph, by adding another single apostroph etc. But this expression works:



```text
if(empty(triggerBody()?['operatingSystem']),'',concat('/?$filter=operatingSystem eq ''',triggerBody()?['operatingSystem'],''''))
```



Next, add another Compose action and name it operatingSystemVersionFilter. This expression is even longer, checking the request trigger for osVersion, and if empty, it just returns the operatingSystemFilter from the previos action, but if present another string concat where I 'and' with the previous filter:


[![](/uploads/2021/01/image-130.png?w=1024)](/uploads/2021/01/image-130.png)



The expression from above image:



```text
if(empty(triggerBody()?['osVersion']),outputs('operatingSystemFilter'),concat(outputs('operatingSystemFilter'),' and startswith(osVersion,''',triggerBody()?['osVersion'],''')'))
```



We can now add that output to the Graph queries, both when getting all or a specific user's devices:


[![](/uploads/2021/01/image-131.png?w=1024)](/uploads/2021/01/image-131.png)



I can now add operatingSystem and osVersion to the request body when calling the Logic App:


[![](/uploads/2021/01/image-132.png?w=391)](/uploads/2021/01/image-132.png)



And if I check the run history when testing the Logic App, I can see that the filter has been appended to the Graph query:


[![](/uploads/2021/01/image-133.png?w=971)](/uploads/2021/01/image-133.png)



You can if you want also build more error handling logic for when if users specify the wrong user principalname, or any other filtering errors that may occur because of syntax etc.



That concludes the bonus tip, thanks again for reading :)
