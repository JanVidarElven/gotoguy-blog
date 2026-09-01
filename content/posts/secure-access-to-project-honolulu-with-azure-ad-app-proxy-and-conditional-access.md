---
title: "Secure Access to Project Honolulu with Azure AD App Proxy and Conditional Access"
date: 2017-09-24T22:10:28Z
draft: false
slug: "secure-access-to-project-honolulu-with-azure-ad-app-proxy-and-conditional-access"
tags:
  - "Azure AD Application Proxy"
  - "Azure Multi-Factor Authentication"
categories:
  - "Azure AD"
  - "Azure AD Conditional Access"
  - "Project Honolulu"
---

Last week Microsoft announced Project “Honolulu”, the new Windows Server remote management experience, and now you can download a technical preview to install in your own data center, read here for more details: [https://blogs.technet.microsoft.com/windowsserver/2017/09/22/project-honolulu-technical-preview-is-now-available-for-download/](https://blogs.technet.microsoft.com/windowsserver/2017/09/22/project-honolulu-technical-preview-is-now-available-for-download/ "https://blogs.technet.microsoft.com/windowsserver/2017/09/22/project-honolulu-technical-preview-is-now-available-for-download/").
As the management is browser based, I thought this was a perfect fit for using Azure AD and publishing the management portal using Azure AD Application Proxy, and even better to secure the access using Azure AD Conditional Access. Consider the following diagram, where you instead of just publishing DNS and open Firewall to access the management server directly, I would instead use Azure AD App Proxy for secure access.
[![ProjectHonolulu](/uploads/2017/09/projecthonolulu_thumb.png "ProjectHonolulu")](/uploads/2017/09/projecthonolulu.png)
So lets get started setting this up!

## Install and configure Project “Honolulu” technical preview

I will not get into great detail on installing Project "Honolulu" here, you can just follow the technical deployment documentation, but in my environment I have installed some servers running as Azure Virtual Machines joined to a single-forest, single-domain Active Directory. I have “on-premises” AD users and groups, and I’m running Azure AD Connect with Password Hash Synchronization.
On one of these Azure VM’s, I’ve downloaded and installed the Project “Honolulu” technical preview, with the following configuration:

- Management Port: 6516
- Self-signed Certificate

I’m now able to access the web based management internally, using <https://azhon1.elven.local:6516>. I can now proceed with publishing this externally with Azure AD App Proxy.

## Configure Azure AD Application Proxy

Before you can publish applications using Azure AD Application Proxy, you have enable the feature in your Azure AD tenant, and install and configure one or more servers running Azure AD App Proxy Connector, and configure those in a connector group to use for the application. If you already have this configured, you can proceed to the next section. If you want more details, see this previous blog post, and the first sections on enabling App Proxy and innstalling connectors: [https://gotoguy.blog/2017/02/21/publish-the-cireson-configuration-manager-portal-with-azure-ad-application-proxy/](https://gotoguy.blog/2017/02/21/publish-the-cireson-configuration-manager-portal-with-azure-ad-application-proxy/ "https://gotoguy.blog/2017/02/21/publish-the-cireson-configuration-manager-portal-with-azure-ad-application-proxy/")

## Publish the Project Honolulu as an Azure AD App Proxy App

In the Azure AD management blade in the Azure Portal, select Enterprise Applications and click to add a new application. Select On-premises application:
[![image](/uploads/2017/09/image_thumb26.png "image")](/uploads/2017/09/image26.png) Specify a Name for your application, and the Internal Url where you installed the Project Honolulu technical preview, including port number as shown below. If you want you can change parts of the External Url, even using your own domain and SSL certificate. I will just use the default here. I will use Azure Active Directory as Pre Authentication, meaning that no-one can access this website without beeing authenticated with Azure AD first. And last, I select my Connector Group of Azure AD App Proxy Connector Servers. PS! Remember that these servers need to be able to access the Internal Url directly, in case you have any Firewalls, NSGs or other components that might block traffic.
[![image](/uploads/2017/09/image_thumb27.png "image")](/uploads/2017/09/image27.png)
After adding the application, I have to do some more configurations. First, optionally, you can select a custom logo:
[![image](/uploads/2017/09/image_thumb28.png "image")](/uploads/2017/09/image28.png)
User assignment is required in this configuration, so next I need to assign some users to the application. Here I have added a normal domain user and a domain admin user. Both these users are synchronized from my local AD.
[![image](/uploads/2017/09/image_thumb29.png "image")](/uploads/2017/09/image29.png)
Next I wan’t to configure Single Sign-On, so that users that authenticate with Azure AD automatically will be signed in to the Project Honolulu management site. I select Integrated Windows Authentication for sign-on mode, and then I specify the internal application SPN for which is needed for Kerberos Constrained Delegation.
[![image](/uploads/2017/09/image_thumb30.png "image")](/uploads/2017/09/image30.png)
After that I have one more important step, and that is to configure delegation at my Application Proxy Connector servers. In my local Active Directory, open the Computer object for every server that acts as Azure AD App Proxy Connectors, and on the Delegation tab, add the server that you installed the Project Honolulu on, selecting http as the service. In my environment, I have added this now. I have some previous delegations for others servers as well.
[![image](/uploads/2017/09/image_thumb31.png "image")](/uploads/2017/09/image31.png)
We are now ready to test the application publishing via Azure AD!

## Access Application using Azure AD

You now have basically two options for accessing the application:

- Accessing the External Url directly, in my example this is [https://projecthonolulu-elven.msappproxy.net/](https://projecthonolulu-elven.msappproxy.net/ "https://projecthonolulu-elven.msappproxy.net/")
- Access the application using Azure AD Access Panel, <https://myapps.microsoft.com>

When using the Azure AD Access Panel, if your users has been assigned access, you will see the application published:
[![image](/uploads/2017/09/image_thumb32.png "image")](/uploads/2017/09/image32.png)
When launching that, I will be automatically logged in to the Project Honolulu web site, configured via SSO and Windows Integrated Authentication:
[![image](/uploads/2017/09/image_thumb33.png "image")](/uploads/2017/09/image33.png)
And I can start managing my configured servers:
[![image](/uploads/2017/09/image_thumb34.png "image")](/uploads/2017/09/image34.png)
So, now we have successfully configured an Azure AD App Proxy Application, and can connect securely from external url using SSO with Windows Integrated Authentication and Azure AD Pre Authentication. The application also requires that only assigned users can access the application.
In the next section I will configure Conditional Access for the application.

## Configuring Conditional Access

When publishing this server management tool for external access, I wan’t to secure access as much as possible. For example, if one of my admins credentials have been leaked, I want that extra layer of security that users have to use Azure Multi-Factor Authentication when accessing the Project Honolulu application. I will configure that using Azure AD Conditional Access. On the application, I select Conditional Access as shown below:
[![image](/uploads/2017/09/image_thumb35.png "image")](/uploads/2017/09/image35.png)
I select to create a new policy, giving it a name:
[![image](/uploads/2017/09/image_thumb36.png "image")](/uploads/2017/09/image36.png)
I then select this to apply for all users:
[![image](/uploads/2017/09/image_thumb37.png "image")](/uploads/2017/09/image37.png)
Confirm that this policy applies to the Project Honolulu application:
[![SNAGHTML7d43e5d](/uploads/2017/09/snaghtml7d43e5d_thumb.png "SNAGHTML7d43e5d")](/uploads/2017/09/snaghtml7d43e5d.png)
On Conditions I can optionally configure conditions for sign-in risk, device platforms, locations and client apps, but I will just let this policy apply for all conditions for now, so I’m leaving Conditions as it is.
[![image](/uploads/2017/09/image_thumb38.png "image")](/uploads/2017/09/image38.png)
Under Access Control I select to Require Multi-Factor Authentication, and the set to Enable the policy. Note that I can select additional controls for even more secure access, but for now I just want to require MFA:
[![SNAGHTML7d8d124](/uploads/2017/09/snaghtml7d8d124_thumb.png "SNAGHTML7d8d124")](/uploads/2017/09/snaghtml7d8d124.png)
So, save the policy, and lets test how accessing the application works now.
If I either go directly to the external url, og via the Access Panel, I will now be prompted for MFA:
[![image](/uploads/2017/09/image_thumb39.png "image")](/uploads/2017/09/image39.png)
That concludes this blog post. I’m very excited for this new preview for Project “Honolulu”, and using the great Azure AD Application Proxy feature I can securely publish and access the management site from external locations and clients. And even better with Azure AD Conditional Access, I can create a policy that sets access control for multi-factor autentication requirements, and if I want I can even control which device clients and what apps they use to access.
Hopefully this has been helpful for you, if you have any questions reach out to me on Twitter or use the comments below this blog post :)
