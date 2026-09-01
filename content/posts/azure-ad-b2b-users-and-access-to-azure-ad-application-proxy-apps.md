---
title: "Azure AD B2B Users and Access to Azure AD Application Proxy Apps"
date: 2017-11-23T22:31:17Z
draft: false
slug: "azure-ad-b2b-users-and-access-to-azure-ad-application-proxy-apps"
tags:
  - "Azure AD Application Proxy"
categories:
  - "Azure AD"
  - "Azure AD B2B"
---

The purpose of this blog post is to show a practical approach and some guidelines for publishing Azure AD App Proxy applications to guest users using Azure AD B2B.
To keep this blog post short and to the point, I will make the following assumptions:

- You have an on-premises AD and Azure AD Connect set up for synchronizing users and groups to Azure AD.
- You have already set up Application Proxy connectors and connector groups (if you want a walkthrough on this, see this blog post <http://gotoguy.blog/2017/09/24/secure-access-to-project-honolulu-with-azure-ad-app-proxy-and-conditional-access/>
- You have published one or more Azure AD App Proxy applications.
- Your tenant is configured for allowing Azure AD B2B users and you have invited one or more guests.

## Demo scenario

I will first give a quick overview over the demo scenario for this blog post:

- I will use my tenant elven.onmicrosoft.com, where I have configured a custom domain elven.no.
- I have invited an external user: [jan.vidar.elven@skill.no](mailto:jan.vidar.elven@skill.no) to the elven.onmicrosoft.com tenant. This user has accepted the invitation and can access resources that will be shared.
- I have published some App Proxy applications, and in this scenario I will use Cireson Portal, which is a Self Service Portal for SCSM.

In this blog post I will use both single sign-on disabled with forms based authentication, and single sign-on with windows integrated authentication for this guest user, but lets first verify that the guest user can log on to my application panel.

## Using Azure AD Access Panel as Guest User

When I log on to the Azure AD Access Panel at <https://myapps.microsoft.com> as external account I will se all my published applications at my company Skill AS, and since I have been added as a Azure AD B2B guest to the Elven Azure AD tenant, I can switch to that tenant like this:
[![image](/uploads/2017/11/image_thumb.png "image")](/uploads/2017/11/image.png)
I will then be redirected to the Elven Azure AD tenant and all my published applications will show (but for now this is none):
[![image](/uploads/2017/11/image_thumb1.png "image")](/uploads/2017/11/image1.png)
So lets start by adding this external guest to a published application without single sign-on and Windows Integrated Authentication enabled.

## Without Single Sign-On

First, this is the guest user I will add to the application:
[![image](/uploads/2017/11/image_thumb2.png "image")](/uploads/2017/11/image2.png)
Then I go to the App Proxy Application, and in the properties I have required that any user must be assigned to access the application:
[![image](/uploads/2017/11/image_thumb3.png "image")](/uploads/2017/11/image3.png)
Under Application Proxy I will require pre authentication with Azure AD, so that users can not access the URL without being logged on to the tenant (in this case as a guest):
[![image](/uploads/2017/11/image_thumb4.png "image")](/uploads/2017/11/image4.png)
In this first scenario single sign-on with Azure AD and Windows Integrated Authentication is disabled:
[![image](/uploads/2017/11/image_thumb5.png "image")](/uploads/2017/11/image5.png)
Then I add my guest user as an assigned user to the application:
[![image](/uploads/2017/11/image_thumb6.png "image")](/uploads/2017/11/image6.png)
In the meantime I have configured the Cireson Portal to use Forms Based Authentication, and now we can test the guest user:
In the Access Panel my guest user can now see and launch the Cireson Portal published application:
[![image](/uploads/2017/11/image_thumb7.png "image")](/uploads/2017/11/image7.png)
And my guest user can successfully get to the web application which now presents a user login form, which will require a on-premises AD user with access rights to the Cireson Portal.
[![image](/uploads/2017/11/image_thumb8.png "image")](/uploads/2017/11/image8.png)
In my on-premises AD I have created just that, a user with the account name jan.vidar.guest:
[![image](/uploads/2017/11/image_thumb9.png "image")](/uploads/2017/11/image9.png)
And I can successfully log on with the guest user:
[![image](/uploads/2017/11/image_thumb10.png "image")](/uploads/2017/11/image10.png)
So far we have seen that an Azure AD B2B user can successfully launch an Azure AD App Proxy application, and in the next step log on with a local AD user with access to the application.
I the next section we will see how we can provide single sign-on with Azure AD and Windows Integrated Authentication.
PS! I will also change the Cireson Portal to use Windows Authentication before this next step!

## Azure AD Single Sign-On and Windows Integrated Authentication

First I will need to change the settings for the Azure AD App Proxy application.
Under Single sign-on I will change to Integrated Windows Authentication, specify a SPN for Kerberos Constrained Delegation, and specify to use User principal name for delegated login identity:
[![image](/uploads/2017/11/image_thumb11.png "image")](/uploads/2017/11/image11.png)
By now you might have realized that for single sign-on to work with windows integrated authentication in a Azure AD B2B guest user scenario, you will need to have a “shadow” AD user for this external scenario. In my first test above, I had created a “jan.vidar.guest” user. Remember that I chose to use User principal name as a delegated login identity. So I will need a UPN that will be a link between my Azure AD guest user account ([jan.vidar.elven@skill.no](mailto:jan.vidar.elven@skill.no)) and the local AD user. If that link is missing, you will see the following in the Application Proxy Connector Log:
[![image](/uploads/2017/11/image_thumb12.png "image")](/uploads/2017/11/image12.png)
So this error message tells us exactly what user principal name is expected from the guest user. The error message below provide more details from this error:
Web Application Proxy encountered an unexpected error while processing the request.
Error: The user name or password is incorrect.
(0x8007052e)
Details:
Transaction ID: {00000000-0000-0000-0000-000000000000}
Session ID: {00000000-0000-0000-0000-000000000000}
Published Application Name:
Published Application ID:
Published Application External URL: <https://selfservice-elven.msappproxy.net/>
Published Backend URL: <http://azscsmms3/>
User: jan.vidar.elven\_skill.no#EXT#@elven.onmicrosoft.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299
Device ID: <Not Applicable>
Token State: NotFound
Cookie State: NotFound
Client Request URL: <https://selfservice-elven.msappproxy.net/Home/NavigationNodes>
Backend Request URL: <Not Applicable>
Preauthentication Flow: PassThrough
Backend Server Authentication Mode: WIA
State Machine State: OuOfOrderFEHeadersWriting
Response Code to Client: 500
Response Message to Client: Internal Server Error
Client Certificate Issuer: <Not Found>
Response Code from Backend: <Not Applicable>
Frontend Response Location Header: <Not Applicable>
Backend Response Location Header: <Not Applicable>
Backend Request Http Verb: <Not Applicable>
Client Request Http Verb: POST
So, lets change the UPN of my local shadow user to that. You can either add the UPN suffix to your Active Directory Forest, or change the user principal name with AD PowerShell like:

```powershell
Set-ADUser jan.vidar.guest -UserPrincipalName jan.vidar.elven_skill.no#EXT#@elven.onmicrosoft.com
```

[![image](/uploads/2017/11/image_thumb13.png "image")](/uploads/2017/11/image13.png)
Generally you will need to add Azure AD B2B users with user principal name in the form of:
<emailalias>\_guestdomain#EXT#tenantdomain
So, lets try to launch the Cireson Portal again now, this time with Azure AD Single Sign-On and Windows Integrated Authentication:
[![image](/uploads/2017/11/image_thumb14.png "image")](/uploads/2017/11/image14.png)
And now the user will be logged directly into the Cireson Portal with SSO:
[![image](/uploads/2017/11/image_thumb15.png "image")](/uploads/2017/11/image15.png)
So now we have seen that we can successfully use Azure AD B2B Guests in an Azure AD Application Proxy published application scenario, with or without Single Sign-On, and that we require a link with the delegated identiy with a “shadow” user in the on-premises AD.
NB! Before you think that you should create that user as a disabled account, this is what happens:
[![image](/uploads/2017/11/image_thumb16.png "image")](/uploads/2017/11/image16.png)
This means, you have to **enable** the AD user account, but the password can be anything and don’t have to be shared with the external user.

## Update: Require MFA from Guest Users

I have had some questions on how requiring MFA would affect guest users when accessing published applications, and decided to update the blog post on this.
First of all you would need to create an Azure AD Conditional Access Policy where you:

- Target the policy to your guest users, for example by creating a group (assigned or dynamic) with all guest users in your tenant.
- Target the policy to your selected published Azure AD App Proxy Apps.
- Setting the policy to require MFA.

Your guest users will have to set up their security verification methods in your tenant before they can authenticate with MFA as guests to your published application. They will be prompted to do that if they haven't done it before at first time, but they can also do that by accessing their profile in your tenants myapps.microsoft.com. See below picture where my guest user can set up preferred methods for MFA in the elven tenant:
![MFAGuest4](/uploads/2017/11/mfaguest4.png)
In this example I have set up Microsoft Authenticator on my mobile phone, and note the #EXT# identity which is the guest user for Elven tenant:
![MFAGuest2](/uploads/2017/11/mfaguest2.png)
I can the select to launch the application as a guest user, and will be prompted authenticate with my selected method for MFA:
![MFAGuest3](/uploads/2017/11/mfaguest3.png)
In my mobile phone I can approve, again I can see that I authenticate with my #EXT# guest account (most text in Norwegian, but you get the idea;)
![MFAGuest1](/uploads/2017/11/mfaguest1.png)
See notes under for license requirements for MFA and guest users.

## Notes and tips

Although Azure AD B2B is a free feature, creating local users in Active Directory and accessing resources like web servers, database servers and any third party applications you publish are not free and you will have to check your licensing requirements.
You shouldn’t synchronize your shadow guest users to Azure AD with Azure AD Connect.
Using Azure AD Conditional Access for require MFA is an Azure AD Premium feature, so you need EMS E3 or Azure AD Premium P1 licenses. You can then use up to 5 Azure AD B2B guests per EMS E3/AADP1 license you own, in a 1:5 ratio. So for example if you internally have 100 EMS licenses, you can require MFA for up to 500 Azure AD B2B guests.
And finally, Microsoft has noted that there will be guidance and documentation coming for best practice and governance for these Azure AD and on-premises AD guest users, as there can be a lot more complex enviroments than my example here, see this link: [https://techcommunity.microsoft.com/t5/Azure-Active-Directory-B2B/AAD-Application-Proxy-and-B2B-Users/td-p/85249](https://techcommunity.microsoft.com/t5/Azure-Active-Directory-B2B/AAD-Application-Proxy-and-B2B-Users/td-p/85249 "https://techcommunity.microsoft.com/t5/Azure-Active-Directory-B2B/AAD-Application-Proxy-and-B2B-Users/td-p/85249")
