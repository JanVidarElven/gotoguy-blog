---
title: "Explore Microsoft Graph as a B2B Guest Account"
date: 2019-08-22T14:44:15Z
draft: false
slug: "explore-microsoft-graph-as-a-b2b-guest-account"
categories:
  - "Azure AD"
  - "Azure AD B2B"
  - "Microsoft Graph"
---

The Microsoft Graph Explorer (<https://aka.ms/ge>) is always a great learning source and useful tool for querying the Microsoft Graph, especially as you can use your own Azure AD work account or Microsoft account to query for real data. Another advantage with the Graph Explorer is that you can use it without requiring an App Registration in your tenant, something most users are not able to do themselves as they don’t have the administrator rights for registering apps.



However, sometimes working with Microsoft Graph, I find myself in a scenario where I want to use my own work account, but where the Microsoft Graph resources I want to query is in another Organization’s tenant. These kind of scenarios is usually where my account is invited as a B2B guest user to the resource tenant, and currently there are no way to use the Graph Explorer tool to do that.



So I need another tool, and as an IT pro I could easily write myself some PowerShell code, or as a developer I could create a Web app or Console app querying Graph, and run the queries against the other tenant from there.



On the other hand, I want to do this more inline with the Graph Explorer experience, so the most logical choice for me is to use a tool where I can just run the REST API queries I like. And the most popular tool, both by me and many others are the “Postman” client. You can get it yourself for free at [https://www.getpostman.com](https://www.getpostman.com "https://www.getpostman.com"), both Windows, Linux and Mac downloads are supported!



So in this blog post I will show how I use Postman to query Microsoft Graph in a B2B Guest User scenario.



## Requirements & Preparation



So, first you will need to get invited to another tenant where the resources you wan’t to query is. You might already have this Azure AD B2B invitation accepted previously. If you aren’t an administrator in that tenant, you will have to ask someone that has the rights to invite to do that for you.



Next, you will need to get assigned permissions to the resources you want to query in the resource tenant. This is all dependent on what kind of queries you want to run, whether it is for reading, writing or deleting resources for example.



Then, you will need an Global Administrator in that resource tenant to create an App Registration. The following instructions and screenshots can be used as a guide:



First, under the Azure AD experience in the Azure Portal, go to App Registrations and create a new Registration, type a name and a redirect URI like shown below:


[![image](/uploads/2019/08/image_thumb.png)](/uploads/2019/08/image.png)



You can type any name you like, for example in this scenario I want to use it for querying identities. I choose to support accounts in this organizational directory only, as this app registration is for members or guests from this tenant. And since I will be using the Postman i specify the redirect URI of “https://www.getpostman.com/oauth2/callback”. This is important as when I authenticate from Postman later the response will be returned to the Postman client.



When accessing Microsoft Graph you have to authenticate using one of the Oauth2 flows, and the most common is using authorization code flow, (<https://developer.microsoft.com/en-us/graph/blogs/30daysmsgraph-day-12-authentication-and-authorization-scenarios/>), which is exactly this scenario is all about as I will authenticate on behalf of my guest user account in the resource tenant. That means that I will have to add some delegated Graph permissions to the app registration, and in this example I add User.ReadBasic.All, this will make me able to query users via Graph:


[![image](/uploads/2019/08/image_thumb-1.png)](/uploads/2019/08/image-1.png)



After granting Admin consent for the permissions, I can verify that the permissions are added correctly:


[![image](/uploads/2019/08/image_thumb-2.png)](/uploads/2019/08/image-2.png)



Next I will need to create a client secret to be used in the request to get an access token, go to certificates & secrets and add a client secret of chosen time expiry:


[![image](/uploads/2019/08/image_thumb-3.png)](/uploads/2019/08/image-3.png)



Copy and make sure you save the client secret for later next:


[![image](/uploads/2019/08/image_thumb-4.png)](/uploads/2019/08/image-4.png)



Then copy the application id and tenant id and save for later:


[![image](/uploads/2019/08/image_thumb-5.png)](/uploads/2019/08/image-5.png)



Click on endpoints (see arrow above), and note the Oauth2 authorization and token endpoints (v2), this endpoints contains the tenantid:


[![image](/uploads/2019/08/image_thumb-6.png)](/uploads/2019/08/image-6.png)



With these steps the requirements are complete and we can move on to the postman client.



## Authenticating and Querying Graph with Postman



There are a lot of features in the Postman client that you should look into when working with REST API’s. You can organize your queries in Collections, save variables in Environments, synchronize your requests across devices and so on. But for now we will start simple and easy.



In the main canvas at your workspace, create a new query, and for example start with <https://graph.microsoft.com/v1.0/me>:


[![image](/uploads/2019/08/image_thumb-7.png)](/uploads/2019/08/image-7.png)



Don’t push Send just yet, we need to authenticate first. Go to the Authorization section under the request, and select Oauth2, then click Get New Access Token:


[![image](/uploads/2019/08/image_thumb-8.png)](/uploads/2019/08/image-8.png)



In the following dialog fill in your details as shown below, where:



- Token Name: You can type what you want here, this is named reference to the Access Token you will aquire.
- Grant Type: As earlier mentioned, running graph queries as the logged in user (delegated) use the Authorization Code Oauth2 flow.
- Callback URL: This is the URL that you specified earlier for Redirect URI under the Azure AD App Registration.
- Auth URL and Access Token URL: These are the URL’s you saw earlier from the Endpoints setting for the Azure AD App Registration (contains the Tenant ID).
- Client ID: This is the Application ID for the App Registration.
- Client Secret: This is the secret key you generated under the App Registration.
- Scope: Provide a default scope, use the default.
- State: Scope is used for creating application logic that prevents cross use of Access Tokens. You can type anything you want here.
- Client Authentication: Select to Send client credentials in body when working with Graph requests.


[![image](/uploads/2019/08/image_thumb-9.png)](/uploads/2019/08/image-9.png)



When you click request token, you will be taken to the resource tenant for authenticating with your delegated user. Type in your username and click next. This username can either be a normal user that belongs to this resource tenant, or in this case you can log in with your B2B Guest Account:


[![image](/uploads/2019/08/image_thumb-10.png)](/uploads/2019/08/image-10.png)



Now dependent on any Conditional Access policies and settings you might be required to approve sign in:


[![image](/uploads/2019/08/image_thumb-11.png)](/uploads/2019/08/image-11.png)



After successfully authenticating I should receive a valid Access Token:


[![image](/uploads/2019/08/image_thumb-12.png)](/uploads/2019/08/image-12.png)



If you get an error here, please verify your App Registration settings and that the account you logged in as is correct.



Scroll down and click Use Token:


[![image](/uploads/2019/08/image_thumb-13.png)](/uploads/2019/08/image-13.png)



You will see that the Access Token is now filled in the Access Token textbox. Next click Preview Request down to the left, this will add the Access Token to the request as a authorization header:


[![image](/uploads/2019/08/image_thumb-14.png)](/uploads/2019/08/image-14.png)



If you click on Headers, you can see the Authorization header has been added with the access token as a Bearer Token value:


[![image](/uploads/2019/08/image_thumb-15.png)](/uploads/2019/08/image-15.png)



This Access Token is now valid for 1 hour, and you can run as many requests you like as long as you are inside the delegated permissions (for the App Registration) and the logged in users actual permissions. After 1 hour you can request a new Access Token.



PS! Postman will save the authenticated user session in cookies, if you want to log in as a different user clear those cookies, se “cookies” link right below the Send button.



So, now lets run this query, click Send at verify the response, you should get details for your guest user. From the screenshot below you can clearly see that this user is a Guest account looking at the userPrincipalName attribute:


[![image](/uploads/2019/08/image_thumb-16.png)](/uploads/2019/08/image-16.png)



Lets try another query, in this query I list all users that has userPrincipalName that starts with “Jan”, and showing only the displayName and userPrincipalName attributes:


[![image](/uploads/2019/08/image_thumb-17.png)](/uploads/2019/08/image-17.png)



As you can see from the result above, I have several guest accounts in this tenant (Microsoft Account, Google, Azure AD) as well as a normal user account. You can also see that the Postman client is helpful in specifying my parameters.



## Inspecting a B2B Guest Access Token



If you copy the Access Token you got earlier, and paste it into a site like [jwt.ms](http://jwt.ms) or [jwt.io](http://jwt.io), we can take a look at the access token contents and claims:


[![image](/uploads/2019/08/image_thumb-18.png)](/uploads/2019/08/image-18.png)



If I scroll down a little I see the displayname of the App Registration, but the most important info is the mail claim, which for Guest users will be the external e-mail address. Idp is the source authority for the Guest account, in this case another Azure AD tenant with the Tenant Id as shown below:


[![image](/uploads/2019/08/image_thumb-19.png)](/uploads/2019/08/image-19.png)



## Working with Environments



Chances are that you might work with several environments in Postman, and that where it’s useful to create environment variables. For example create an environment like shown below:


[![image](/uploads/2019/08/image_thumb-20.png)](/uploads/2019/08/image-20.png)



That way you can select which environment you want to work with when running queries, and when referencing variables use “{{ .. }}”. For example under Get New Access Token, change to this:


[![image](/uploads/2019/08/image_thumb-21.png)](/uploads/2019/08/image-21.png)



Now, lets finalize this blog post by logging in with another guest account, I will choose my Gmail account, I’ve already set up Google Federation and invited this user to my tenant.



First I need to clear the cookies:


[![image](/uploads/2019/08/image_thumb-22.png)](/uploads/2019/08/image-22.png)



Next I will click to Get a New Access Token again, and then authenticate as my Google account, which directs me to the Google login page:


[![image](/uploads/2019/08/image_thumb-23.png)](/uploads/2019/08/image-23.png)



After successfully authenticating, and using the new Access Token in the Authorization Header, I can run the basic /me query again, this time showing me that I’m now authenticated to Graph with my Gmail user:


[![image](/uploads/2019/08/image_thumb-24.png)](/uploads/2019/08/image-24.png)



And looking inside the Access Token again, I can see that the e-mail address is my gmail and the idp is now google.com:


[![image](/uploads/2019/08/image_thumb-25.png)](/uploads/2019/08/image-25.png)



If I had logged on with a Microsoft Account the idp value would have been “live.com”.



## Next steps



So, now you know how to authenticate to and query Microsoft Graph with an Azure AD B2B Guest User. I really hope this functionality will come to Graph Explorer eventually, but for now Postman is already an awesome free tool for organizing and running your Microsoft Graph queries that I use a lot myself.



The Microsoft Graph Team has also published this source for a lot of useful collections of Graph queries:



<https://github.com/microsoftgraph/microsoftgraph-postman-collections>
