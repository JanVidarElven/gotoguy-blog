---
title: "Connect Power Platform to Azure AD Protected APIs using built-in HTTP connectors"
date: 2022-12-12T12:02:35Z
draft: false
slug: "connect-power-platform-to-azure-ad-protected-apis-using-built-in-http-connectors"
tags:
  - "Power Platform"
categories:
  - "Azure AD"
  - "Microsoft Graph"
  - "Power Automate"
  - "PowerApps"
---

There are several ways you can access the Azure AD Protected APIs in Power Platform Flows and Apps. Without creating Custom Connectors, which basically can connect to any REST based API that is available, it is useful to know what built-in HTTP connectors are available and can be used for delegated authentication to Azure AD Protected APIs like Microsoft Graph or other APIs.



This and more will be answered and demoed in this blog post.



## What is an Azure AD Protected API?



First, lets do a quick explanation of what an Azure AD Protected API is.



The most known Microsoft API is the [Microsoft Graph API](https://aka.ms/graph). Another well known API is the [Azure REST API](https://learn.microsoft.com/en-us/rest/api/azure/). These APIs are protected by and accessed by identities and applications from Azure Active Directory organizations.



Other than that, any API has the possibility to be protected by Azure AD and by using industry standard authentication and authorization protocols like OpenID Connect (OIDC) and OAuth2.0. This includes APIs you might build yourself or APIs from third party services.



## Delegated vs. Application Access



When you want to access Azure AD Protected APIs from Power Platform you also need to know the access scenarios you will need. There are 2 main access scenarios: Delegated access and Application-only access, and as shown in the picture below, there is a distinct difference in that the delegated access scenario always includes the user.


[![](/uploads/2022/12/image.png?w=1024)](/uploads/2022/12/image.png)



This means that if you are running a Power Automate flow, or a PowerApp, you will usually run that interactively as your user account, and any connections you use will be running via the app under your user context and permissions to access the data resources the app might be using. The data resource in this example can be represented by an Azure AD Protected API.



If you share the PowerApp or Power Automate flow with other users in your organization, then those users will use the connections to the API resource under their own user context.



If you, on the other hand, wants to run a Power Automate flow on a schedule or in any other way without user interaction or without a user context, then you typically will use the app-only access scenario.



In this blog post I will focus on delegated access scenarios, and where you can use built-in HTTP connectors that will run in connection based on the running user.



## Built-in HTTP Connectors in Power Platform



Let's start with an overview over what built-in HTTP connectors and actions for Azure AD Protected APIs we have available in Power Platform. These are HTTP connector actions you can use in Power Automate, PowerApps and in most cases also Logic Apps, and the following list is current as of December 2022:



- "Send an HTTP request (preview)", **Office 365 Outlook** connector.
- "Send an HTTP request (preview)", **Office 365 Users** connector.
- "Send an HTTP request", **Office 365 Groups** connector.
- "Send an HTTP request V2 (preview)", **Office 365 Groups** connector.
- "Send an HTTP request (preview)", **Office 365 Groups Mail** connector.
- "Send an HTTP request to SharePoint", **SharePoint** connector.
- "Send an HTTP request (preview)", **LMS365** connector.



These are all **Standard** connectors that you can freely use if you are using the Power Apps/Automate plan for Microsoft 365.



There is also an interesting HTTP action with Azure AD that is **Premium** and has the following action:



- "Invoke an HTTP request", **HTTP with Azure AD** connector.



**Premium** means you need to acquire a standalone Power Apps and Power Automate licensing plan.



There is also a "Send an HTTP request to Azure DevOps" in the Azure DevOps connector that is also **Premium**.



While these connectors are for querying resources that are under the scope of the data that are accessible via the connector, the most important part is that these are all dependent on the user **connection** and is using the **delegated access** scenario.



This makes them especially useful for calling Microsoft Graph API in the context of your own user.



If you want to send HTTP requests in an app-only access scenario, then you can use the built in **HTTP connector**, which is **Premium**. But that is not the scope of this blog post, so let's continue looking into some scenarios and examples for the above delegated access connectors.



## Send HTTP Request via Office 365 connectors



Lets do a couple of scenarios of the Office 365 Outlook/Users/Groups connectors from above, and their HTTP request actions. I have created a instant cloud flow with a manual trigger for now.



First I will initialize a variable for the base Url, this will be the Microsoft Graph API:


[![](/uploads/2022/12/image-1.png?w=569)](/uploads/2022/12/image-1.png)



Then I add each of the HTTP actions from the Office 365 connectors, using the baseUrl and the "me" resource to start with. In the below image I've renamed the HTTP actions so that you can see from which connector they are from, and I'm running a simple GET method:


[![](/uploads/2022/12/image-2.png?w=506)](/uploads/2022/12/image-2.png)



I've also configured the run after setting for each of the actions, so that I can verify the results of the others if anyone fails:


[![](/uploads/2022/12/image-3.png?w=551)](/uploads/2022/12/image-3.png)



When I save and test the flow I can verify that I've signed in to the connectors as my own user, and any permissions that these have:


[![](/uploads/2022/12/image-4.png?w=289)](/uploads/2022/12/image-4.png)



When I try to run this Flow, it will fail on several of the actions, this is expected:


[![](/uploads/2022/12/image-5.png?w=1024)](/uploads/2022/12/image-5.png)



The reason it fails is because there are restrictions on the resources and objects the actions are allowed to query, for example for the first one we get the info on that this connector can use either "me" resource or "users" resource, but also only for the listed objects like messages, calendar etc:


[![](/uploads/2022/12/image-6.png?w=520)](/uploads/2022/12/image-6.png)



One of the actions is successful however, and that is from the Office 365 Groups connector and the first version of the Send an HTTP request, which is allowed to get the /me resource:


[![](/uploads/2022/12/image-7.png?w=560)](/uploads/2022/12/image-7.png)



Lets make some adjustments to the queries for the different actions:


[![](/uploads/2022/12/image-8.png?w=513)](/uploads/2022/12/image-8.png)



In the above image I've added some supported objects for the different actions, and all these should return a valid Graph response:


[![](/uploads/2022/12/image-9.png?w=563)](/uploads/2022/12/image-9.png)



So this means as long as you either:



- use the /me/{object} or
- /users/{userid-or-userprincipalname}/{object} or
- /groups or /groups/{groupid}/{object}



From the supported list of objects (messages, events, calendar, etc) then you can run any Microsoft Graph API queries including GET, POST, PUT, PATCH and DELETE.



From earlier we saw that one of the connector actions had more broad support than the others, and that was the Office 365 Groups connector and the original version of the "Send an HTTP request". There has since been released a V2 version of the same action, and that limits only queries against /groups resource.



Lets do a quick test on if the first action supports getting the user's registered authentication methods. If we run that same query using [Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer?request=me%2Fauthentication%2Fmethods&method=GET&version=v1.0&GraphUrl=https://graph.microsoft.com&headers=W3sibmFtZSI6IkNvbnNpc3RlbmN5TGV2ZWwiLCJ2YWx1ZSI6ImV2ZW50dWFsIn1d), we will get a list of your users methods for authentication, including Authenticator, Phone, Windows Hello etc. In the action I will type /me/authentication/methods, but when I run it will fail with request authorization failed:


[![](/uploads/2022/12/image-11.png?w=562)](/uploads/2022/12/image-11.png)



This means that even though I have permission as my self to query my authentication methods (see Graph Explorer for example), the connector does not have the correct delegated permissions to act on my behalf. From Graph Explorer I can verify that I need to consent to permissions for authentication methods:


[![](/uploads/2022/12/image-12.png?w=1024)](/uploads/2022/12/image-12.png)



So to summarize the Office 365 connectors and HTTP actions, they can be valuable for many Graph API requests for your users, but only for permitted objects and permissions.



This is where the "Invoke an HTTP request", **HTTP with Azure AD** connector, can be useful, and we will look into that next.



## Send Request via HTTP with Azure AD Connector



First of all, this is a Premium connector, so you must make sure you are licensed with a separate Power Apps / Power Automate plan for this, but a trial should also be available to for exploring the connector.



According to the documentation, the [HTTP with Azure AD connector](https://learn.microsoft.com/en-us/connectors/webcontents/) can be used to fetch resources from various web services that are authenticated by Azure AD. It can also be used to query from an on-premise web service.



Note that there are known issues and limitations, such as if you get *"Forbidden"* or *"Authorization Request Denied*", or *"Insufficient privileges to complete the operation."* then it could be because this connector has a limited set of scopes.



The big advantage of this connector is that you can use it for several of Microsoft APIs, not just the Graph API.



Lets try it out, I will create another instant cloud flow with manual trigger, and then add the HTTP with Azure AD connector and Invoke an HTTP request action:


[![](/uploads/2022/12/image-13.png?w=553)](/uploads/2022/12/image-13.png)



If this is the first time you have added that connector action and you don't have any existing connections, then you need to configure that and sign in first. If we want to use the Microsoft Graph API, then you need to fill in this and then sign in:


[![](/uploads/2022/12/image-15.png?w=535)](/uploads/2022/12/image-15.png)



Then, we can start with a simple Graph request for getting my profile info:


[![](/uploads/2022/12/image-14.png?w=577)](/uploads/2022/12/image-14.png)



When we run that, it should successfully return the user profile:


[![](/uploads/2022/12/image-16.png?w=1024)](/uploads/2022/12/image-16.png)



Ok, let's try another request again, and see if this connector lets us query for authentication methods:


[![](/uploads/2022/12/image-17.png?w=1024)](/uploads/2022/12/image-17.png)



So here we can see that the limitations in scope also applies to this connector, as we get an access denied and request authorization failed.



But there are more scenarios that this connector action support than the Office 365 connectors I described in the previous section. For example I can get my groups memberships, note the use of $count parameter and that it requires the consistencyLevel=eventual in the Request Header:


[![](/uploads/2022/12/image-18.png?w=1024)](/uploads/2022/12/image-18.png)



There aren't really any good documentation on the HTTP for Azure AD connector to say which resources and objects you can send requests to, but you can assume that you can do a lot of the normal member of a directory can do, but not necessarily those that require Graph permission consent outside read user information.



Note that you can use the HTTP for Azure AD connector to other APIs than Microsoft Graph, and this is just a list of examples:



- management.azure.com
- vault.azure.net
- <tenant>.sharepoint.com
- api.loganalytics.io



But I thought I should wrap up the blog post by looking at how the HTTP for Azure AD connector can be used for invoking requests for APIs that you have built yourself, like for Azure Functions or Logic Apps.



## Invoke Requests for your Serverless APIs with HTTP for Azure AD



### Protected Logic Apps



I have previously written a blog post series on how you can protect Logic Apps with Azure AD: <https://gotoguy.blog/2020/12/31/protect-logic-apps-with-azure-ad-oauth-part-1-management-access/>



Lets use that knowledge to see if the HTTP for Azure AD connector can invoke requests to a Logic App that is protected with an Azure AD Authorization Policy.



I have created a new simple Logic App with a HTTP request trigger:


[![](/uploads/2022/12/image-19.png?w=1024)](/uploads/2022/12/image-19.png)



I've added a response action, and made sure that the response is returning JSON content like this:


[![](/uploads/2022/12/image-20.png?w=1024)](/uploads/2022/12/image-20.png)



Then, I have added an Azure AD Authorization Policy like the following, requiring that the issuer claim in the authorization header is from my tenant:


[![](/uploads/2022/12/image-21.png?w=1024)](/uploads/2022/12/image-21.png)



I can now go to my Power Automate flow, and add an HTTP for Azure AD connector action, but I need to set up a new connection like the following. Note that the base resource URL will be the Logic App instance, and the Azure AD Resouce URI will be one of the well known Azure APIs like below. (I haven't been able to use graph.microsoft.com here, because I suspect the fact that Graph API tokens cannot be validated outside Microsoft Graph itself).


[![](/uploads/2022/12/image-22.png?w=1024)](/uploads/2022/12/image-22.png)



When I have signed in at set that connection active I can configure the Invoke an HTTP request action like the following, note that I have left out the parameters that belong to the SAS (shared access scheme) like sig, sv, sp, as you only can use on of SAS or OAuth2:


[![](/uploads/2022/12/image-23.png?w=1024)](/uploads/2022/12/image-23.png)



When I run this I get a successful response:


[![](/uploads/2022/12/image-24.png?w=1024)](/uploads/2022/12/image-24.png)



This means that the HTTP for Azure AD connector was now able to invoke a request for a protected API that I have built myself. Of course this was a simple request, but if you look at the aforementioned blog post series of protecting Logic Apps, you can see how you can include the Authorization Header in the Logic App trigger, and then get the claims and do authorization logic inside the Logic App.



In this example I didn't include my own API definition, so lets now get even more advanced and look at an Azure Functions API example!



### Protected Azure Functions with Custom API



Last year for Festive Tech Calendar in 2021, I created this solution for my contribution: <https://gotoguy.blog/2021/12/22/creating-an-azure-ad-protected-api-in-azure-in-a-school-hour/>



I will now use this as an example on how I can invoke requests for this API using Power Automate and the HTTP for Azure AD connector!



In another instant cloud flow, I've added the Invoke request with HTTP for Azure AD, and I need to create another connection, which will be configured as follow:


[![](/uploads/2022/12/image-25.png?w=1024)](/uploads/2022/12/image-25.png)



The base URL is the Function App URL, and for Resource URI I've used the Application ID URI I created when I defined the custom API (see the blog post for details).



However, when I sign in I will first get an error like the following:


[![](/uploads/2022/12/image-26.png?w=1024)](/uploads/2022/12/image-26.png)



Note the client app id I've marked with a yellow shape above, this is a well known global confidential application ID for Power Platform, so this will be the same ID for you as it is for me. This is also described in this article: <https://learn.microsoft.com/en-us/power-query/connectorauthentication>.



This means that I need to go to my custom API app registration, and add this ID as an authorized client application and which scopes it is authorized to use:


[![](/uploads/2022/12/image-27.png?w=1024)](/uploads/2022/12/image-27.png)



After adding that I can now sign in to create the connection, and next configure the invoke HTTP request as follows, using one of the API methods I've defined (again see my blog post from last year for details :):


[![](/uploads/2022/12/image-29.png?w=1024)](/uploads/2022/12/image-29.png)



When I run the Flow I see that the request is successful, and I indeed get a response from the Protected Functions API:


[![](/uploads/2022/12/image-28.png?w=1024)](/uploads/2022/12/image-28.png)



## Summary



In this blog post I have shown how you can use and connect Power Platform to Azure AD Protected APIs using built-in HTTP connectors that use the delegated access scenario.



While the Office 365 connectors are great for limited scenarios around Microsoft Graph, we could verify that the HTTP for Azure AD connector (Premium) had more usage scenarios, including the ability to invoke requests from both Microsoft APIs, as well as your own APIs.



Hope this has been useful, thanks for reading!
