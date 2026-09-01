---
title: "Protect Logic Apps with Azure AD OAuth - Part 1 Management Access"
date: 2020-12-31T10:55:23Z
draft: false
slug: "protect-logic-apps-with-azure-ad-oauth-part-1-management-access"
tags:
  - "OAuth2"
  - "OpenID Connect"
categories:
  - "Azure AD"
  - "Logic Apps"
---

Azure Logic Apps are great for creating workflows for your IT automation scenarios. Logic App workflows can be triggered using a variety of sources and events, including schedules, but a popular trigger is using a HTTP trigger for starting the Logic App workflow interactively or on-demand from outside the Logic App.



To trigger a Logic App using a HTTP trigger, you need to know the endpoint URL, for example:


[![](/uploads/2020/12/image-229.png?w=932)](/uploads/2020/12/image-229.png)



This URL consist of the endpoint address of the Logic App and workflow trigger, and with the following query parameters:



- api-version
- sp (specifies permissions for permitted HTTP methods to use)
- sv (SAS version to use)
- sig (shared access signature)


[![](/uploads/2020/12/image-230.png?w=1024)](/uploads/2020/12/image-230.png)



Anyone with access to this URL and query parameters kan trigger the Logic App, so it's very important to protect it from unauthorized access and use.



In this multi part blog post series we will look into how Logic Apps can be protected by Azure AD.



Scenarios this multi-part blog post articles will cover:



- Provide Management Access Tokens and Restrict Issuer and Audience via OAuth
- Restrict External Guest User Access
- Expose Logic App as API
- Restrict permitted Enterprise Application Users and Groups and Conditional Access policies.
- Scopes and Roles Authorization in Logic Apps.
- Logic Apps and APIM (Azure API Management).



Lets first look at the other methods for protecting Logic Apps you should be aware of.



## Protect Logic Apps Keys and URLs



Before we move on to protecting Logic Apps with Azure AD Open Authentication (OAuth), lets take a quick summary of other protections you should be aware of:



- Regenerate access keys. If you have reason to think SAS keys are shared outside your control, you can regenerate and thus making previous SAS keys invalid.
- Create expiring Callback URLs. If you need to share URLs with people outside your organization or team, you can limit exposure by creating a Callback URL that expire on a certain date and time.
- Create Callback URL with primary or secondary key. You can select to create the Callback URL with the specified primary or secondary SAS key.



The above methods should be part of any governance and security strategy for protecting Logic Apps that perform privilieged actions or might return sensitive data.



## Protect Logic Apps via restricting inbound IP address



Another way to protect Logic Apps is to restrict from where the Logic App can be triggered via inbound IP address restrictions.



This opens up scenarios where you can specify your datacenter IP ranges, or only let other Logic Apps outbound IP addresses call nested Logic Apps, or only allow Azure API management to call Logic App.



## Protect Logic Apps with Azure AD OAuth



By creating an Authtorization Policy for your Logic App you can use a Authorization header with a Bearer Token and require that the token contains the specified issuer, audience or other claims. Showing how that works in detail, and usable scenarios will be the main focus for this blog post.



Let's start by building a basic Logic App we can use for demo purpose.



### Creating a basic Logic App with HTTP Trigger and Response



In you Azure Subcription, create a new Logic App, specifying to use a HTTP trigger. In my example below I have named my Logic App "logicapp-test-auth":


[![](/uploads/2020/12/image-231.png?w=754)](/uploads/2020/12/image-231.png)



Next, add a Parse JSON action, where the Content is set to the trigger headers, as shown below. I've just specified a simple schema output, this can be customized later if needed:


[![](/uploads/2020/12/image-232.png?w=761)](/uploads/2020/12/image-232.png)



After that activity, add a Response action to return data to the caller. In my example below I return a Status Code of 200 (OK), and set the Content-Type to application/json, and return a simple JSON body of UserAgent where the value is set to the parsed header output from the trigger, using dynamic expression:   
`body('Parse_JSON_Headers')?['User-Agent']`


[![](/uploads/2020/12/image-233.png?w=611)](/uploads/2020/12/image-233.png)



### Testing Logic App with Postman



A great way to test and explore HTTP and REST API calls from your client is to use Postman ([Download Postman | Try Postman for Free](https://www.postman.com/downloads/)). When testing the above Logic App, paste in the HTTP POST URL for your trigger, and set the method to POST as shown below:


[![](/uploads/2020/12/image-234.png?w=915)](/uploads/2020/12/image-234.png)



From the above image, you can see the URL, and also the query parameters listed (api-version, sp, sv, and sig, remember that these should be shared publicly).



When I send the request, it will trigger the Logic App, and should response back:


[![](/uploads/2020/12/image-235.png?w=429)](/uploads/2020/12/image-235.png)



We can also verify the run history for the Logic App:


[![](/uploads/2020/12/image-236.png?w=631)](/uploads/2020/12/image-236.png)



We have now successfully tested the Logic App using SAS authentication scheme, and can proceed to adding Azure AD OAuth. First we need to create an Authorization Policy.



### Creating an Azure AD Authorization Policy



Under Settings and Authorization for your Logic App, add a new Authorization Policy with your name, and add the Issuer claim for your tenant. Issuer will be either https://sts.windows.net/{your-tenant-id}/ or https://login.microsoftonline.com/{your-tenant-id}/ depending on the version of the Access Token:


[![](/uploads/2020/12/image-237.png?w=939)](/uploads/2020/12/image-237.png)



We will add more Claims later, but for now we will just test against the Issuer. Before we can test however, we need to get an Access Token. There are several ways to easily get an access token, basically we can consider one of the following two scenarios:



1. Aquire an Access Token for well known Azure Management Resource Endpoints.
2. Create an App Registration in Azure AD exposing an API.



We'll cover App Registration and more advanced scenarios later, but for now we will get an Access Token using well known resource endpoints for Azure management.



*PS! Just a quick note on Access Tokens aquired for Microsoft Graph resources: These cannot be used for Logic Apps Azure AD OAuth authorization policies, because Graph access tokens does not allow for signature validation.*



### Management Access Tokens



The following examples require that you either have installed Azure CLI ([Install the Azure CLI | Microsoft Docs](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?WT.mc_id=AZ-MVP-5001872)) or Az PowerShell ([Install Azure PowerShell with PowerShellGet | Microsoft Docs](https://docs.microsoft.com/en-us/powershell/azure/install-az-ps?WT.mc_id=AZ-MVP-5001872)).



#### Azure CLI



If you haven't already, you will first need to login to Azure using az login. You can login interactively using default browser which supports modern authentication, including MFA, but if you are running multiple browsers and profiles it might be easier to use the device code flow:



```bash
az login --use-device-code
```



You will be prompted to open the microsoft.com/devicelogin page and enter the supplied device code, and after authentication with your Azure AD account, you will get a list of all subscriptions you have access to.


[![](/uploads/2020/12/image-238.png?w=1024)](/uploads/2020/12/image-238.png)



PS! If your account has access to subscriptions in multiple tenants, you can also specify which tenant to log into using:



```bash
az login --tenant elven.onmicrosoft.com --use-device-code
```



To get an Access Token you can just run `az account get-access-token`, like the following:


[![](/uploads/2020/12/image-239.png?w=1024)](/uploads/2020/12/image-239.png)



Let's save that into a variable and get the token:



```powershell
$accessToken = az account get-access-token | ConvertFrom-Json  
$accessToken.accessToken | Clip
```



The above command copies the Access Token to the Clipboard. Let's take a look at the token. Open the website [jwt.ms](https://jwt.ms) or [jwt.io](https://jwt.io), and paste in the token. From the debugger you can look at the decoded token payload. The most interesting part for now is the issuer (iss) and audience (aud), which tells us where the token has been issued from, and to which audience:


[![](/uploads/2020/12/image-240.png?w=1024)](/uploads/2020/12/image-240.png)



As we can see from above, the audience for the token is "management.core.windows.net". You can also get an access token for a specific resource endpoint using:



```powershell
$accessToken = az account get-access-token --resource-type arm | ConvertFrom-Json
```



To show all available resource endpoints use:



```bash
az cloud show --query endpoints
```



Now that we have the method to get the access token using Az Cli, lets take a look at Az PowerShell as well. For reference for az account command and parameters, see docs here: [az account | Microsoft Docs](https://docs.microsoft.com/en-us/cli/azure/account?view=azure-cli-latest#az_account_get_access_token)



#### Azure PowerShell



First you need to login to your Azure Subscription by using:



```powershell
Connect-AzAccount
```


[![](/uploads/2020/12/image-241.png?w=1024)](/uploads/2020/12/image-241.png)



If your account has access to multiple subscriptions in multiple tenant, you can use the following command to specify tenant:



```powershell
Connect-AzAccount -Tenant elven.onmicrosoft.com
```



If there are multiple subscriptions, you might need to specify which subscription to access using `Set-AzContext -Subscription <Subscription>`. Tip, use `Get-AzContext -ListAvailable` for listing available subscriptions.



To get an access token using Az PowerShell, use the following command to save to variable and copy to clipboard:



```powershell
$accessToken = Get-AzAccessToken
$accessToken.Token | Clip
```



We can once again look at the JWT debugger to verify the token:


[![](/uploads/2020/12/image-242.png?w=1024)](/uploads/2020/12/image-242.png)



As with Az CLI, you can also specify resource endpoint by using the following command in Az PowerShell specifying the resource Url:



```powershell
$accessToken = Get-AzAccessToken -ResourceUrl 'https://management.core.windows.net'
```



Now that we have the Access Token for an Azure Management resource endpoint, let's see how we can use that against the Logic App.



#### Use Bearer Token in Postman



From the previous test using Postman earlier in this article, go to the Authorization section, and specify Bearer Token, and then Paste the management access token you should still have in your clipboard like the following:


[![](/uploads/2020/12/image-243.png?w=1024)](/uploads/2020/12/image-243.png)



When clicking Send request, observe the following error:


[![](/uploads/2020/12/image-244.png?w=1024)](/uploads/2020/12/image-244.png)



We cannot combine both SAS (Shared Access Signature) and Bearer Token, so we need to adjust the POST URL to the Logic Apps. In Postman, this can be easily done in Postman under Params. Deselect the sp, sv and sig query parameters like the following, which will remove these from the POST URL:


[![](/uploads/2020/12/image-251.png?w=751)](/uploads/2020/12/image-251.png)



When you now click Send request, you should get a successful response again, provided that tha access token is valid:


[![](/uploads/2020/12/image-246.png?w=598)](/uploads/2020/12/image-246.png)



Perfect! We have now authorized triggering the Logic App using Azure AD OAuth, based on the Authorization policy:


[![](/uploads/2020/12/image-247.png?w=943)](/uploads/2020/12/image-247.png)



And the Access Token that match that Issuer:


[![](/uploads/2020/12/image-248.png?w=1024)](/uploads/2020/12/image-248.png)



I will now add the audience to the Authorization Policy as well, so that only Access Tokens for the management endpoint resource can be used:


[![](/uploads/2020/12/image-249.png?w=1008)](/uploads/2020/12/image-249.png)



Any HTTP requests to the Logic App that has a Bearer Token that does not comply with the above Authorization Policy, will received this 403 - Forbidden error:


[![](/uploads/2020/12/image-250.png?w=888)](/uploads/2020/12/image-250.png)



#### Test using Bearer Token in Azure CLI



You can trigger HTTP REST methods in Azure CLI using `az rest --method .. --url ..`.



When using az rest an authorization header with bearer token will be automatically added, trying to use the url as resource endpoint (if url is one of the well known resource endpoints). As we will be triggering the Logic App endpoint as url, we need to specify the resource endpoint as well. In my example, I will run the following command for my Logic App:



```bash
az rest --method POST --resource 'https://management.core.windows.net/' --url 'https://prod-72.we  
steurope.logic.azure.com:443/workflows/2fa8c6d0ed894b50b8aa5af7abc0f08b/triggers/manual/paths/invoke?api-  
version=2016-10-01'
```



From above, I specify the resource endpoint of management.core.windows.net, from which the access token will be aquired for, and for url I specify my Logic App endpoint url, without the sp, sv and sig query parameters. This results in the following response:


[![](/uploads/2020/12/image-252.png?w=955)](/uploads/2020/12/image-252.png)



So the Logic App triggered successfully, this time returning my console (Windows Terminal using Azure CLI).



#### Test using Bearer Token in Azure PowerShell



I will also show you how you can do a test using Az PowerShell. Make sure that you get an access token and saving the bearer token to a variable using this command first:



```powershell
$accessToken = Get-AzAccessToken
$bearerToken = $accessToken.Token
```



I will also set the Logic App url to a variable for easier access:



```powershell
$logicAppUrl = 'https://prod-72.westeurope.logic.azure.com:443/workflows/2fa8c6d0ed894b50b8aa5af7abc0f08b/triggers/manual/paths/invoke?api-version=2016-10-01'
```



There are 2 ways you can use Az PowerShell, either using Windows PowerShell or PowerShell Core.



For Windows PowerShell, use Invoke-RestMethod and add a Headers parameter specifying the Authorization header to use Bearer token:



```powershell
Invoke-RestMethod -Method Post -Uri $logicAppUrl -Headers @{"Authorization"="Bearer $bearerToken"}
```



Running this should return this successfully, specifying my Windows PowerShell version (5.1) as User Agent:


[![](/uploads/2020/12/image-253.png?w=961)](/uploads/2020/12/image-253.png)



For PowerShell Core, Invoke-RestMethod has now support for using OAuth as authentication, but I first need to convert the Bearer Token to a Secure String:



```powershell
$accessToken = Get-AzAccessToken
$bearerToken = ConvertTo-SecureString ($accessToken.Token) -AsPlainText -Force
```



Then I can call the Logic App url using:



```powershell
Invoke-RestMethod -Method Post -Uri $logicAppUrl -Authentication OAuth -Token $bearerToken
```



This should successfully return the following response, this time the User Agent is my PowerShell Core version (7.1):


[![](/uploads/2020/12/image-254.png?w=952)](/uploads/2020/12/image-254.png)



#### Summary so far of Management Access Tokens and Logic Apps



At this point we can summarize the following:



1. You can trigger your Logic App either by using SAS URL or using Bearer Token in Authorization Header, but not both at the same time.
2. You can add an Azure AD Authorization Policy to your Logic App that specifies the Issuer and Audience, so that calling clients only can use Bearer Tokens from the specified issuer (tenant id), and audience (resource endpoint).
3. While you cannot disable use of SAS signatures altogether, you can keep them secret, and periodically rollover, and only share the Logic App url endpoint and trigger path with clients.
4. This is especially great for automation scenarios where users can use CLI or Azure PowerShell and call your Logic Apps securely using OAuth and Access Tokens.



In the next part we will look more into how we can customize the Logic App to get the details of the Access Token so we can use that in the actions.



### Include Authorization Header in Logic Apps



You can include the Authorization header from the OAuth access token in the Logic App. To do this, open the Logic App in code view, and add the operationOptions to IncludeAuthorizatioNHeadersInOutputs for the trigger like this:



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



For subsequent runs of the Logic App, we can now see that the Authorization Header has been included:


[![](/uploads/2020/12/image-255.png?w=873)](/uploads/2020/12/image-255.png)



And if we parse the headers output, we can access the Bearer Token:


[![](/uploads/2020/12/image-256.png?w=637)](/uploads/2020/12/image-256.png)



If we want to decode that Bearer token to get a look into the payload claims, we can achieve that with some custom expression magic. Add a Compose action to the Logic App and use the following custom expression:


[![](/uploads/2020/12/image-265.png?w=639)](/uploads/2020/12/image-265.png)



Let's break it down:



- The Replace function replaces the string 'Bearer ' with blank (including the space after)
- The Split function splits the token into the header, payload data, and signature parts of the JWT. We are interested in the payload, so refers to that with index [1]



```text
split(replace(body('Parse_JSON_Headers')?['Authorization'], 'Bearer ',''), '.')[1]
```



Now it becomes a little tricky. We will have to use the base64ToString function to get the payload into readable string, but if the length of the payload isn't dividable by 4 we will get an error. Therefore we need to see if we need to add padding (=), as explained here: ([Base64 - Wikipedia](https://en.wikipedia.org/wiki/Base64#Output_padding)).



First I get the length of the payload data, and then use modulo function to see if there are any remaining data after dividing by 4:


[![](/uploads/2020/12/image-266.png?w=620)](/uploads/2020/12/image-266.png)



```text
mod(length(outputs('Get_JWT_Payload')),4)
```



Then I can do a conditional logic, where I use concat to add padding (=) to make it dividable by 4:


[![](/uploads/2020/12/image-267.png?w=1020)](/uploads/2020/12/image-267.png)



```text
if(equals(outputs('Length_and_Modulo'),1),concat(outputs('Get_JWT_Payload'),'==='),if(equals(outputs('Length_and_Modulo'),2),concat(outputs('Get_JWT_Payload'),'=='),if(equals(outputs('Length_and_Modulo'),3),concat(outputs('Get_JWT_Payload'),'='),outputs('Get_JWT_Payload'))))
```



After this I can use base64ToString to convert to a readable string object and format to JSON object:


[![](/uploads/2020/12/image-268.png?w=626)](/uploads/2020/12/image-268.png)



```text
json(base64ToString(outputs('Padded_JWT_Payload')))
```



Now that we have access to the claims, we can later be able to do some authorization in the Logic Apps, for example based on roles or scopes, but we can also get some information on which user that has called the Logic App.



In the Response action, add the following to return the Name claim:


[![](/uploads/2020/12/image-269.png?w=625)](/uploads/2020/12/image-269.png)



And if I test the Logic App http request again, I can see at it indeed returns my name based on the claims from the access token:


[![](/uploads/2020/12/image-259.png?w=943)](/uploads/2020/12/image-259.png)



We now have a way to identify users or principals calling the Logic App. The Authorization Policy for the Logic App now permits users and principals from my own organization (based on the issuer claim) and as long as the audience is for management.core.windows.net. But what if I want external access as well? Let's add to the authorization policies next.



### Add OAuth Authorization Policy for Guests



A logic app can have several Azure AD Authorization Policies, so if I want to let external guest users to be allowed to trigger the logic app, I will need to create another authorization policy that allows that issuer:


[![](/uploads/2020/12/image-260.png?w=668)](/uploads/2020/12/image-260.png)



Lets also add the upn claim to the response, so it is easier to see which user from which tenant that triggered the Logic App:


[![](/uploads/2020/12/image-262.png?w=617)](/uploads/2020/12/image-262.png)



When I now test with different users, internal to my tenant and external, I can see that it works and the response output is as expected:


[![](/uploads/2020/12/image-263.png?w=949)](/uploads/2020/12/image-263.png)


[![](/uploads/2020/12/image-264.png?w=900)](/uploads/2020/12/image-264.png)



## Summary of Management Access Scenarios



The purpose of the above steps has been to provide a way for management scenarios, where users and principals can get an Access Token using one of the Azure Management well known endpoints, and provide that when calling the Logic App. The access token is validated using OAuth Authorization Policies, requiring specific issuer (tenant id) and audience (management endpoint). This way we can make sure that we don't have to share the SAS details which lets users that have access to this URL call the Logic App without authentication.



In the next parts of this blog post articles, we will look into more advanced scenarios where we will expose the Logic App as an API and more.
