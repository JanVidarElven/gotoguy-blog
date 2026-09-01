---
title: "Creating an Azure AD Protected API in Azure in an hour!"
date: 2021-12-22T10:48:00Z
draft: false
slug: "creating-an-azure-ad-protected-api-in-azure-in-a-school-hour"
categories:
  - "Azure"
  - "Azure AD"
  - "Azure Function"
  - "Azure REST API"
  - "Managed Identites"
  - "OAuth2"
---

This blog post will accompany my contribution for Festive Tech Calendar 2021, where I on the 22nd of December will present a live stream & interactive session where I in just a school hour will show you how you can create your own API in Azure and protect it with Azure AD using Oauth2. API's can be anything you want, but let's keep it festive!



This is some of the content I will cover in this blog post:



- What is an API anyway?
- What can you use in Azure to create APIs?
- Get your tools out!
- Why do we want to secure it?
- How can we use Azure AD to secure it?



## What is an API?



API, Application Programming Interface, is a middle layer of logic between the consumer (represented by a client), and the data and/or services that the client needs to access. An relevant example is a web application that reads and writes data to a database. To be able to read and write data in that database, you must provide a secure and consistent way to do that, and that is where the API's come into play. By calling the API the Web Application don't have to manage the logic and security of operating against the database, the API will handle all of that by exposing methods the client can send requests to and receive responses from.



There are different ways of how you can communicate with an API, or if it will be available on a public network or private, but it is common today that APIs are web based and openly accessible. In general, these APIs should adhere to:



- **Platform independence**. Any clients should be able to call it, and that means using standard protocols.
- **Service evolution**. The Web API should be able to evolve and add functionality without breaking the clients.



### The RESTful API



REST, Representational State Transfer, is an architectural approach to designing web services. Most common REST API implementations use HTTP as the application protocol, making it easier to achieve the goal of platform independence.



Some of the most important guidelines for designing REST APIs for HTTP are (using Microsoft Graph API as examples):



- The use of resources: https://<api.fqdn>/<version>/<resource>  

  For example, the Microsoft Graph API are a good example, here where users are a resource:  

  https://graph.microsoft.com/v1.0/**users**
- Using identifiers for specific resources, for example:  

  https://graph.microsoft.com/v1.0/users/**<userid>**
- Data exchange usually done by JSON as exchange format for representing resources, both in request and response formats.
- HTTP verbs for operations (GET, POST, PUT, PATCH, DELETE)
- REST APIs are stateless, in that requests can be run independently of each other.



If you want to read more on this topic, I highly recommend this article: <https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design>.



In this blog post I will build on these design principles.



## Using Azure to create your own APIs



Using Azure Resources you have a range of different solutions from where you can create your own APIs. You can develop and publish APIs using App Services, you can use Azure API Management, or you can start a little more simpler with Azure Serverless technologies like Azure Functions or Logic Apps.



In this blog post I will use Azure Functions for my demo scenario, creating a Serverless API that will receive and respond to HTTP requests. Azure Functions supports all the architectural guidelines from above, including connections to backend services like a database.



### Demo Scenario



I will build the following scenario for the solution I want to demo. The theme will be Festive and build a solution for registering and managing Christmas Whishes!



1. A CosmosDB Account and Database, which will store whishes as document items.
2. An Azure Function App, with Functions that will serve as the API, and will:
   - Implement methods to GET whishes, create new whishes (POST), change existing (PUT) or DELETE whishes.
   - Provide a secure connection to the Cosmos DB account to update items accordingly.
3. An Azure App Service, running a web site as frontend, from where users will get, create, update and delete whishes, and this will use the Azure Functions API.



The following simple diagram shows an architectural overview over this solution as described above:


![Diagram displaying the parts of the application: web site, the API using Azure Functions, and the database with the products data](https://docs.microsoft.com/en-us/learn/modules/build-api-azure-functions/media/product-manager-all-parts.svg)



Later in this blog post I will show how we can add Azure AD Authentication and Authorization to this solution, and securing the API.



## Get your tools ready!



I will use Visual Studio Code and Azure Functions Core Tools to create, work with and publish the serverless API, in addition to creating a frontend web based on Node.js.



If you want to follow along and recreate this scenario in your environment, make sure you have the following installed:



1. Visual Studio Code. <https://code.visualstudio.com/>
2. Node.js. <https://nodejs.org/en/>
3. Azure Function Core Tools. <https://github.com/Azure/azure-functions-core-tools>
4. Azure Function Extension. <https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions>
5. In addition, I will build the API logic using Azure Functions PowerShell so you need to have [PowerShell Core](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell?view=powershell-7.2) installed as well.



In addition to the above tools, you will also need access to an Azure AD tenant where you can create App Registrations for Azure AD Authentication, as well as an Azure Subscription where you can create the required resources.



If you don't have access to an Azure Subscription with at least Contributor access for a Resource Group, you can develop and run parts of the solution locally, but then you would not be able to fully complete all parts of the authentication and authorization requirements.



After making sure you have those components installed, configured or updated, you can proceed to the next steps.



### Download Repository set up Resources



I have the following GitHub repository set up with starting resources: <https://github.com/JanVidarElven/build-azure-ad-protected-api-azure-functions-festivetechcalendar>



You can download all the files using a ZIP file, or you can fork and/or clone the repository if you have your own GitHub account.



After the repository has been downloaded, open the workspace file "christmas-whishes.code-workspace" in VS Code, you should now see two folders, one for api and one for frontend.



The api folder contains the Functions Project, and the Functions I have pre-created and that we will build on later. The frontend folder contains the node.js website with the html file and a javascript file for connecting to the api logic.


[![](/uploads/2021/12/image.png?w=412)](/uploads/2021/12/image.png)



Before we proceed with configuring the local project, we need to create the dependant Azure Resources like the Cosmos DB and Functions App.



### Set up Azure Resources



In my repository you downloaded / cloned above, you will find instructions and some Az PowerShell samples for creating the required resources, this will include:



- Create a Resource Group "rg-festivetechcalendar" in your chosen region (you can change the rg name to something other of your choice).
- Create a Azure Function App of <yourid>-fa-festivetechcalendar-api in the above resource group. Choose your region and a consumption plan.
- Create a Cosmos DB account in your region and in the above resource group with the name <-yourid>-festivetechcalendar-christmaswhishes, opt in for free tier.
- In the Cosmos DB account, create a new database called "festivetechcalendar" and a container named "whishes" using /id as partition key.
- In the above resource group, create an App Service for the frontend web site, with the name <yourid>-festivetechcalendar-christmaswhishes, using Node and Node 14 LTS as runtime and Linux as operationg system. If a Free plan is available in your region, you can use that, but else use a low cost dev/test plan.



PS! You can use other names for the above resources, but then you need to make sure that you change this in the repository code you will be working from.



In addition to the above resources, some supporting services like App Plans, Applications Insights and Storage Accounts are created as part of the process.



### Connect to the Azure Account in VS Code



Using the Azure Accont extension i VS Code, make sure that you are signed in to the correct subscription, you should be able to see the above Function App for example, like in my environment:


[![](/uploads/2021/12/image-1.png?w=468)](/uploads/2021/12/image-1.png)



PS! If you, like I have access to many subscriptions in different tenants, it might be worthwhile to add this azure.tenant setting to the VS Code workspace file:



`"settings": {`   
`"azure.tenant": "yourtenant.onmicrosoft.com",`



### Configure the Bindings and make the API RESTful



Next we will make some changes to the Azure Functions API, so that we can successfully connect to the Cosmos DB and make the API RESTful following the architectural guidelines.



First we need to create/update a **local.settings.json** file in the api folder, where you need the following settings, replace the **Festive\_CosmosDB** connection string with your own connection string from your Azure Resource:


> `{  
> "IsEncrypted": false,  
> "Values": {  
> "AzureWebJobsStorage": "",  
> "FUNCTIONS_WORKER_RUNTIME_VERSION": "~7",  
> "FUNCTIONS_WORKER_RUNTIME": "powershell",  
> "Festive_CosmosDB": "AccountEndpoint=https://festivetechcalendar-christmaswhishes.documents.azure.com:443/;AccountKey=jnrSbHmSDDDVzo1St4mWSHn……;"  
> },  
> "Host": {  
> "CORS": "*"  
> }  
> }`



Open a new Terminal Window in VS Code (if not already open) and choose the api folder. Then run the following command **func start**. This will start up the Functions Core Tools runtime and enable to send requests to the API locally. Typically when you create and run functions locally the will show something like the following:


[![](/uploads/2021/12/image-2.png?w=834)](/uploads/2021/12/image-2.png)



You will see from above that I have created from before 4 functions:



- CreateWhish: Function for creating new Christmas Whishes
- DeleteWhish: Function for Deleting Whishes
- GetWhishes: Function for Getting Whishes
- UpdateWhish: Function for Updating Whishes



All of these functions are using an HTTP trigger for request and response. In addition I have used a CosmosInput trigger for getting existing items from the DB (via the connection string defined in local.settings.json) and CosmosOutput trigger for sending new or updated items back to the DB.



Deleting items from Cosmos DB is a little bit more trickier though, as the CosmosOutput trigger does not support deletes. So in that case I chose to do the delete via Cosmos REST API, using Managed Identity for the Function App, or the logged on user locally. More on that later.



First, lets make the APIs RESTful. As I mentioned earlier, the API should make use of resources. And while I have methods for CreateWhish, DeleteWhish and so on, I want to change this so that I will focus on the resource whish, and use the correct verbs for the operations I want. I will change the API to the following:



- GET /api/whish (getting all whishes)
- POST /api/whish (creating a new whish)
- DELETE /api/whish (delete a whish)
- PUT /api/whish (change a whish)



That should be much better! I should also specify and existing id for DELETE or PUT, and make it possible to GET a specific whish also by id. So let's define that as well:



- GET /api/whish/{id?}
- POST /api/whish
- DELETE /api/whish/{id}
- PUT /api/whish/{id}



The question mark after GET /api/whish/{id?} means that it is optional (for getting all whishes) or a specific whish by id. DELETE and PUT should always have an id in the request.



Let's make this changes in the Functions. Inside every function there is a **function.json** file, which defines all the input and output bindings. For doing the above changes, we will focus specifically on the HttpTrigger In binding. Two changes must be made, one is to change the method (the http verb) and the other is to add a "**route**" setting. So for example for GetWhishes, change the first binding to:



```json
{
  "bindings": [
    {
      "authLevel": "function",
      "type": "HttpTrigger",
      "direction": "in",
      "name": "Request",
      "methods": [
        "get"
      ],
      "route": "whish/{id?}"      
    },
```



Then the CreateWhish should be changed to:



```json
{
  "bindings": [
    {
      "authLevel": "function",
      "type": "HttpTrigger",
      "direction": "in",
      "name": "Request",
      "methods": [
        "post"
      ],
      "route": "whish"      
    },
```



The DeleteWhish HttpTrigger in should be changed to:



```json
{
  "bindings": [
    {
      "authLevel": "function",
      "type": "HttpTrigger",
      "direction": "in",
      "name": "Request",
      "methods": [
        "delete"
      ],
      "route": "whish/{id}"      
    },
```



And last the UpdateWhish HttpTrigger in to be changed to:



```json
{
  "bindings": [
    {
      "authLevel": "function",
      "type": "HttpTrigger",
      "direction": "in",
      "name": "Request",
      "methods": [
        "put"
      ],
      "route": "whish/{id}"
    },
```



Now, run func start again in the terminal windows, and the Functions should now show the following:


[![](/uploads/2021/12/image-3.png?w=794)](/uploads/2021/12/image-3.png)



The API is now much more RESTful, each method is focused on the resource **whish**, and using the correct http verbs for the operations.



### The case of the Delete of Item in Cosmos DB



As mentioned earlier the CosmosOutput binding handles updates and creation of new items in the Cosmos DB, but not deleting. Barbara Forbes has a nice and more detailed walkthrough of how to use the Cosmos DB input and output bindings [in this blog post](https://4bes.nl/2020/05/03/configure-azure-powershell-function-apps-with-cosmos-db/), but for deletes I did it another way. Let's look into that.



The code in run.ps1 for DeleteWhish function starts with the following, getting the input bindings and retrieving the whish by id from the CosmosInput:



```powershell
using namespace System.Net

# Input bindings are passed in via param block.
param($Request, $TriggerMetadata, $CosmosInput)

# Write to the Azure Functions log stream.
Write-Host "PowerShell HTTP trigger function processed a request to delete a whish."

# Check id and get item to delete
If ($Request.Params.id) {
    $whish = $CosmosInput | Where-Object { $_.id -eq $Request.Params.id}
}
```



I now have the item I want to delete. Next I build the document URI for the item I want to delete using the Cosmos DB REST API:



```powershell
# Build the Document Uri for Cosmos DB REST API
$cosmosConnection = $env:Festive_CosmosDB -replace ';',"`r`n" | ConvertFrom-StringData
$documentUri = $cosmosConnection.AccountEndpoint + "dbs/" + "festivetechcalendar" + "/colls/" + "whishes" + "/docs/" + $whish.id
```



Note that I have hardcoded my Database (festivetechcalendar) and container (whishes) above, you might want to change that in your environment if different. Next I check if the Azure Function is running in the Function App in Azure, or locally inside my VS Code. If running in the Function App I will use the Managed Identity to connect to the resource https://cosmos.azure.com and get an access token. If I run locally in VS Code I'll just get an acces token using Get-AzAccessToken, providing that I have connected to my tenant and subscription earlier using Login-AzAccount.



NB! This operation requires RBAC Data Operations role assigment, more on that later!



```powershell
# Check if running with MSI (in Azure) or Interactive User (local VS Code)
If ($env:MSI_SECRET) {
    
    # Get Managed Service Identity from Function App Environment Settings
    $msiEndpoint = $env:MSI_ENDPOINT
    $msiSecret = $env:MSI_SECRET

    # Specify URI and Token AuthN Request Parameters
    $apiVersion = "2017-09-01"
    $resourceUri = "https://cosmos.azure.com"
    $tokenAuthUri = $msiEndpoint + "?resource=$resourceUri&api-version=$apiVersion"

    # Authenticate with MSI and get Token
    $tokenResponse = Invoke-RestMethod -Method Get -Headers @{"Secret"="$msiSecret"} -Uri $tokenAuthUri
    $bearerToken = $tokenResponse.access_token
    Write-Host "Successfully retrieved Access Token Cosmos Document DB API using MSI."

} else {
    # Get Access Token for the interactively logged on user in local VS Code
    $accessToken = Get-AzAccessToken -TenantId elven.onmicrosoft.com -ResourceUrl "https://cosmos.azure.com"
    $bearerToken = $accessToken.Token
}
```



Then, when I got the Access Token for the Cosmos DB REST API, I can proceed to delete the document item. There are some special requirements for the headers to include the Authorization header, version and partition key as shown below. Then I can Invoke-RestMethod with Delete operation on the Document Uri and with the right Headers. Note also that PowerShell Core wasn't to happy with this header format, so I had to use the SkipHeaderValidation:



```powershell
# Prepare the API request to delete the document item
$partitionKey = $whish.id
$headers = @{
    'Authorization' = 'type=aad&ver=1.0&sig='+$bearerToken
    'x-ms-version' = '2018-12-31'
    'x-ms-documentdb-partitionkey' = '["'+$partitionKey+'"]'
}

Invoke-RestMethod -Method Delete -Uri $documentUri -Headers $headers -SkipHeaderValidation

$body = "Whish with Id " + $whish.id + " deleted successfully."

# Associate values to output bindings by calling 'Push-OutputBinding'.
Push-OutputBinding -Name Response -Value ([HttpResponseContext]@{
    StatusCode = [HttpStatusCode]::OK
    Body = $body
})
```



Now, for the user getting the access token, either interactively or the Managed Identity, you will need to assign roles for Data Operations. This is all documented here: <https://docs.microsoft.com/en-us/azure/cosmos-db/how-to-setup-rbac>, but the following commands should get you started:



```powershell
$subscriptionId = "<subscriptionId_for_Azure_subscription_for_resources>"
Set-AzContext -Subscription $subscriptionId
$principalUpn = "<user_upn_for_member_or_guest_to_assign_access>"
$managedIdentityName = "<name_of_managed_identity_connected_to_function_app>"

$resourceGroupName = "rg-festivetechcalendar"
$accountName = "festivetechcalendar-christmaswhishes"
$readOnlyRoleDefinitionId = "00000000-0000-0000-0000-000000000001" 
$contributorRoleDefinitionId = "00000000-0000-0000-0000-000000000002"

$principalId = (Get-AzADUser -UserPrincipalName $principalUpn).Id
New-AzCosmosDBSqlRoleAssignment -AccountName $accountName `
    -ResourceGroupName $resourceGroupName `
    -RoleDefinitionId $contributorRoleDefinitionId `
    -Scope "/" `
    -PrincipalId $principalId

$servicePrincipalId = (Get-AzADServicePrincipal -DisplayName $managedIdentityName).Id
New-AzCosmosDBSqlRoleAssignment -AccountName $accountName `
    -ResourceGroupName $resourceGroupName `
    -RoleDefinitionId $contributorRoleDefinitionId `
    -Scope "/" `
    -PrincipalId $servicePrincipalId
```



In my commands from above I have assigned both my own user (running locally in VS Code) and the Managed Identity for the Function App to the Contributor Role.



PS! Don't forget to enable Managed Identity for the Function App:


[![](/uploads/2021/12/image-4.png?w=620)](/uploads/2021/12/image-4.png)



That means that the API is now finished in this first phase, and we can **deploy** them to the Function App.


[![](/uploads/2021/12/image-5.png?w=478)](/uploads/2021/12/image-5.png)



After you deploy the functions to the Function App, also make sure to update the app settings.



I won't go into details for testing this now, I often use Postman for these testing scenarios, both locally and remotely to the Function App, but if you want to see this from a recording of my session at **Festive Tech Calendar**, you can find that here: <https://www.youtube.com/watch?v=5zLbksF0Ejg>.



### The Web Frontend



A few words about the web frontend also, as I mentioned earlier this is built on Node.js as a Single Page Application (SPA). This means the entire application exists in the browser, there is no backend for the web. All the more reasons for separating the logic and security connections in the API.



The web frontend basically consists of an html page and a javascript file. The javascript file has some methods for using the api, as the screenshot below shows:


[![](/uploads/2021/12/image-6.png?w=1024)](/uploads/2021/12/image-6.png)



There is a API constant that points to the Azure Functions API urls that we saw when running func start. The getWhishes, updateWhish methods and so on use this API and the resource whish, together with the http verbs to send requests and receive responses from the API.



I'm not really a web developer myself, so I have depended on other Microsoft Identity samples and good help from collegueas and community, but I have been able to change the code such that the web frontend you downloaded from the repository earlier now should work with the API locally.



So while you still are running func start from before, open a new terminal window, choosing frontend as the folder, and run:



**npm start**



This will build and start the web frontend locally:


[![](/uploads/2021/12/image-7.png?w=687)](/uploads/2021/12/image-7.png)



You can now go to your browser and use http://localhost:3000, which will show you the start page that will look something like this:


[![](/uploads/2021/12/image-8.png?w=1024)](/uploads/2021/12/image-8.png)



You can now Create a Whish, see existing as they are created, change or delete them, it should work provided you have followed the steps as layed out above.



With the API now working between the frontend and the backend Cosmos DB, we can proceed to secure the API!



## Why secure the API?



The API is important to protect, as it contains connection strings in app settings and a managed idenity that can manipulate the Cosmos DB. While the default mode for functions require a knowledge of a function code query parameter, this will still be exposed in the web frontend code, any user can open this source code and get those URI's and run them from other places.



Another reason is the increasing focus on security and zero trust, where every user and access should be verified and never trusted. For example, runnning requests from another unfamiliar location against the API, and as well the assume breach mindset should make sure that every connection is authenticated and audited.



Authentication is one thing, but also authorization is an important part of API protection. Take this simple, but relevant case of Christmas Whishes: Should really everyone be able to see both your own but also everybody elses whishes? Should you be able to write and delete other users whishes?



For this next scenario we will implement authentication and authorization for this Azure Functions API, using Azure AD and OAuth2.



### How to use Azure AD to protect the API



Azure Active Directory can be the Identity Provider that can require and successfully authenticate users. Azure AD can also expose API scopes (delegated permissions) and roles (application permissions) as needed so that you can use OAuth2 for authorization decicions as well.



We can require authentication on the API, and provide a way for the frontend web to sign users in, consent to permissions that the scopes have defined, and securely call the API. In that way, there is no way an anonymous user can send requests to the API, they have to be authenticated.



We will use Azure AD App Registrations for setting this up. Let's get started.



### Create the API App Registration



We will first create a App Registration for defining the API. In the Azure AD Portal, select new App Registration, give it a name like **FestiveTechCalendar API**, and then select the **multitenant** setting of **accounts in any organizational directory** and **personal Microsoft accounts**, and the click create.



(NB! You can use single-tenant if you want to, then only users in your tenant will be able to authenticate to the API).



Next, go to Expose an API, and first set the Application ID URI to something like the following:


[![](/uploads/2021/12/image-9.png?w=763)](/uploads/2021/12/image-9.png)



Then, we will add the following scopes to be defined by the API:



- access\_as\_user, to let users sign in and access the api as themselves
- Whish.ReadWrite, to let users be able to create, edit, delete or get their own whishes only.
- Whish.ReadWrite.All, with admin consent only, to let privileged users be able to see all users' whishes (for example Santa Claus should have this privilege 🎅🏻)



This should look something like this after:


[![](/uploads/2021/12/image-10.png?w=980)](/uploads/2021/12/image-10.png)



This completes this App Registration for now. We will proceed by creating another App Registration, to be used from the clients.



### Create the Frontend App Registration



Create a new App Registration, with the name for example **FestiveTechCalendar Frontend**, and with the same **multitenant** + **Microsoft personal account** setting as the API app. Click create.



Next, go to API permissions, and click Add a permission, from which you can select own APIs and find the FestiveTechCalendar API app and add our three custom scopes, as shown below:



PS! Do NOT click to grant admin consent for your organization: (I prefer that users consent themselves, providing that they are allowed to do so that is)


[![](/uploads/2021/12/image-12.png?w=1024)](/uploads/2021/12/image-12.png)



Next, under Authentication, click to **Add a platform**, select Single Page Application (SPA) and add http://localhost:3000 as redirect uri:


[![](/uploads/2021/12/image-13.png?w=559)](/uploads/2021/12/image-13.png)



Adding localhost:3000 will make sure that when I run the web frontend locally, I can sign in from there.



Also, add the checkboxes for Access tokens and ID tokens, as we will need this in our scenario with the API:


[![](/uploads/2021/12/image-14.png?w=897)](/uploads/2021/12/image-14.png)



Go back to Overview, and note/copy the Application (Client) ID, you will need that later.



### Azure AD Authentication to the API with Postman



If you want to be able to test secured requests from [Postman](https://www.postman.com/downloads/) client, you can also add the following Web platform in addition to the Single Page Application platform:


[![](/uploads/2021/12/image-15.png?w=720)](/uploads/2021/12/image-15.png)



Add https://oauth.pstmn.io/v1/callback as Redirect URI for Postman requests.



For authenticating with Postman you also need to setup a Client Secret:


[![](/uploads/2021/12/image-16.png?w=979)](/uploads/2021/12/image-16.png)



Take a note/copy of that Secret also, it will be needed for Postman testing later.



For now, this App Registration for the frontend client is finished.



### Require Authentication on Azure Function App



Wiht Azure AD App Registrations set up, we can now proceed to the Function App and require Azure AD Authentication.



Under **Authentication**, click to **Add an identity provider**:


[![](/uploads/2021/12/image-17.png?w=831)](/uploads/2021/12/image-17.png)



Select Microsoft, then pick and existing app registration and find the FestiveTechCalendar Fronted app. Change the Issuer URL to use the common endpoint, as we have configured this to support both multitenant and microsoft accounts:


[![](/uploads/2021/12/image-18.png?w=850)](/uploads/2021/12/image-18.png)



Set restric access to **Require authentication**, and for unauthenticated requests to the API to get a **HTTP 401 Unauthorized**:


[![](/uploads/2021/12/image-19.png?w=865)](/uploads/2021/12/image-19.png)



Click Add to finish adding and configuring the Identity provider, the Function App and the Functions API are now protected!



The last step we need to do, is to configure the allowed audiences for the function app authentication, we need to add the following two audiences, and this is for the API App Registration. For v1.0 token formats, use api://festivetechcalendarapi, for v2.0 token formats (which should be default today), use the App ID for the API App Registration:


[![](/uploads/2021/12/image-25.png?w=721)](/uploads/2021/12/image-25.png)



Note also that for token 2.0 formats the issuer will be https://login.microsoftonline.com/common/v2.0.



### Remove Function Key authentication



Now that the Function App in itself is protected with Azure AD Authentication, we can remove the Function Key authentication. For each of the functions (GetWhishes, UpdateWhish, etc), go into the function.json file, and change the authLevel from **function** to **anonymous**, like below:



```json
{
  "bindings": [
    {
      "authLevel": "anonymous",
      "type": "HttpTrigger",
      "direction": "in",
      "name": "Request",
```



After the functions have been changed, deploy from VS Code to the Function App again.



### Testing Authentication with Postman



We can now try to do some testing against the API from Postman. This isn't something you have to do, but it's nice to use for some evaluating and testing before we proceed to the web frontend.



I have created myself a collection of requests for Festive Tech Calendar in Postman:


[![](/uploads/2021/12/image-20.png?w=298)](/uploads/2021/12/image-20.png)



The local ones use the URL http://localhost:7071/api/ for requests, while the remote ones use https://<myfunctionapp>.azurewebsites.net/api/ for requests.



For example, if I try to Get Whishes Remote, without authentication, I will now recieve a 401 Unauthorized, and the message that I do not have permission:


[![](/uploads/2021/12/image-21.png?w=708)](/uploads/2021/12/image-21.png)



In Postman and on the Collection settings, you can add Authorization. Here I have added OAuth 2.0, and specified a Token Name and using Authorization Code grant flow. I will use the browser to authenticate, and note that the callback url should be the same as you added to the Frontend App registration earlier:


[![](/uploads/2021/12/image-22.png?w=678)](/uploads/2021/12/image-22.png)



Next, specify the /common endpoints for Auth URL and Token URL (https://login.microsoftonline.com/common/oauth2/v2.0/authorize and https://login.microsoftonline.com/common/oauth2/v2.0/token), the Client ID should be the App ID of the Frontend App registration, and the Secret should be the secret you created earlier. I have used environment variables in my setup below.



Important! You need to specify the scopes for which API you will get an access token for. In this case I use the api://festivetechcalendarapi/access\_as\_user and api://festivetechcalendarapi/Whish.ReadWrite:


[![](/uploads/2021/12/image-24.png?w=658)](/uploads/2021/12/image-24.png)



With all that set up, you can now click to **Get New Access Token.** It will launch a browser session (if you are running multiple profiles, make sure it opens in your correct one), and you can authenticate. Upon successful authentication, an access token will be returned to Postman and you can again test a remote request, which this time should be successful:


[![](/uploads/2021/12/image-26.png?w=672)](/uploads/2021/12/image-26.png)



### Adding Authorization Logic to Azure Functions



So now we know that the Function App and API is protected using Azure AD.



The next step would be to implement authorization logic inside the functions. This is when a request has been triggered with an Authorization Header, which contains the Access Token for the API, and where we can get the details from the token and make authorization logic based on that.



For this scenario I'm going to use a community PowerShell module called JWTdetails, made by [Darren Robinson](https://blog.darrenjrobinson.com/jwtdetails-powershell-module-for-decoding-jwt-access-tokens-with-readable-token-expiry-time/).



First add a dependency on that module in requirements.psd1 inside the api folder:



```powershell
@{
    # For latest supported version, go to 'https://www.powershellgallery.com/packages/Az'.
    # To use the Az module in your function app, please uncomment the line below.
    'Az' = '7.*'
    'JWTDetails' = '1.*'
}
```



Then in run.ps1 for each of the functions (Create, Update, Get and Delete Whish) add the following in the beginning, just after param statement and write-host for "PowerShell HTTP trigger...":



```powershell
$AuthHeader = $Request.Headers.'Authorization'
If ($AuthHeader) {
    $AuthHeader
    $parts = $AuthHeader.Split(" ")
    $accessToken = $parts[1]
    $jwt = $accessToken | Get-JWTDetails

    Write-Host "This is an authorized request by $($jwt.name) [$($jwt.preferred_username)]"

    # Check Tenant Id to be another Azure AD Organization or Personal Microsoft
    If ($jwt.tid -eq "9188040d-6c67-4c5b-b112-36a304b66dad") {
        Write-Host "This is a Personal Microsoft Account"
    } else {
        Write-Host "This is a Work or School Account from Tenant ID : $($jwt.tid)"
    } 
}
```



The code you see above, retrieves the Authorization Header if it is present, and then splits the access token from the string "BEARER <jwt token>". That JWT token can then be checked for details by the Get-JWTDetails command. I'm retreiving a couple of claims to get the user name and the user principal name, and also checks which organization or personal (fixed tenant id for MS accounts) the user is coming from.



In addition, for the GetWhishes function, I also add the authorization logic that the functions checks the scopes, and if the user does not have Whish.ReadWrite.All, then the user should only be allowed to see own whishes at not everybody elses.



This code should be placed right after getting the Cosmos DB items in the run.ps1 for GetWhishes function:



```powershell
If ($AuthHeader) {
    Write-Host "The Requesting User has the Scopes: $($jwt.scp)"
    # Check for Scopes and Authorize
    If ($jwt.scp -notcontains "Whish.ReadWrite.All") {
        Write-Host "User is only authorized to see own whishes!"
        # $Whishes = $Whishes | Where-Object {$_.uid -eq $jwt.oid}
        # $Whishes = $Whishes | Where-Object {$_.upn -eq $jwt.preferred_username }
        $Whishes = $Whishes | Where-Object {$_.name -eq $jwt.name}
    }
} else {
    Write-Host "No Auth, return nothing!"
    $Whishes = $Whishes | Where-Object {$_.id -eq $null}
}
```



You will see that I can select a few alternatives for filtering (I have commented out the ones not in use). I can use a soft filter based on name, or if I want to I can filter based on user/object id, or user principal name. The last two options require that I add a couple of lines to the CreateWhish function as well:



```powershell
$whish = [PSCustomObject]@{
    id = $guid.Guid
    name = $Request.Body.name
    whish = $Request.Body.whish
    pronoun = [PSCustomObject]@{ 
        name = $Request.Body.pronoun.name 
    }
    created = $datetime.ToString()
    uid = $jwt.oid
    upn = $jwt.preferred_username
}
```



As you see from the last two lines above, I have added that the creation of a new item is also stored with the object id and the upn of the user that has authenticated to the API (using the JWT token).



With these changes, you should once again Deploy the local Functions to the Function App.



If I now do another remote test in Postman client, and follow the Azure Function App monitor in the Azure Portal, I can indeed see that my user has triggered the API securly, and is only authorized to see own whishes:


[![](/uploads/2021/12/image-27.png?w=1024)](/uploads/2021/12/image-27.png)



The last remaining step now is to change the web frontend to be able to use the API via Azure AD Authentication.



## Authenticate to API from a Single Page Application (SPA)



We are now going to configure the web frontend application, which is based on JavaScript SPA, to be able to sign in and authorize, get ID and Access Token and send secured requests to our Christmas Whishes API, this will use the Oauth2 authorization code flow as shown below:


[![](/uploads/2021/12/image-28.png?w=1024)](/uploads/2021/12/image-28.png)



### Configure Msal.js v2



We are going to use the Microsoft Authentication Library (MSAL) for Javascript, Msal.js v2, for the authentication and authorization flows in the web app.



First, in the frontend folder, create a file named **authConfig.js**, and add the following code:



```javascript
const msalConfig = {
    auth: {
      clientId: "<your-app-id>",
      authority: "https://login.microsoftonline.com/common",
      redirectUri: "http://localhost:3000",
    },
    cache: {
      cacheLocation: "sessionStorage", // This configures where your cache will be stored
      storeAuthStateInCookie: false, // Set this to "true" if you are having issues on IE11 or Edge
    }
  };

  // Add here scopes for id token to be used at MS Identity Platform endpoints.
  const loginRequest = {
    scopes: ["openid", "profile"]
  };
```



Change the above code to your app id from the frontend app registration, and if you have other names for the api scopes change that as well for the tokenRequest constant.



*PS! If you created a single-tenant application earlier, and not multi-tenant and personal microsoft accounts as I did, replace authority above with https://login.microsoftonline.com/<your-tenant-id>.*



Create another file in the frontend folder named **apiConfig.js**. Add the following code:



```javascript
const apiConfig = {
    whishesEndpoint: "https://<yourfunctionapp>.azurewebsites.net/api/whish/"
  };
```



Change the above endpoint to your function app name.



Next, create another file in the frontend folder named **authUI.js**, and add the following code:



```javascript
// Select DOM elements to work with
const welcomeDiv = document.getElementById("welcomeMessage");
const signInButton = document.getElementById("signIn");

function showWelcomeMessage(account) {
  // Reconfiguring DOM elements
  welcomeDiv.innerHTML = `Welcome ${account.username}`;
  signInButton.setAttribute("onclick", "signOut();");
  signInButton.setAttribute('class', "btn btn-success")
  signInButton.innerHTML = "Sign Out";
}

function updateUI(data, endpoint) {
  console.log('Whishes API responded at: ' + new Date().toString());

}
```



The above code is used for hiding/showing document elements based on if the user is signed in or not.



Next, we need to have a script with functions that handles the sign-in and sign-out, and getting the access token for the API. Add a new file to the frontend folder called **authPopup.js**, and add the following script contents to that file:



```javascript
// Create the main myMSALObj instance
// configuration parameters are located at authConfig.js
const myMSALObj = new msal.PublicClientApplication(msalConfig);

let username = "";

function loadPage() {
    /**
     * See here for more info on account retrieval:
     * https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-common/docs/Accounts.md
     */
    const currentAccounts = myMSALObj.getAllAccounts();
    if (currentAccounts === null) {
        return;
    } else if (currentAccounts.length > 1) {
        // Add choose account code here
        console.warn("Multiple accounts detected.");
    } else if (currentAccounts.length === 1) {
        username = currentAccounts[0].username;
        showWelcomeMessage(currentAccounts[0]);
    }
}

function handleResponse(resp) {
    if (resp !== null) {
        username = resp.account.username;
        console.log('id_token acquired at: ' + new Date().toString());        
        showWelcomeMessage(resp.account);
    } else {
        loadPage();
    }
}

function signIn() {
    myMSALObj.loginPopup(loginRequest).then(handleResponse).catch(error => {
        console.error(error);
    });
}

function signOut() {
    const logoutRequest = {
        account: myMSALObj.getAccountByUsername(username)
    };

    myMSALObj.logout(logoutRequest);
}

loadPage();
```



We can now start to make some changes to the **index.html** file, so that it supports the Msal v2 library, shows a sign in button and a welcome message, and adds the app scripts from above.



First add the following html code to the HEAD section of the index.html file in frontend folder:



```html
    <!-- IE support: add promises polyfill before msal.js  -->
    //cdn.jsdelivr.net/npm/bluebird@3.7.2/js/browser/bluebird.min.js
    https://alcdn.msauth.net/browser/2.0.0-beta.4/js/msal-browser.js
```



Then, add the following sign in button and welcome message text to index.html, so that the header section looks something like this:



```html
      <header>
        <div class="container">
          <div class="hero is-info is-bold">
            <div class="hero-body">
                <img src="festivetechcalendar.jpg" width="500px">
              <h1 class="is-size-1">Christmas Whishes</h1>
            </div>
            <div>
              <button type="button" id="signIn" class="btn btn-success" onclick="signIn()">Sign In</button>
            </div>            
          </div>
          <div>
            <h5 class="is-size-4" id="welcomeMessage">Please Sign In to create or see whishes.</h5>
          </div>
        </div>
      </header>
```



Then, at the end of the index.html file, add the following app scripts:



```html
    <!-- importing app scripts (load order is important) -->
    http://./authConfig.js
    http://./apiConfig.js
    http://./authUi.js
    http://./authPopup.js
  </body>
</html>
```



Then, back to the Visual Studio Code and Terminal Window, stop the node web application if it's still running, and type the following command in the frontend folder:



`npm install @azure/msal-browser`



This will install and download the latest package references of Msal. After this has been run successfull you will see references updated in the package.json and package-lock.json files.



Save the index.html file with the above changes. We can now test the updated web page via http://localhost:3000. Type npm start in the terminal window to start the web application again. Now you can click the Sign in button, and you can sign in with your account:


[![](/uploads/2021/12/image-29.png?w=1024)](/uploads/2021/12/image-29.png)



PS! Note that the above application supports multi-tenant and personal microsoft accounts, so you can sign in with either.



First time signing in you should get a consent prompt:


[![](/uploads/2022/01/image.png?w=440)](/uploads/2022/01/image.png)



These are the permission scopes "openid" and "profile" defined in the login request above.



After signing in the welcome message should get updated accordingly:


[![](/uploads/2021/12/image-30.png?w=806)](/uploads/2021/12/image-30.png)



We have now been able to sign in with the Identity Platform, and this will get an ID token for the signed in user. We are halfway there, because we will need an access token to be able to call the resource api.



### Getting an Access Token for the API using Msal.js v2
