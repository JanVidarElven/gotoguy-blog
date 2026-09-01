---
title: "Publish the Cireson Configuration Manager Portal with Azure AD Application Proxy"
date: 2017-02-20T23:39:43Z
draft: false
slug: "publish-the-cireson-configuration-manager-portal-with-azure-ad-application-proxy"
tags:
  - "Azure AD Application Proxy"
  - "Azure AD Premium"
categories:
  - "Azure AD"
  - "Cireson Configuration Manager Portal"
  - "Enterprise Mobility + Security"
---

Cireson will soon be releasing a new web based Portal for System Center Configuration Manager, [http://go.cireson.com/cireson-portal-for-configmgr](http://go.cireson.com/cireson-portal-for-configmgr "http://go.cireson.com/cireson-portal-for-configmgr"). This would make it possible to access a lot of functionality for Configuration Manager anywhere with a web browser. The Cireson Portal for Configuration Manager must be installed locally, either on the Configuration Manager server or on a server close to the Configuration Manager server and database.
This makes this an ideal candidate for Azure AD Application Proxy publishing, as we can make it available as an Azure AD App with all the features and possibilities that this can give, including:

- Azure AD Preauthentication and Single Sign-On to the Portal
- Assigning Users and Groups
- Conditional Access
- Easy access via the users Access Paneler or the Office 365 App Launcher

We will look into all this in a two-part blog post! This will also be a good opportunity to use the new management experience for the preview of Azure Active Directory management in the Azure Portal, <https://portal.azure.com>.
Part 1: Publish the Cireson Configuration Manager Portal with Azure AD Application Proxy
Part 2: Conditional Access and Self Service for the published Configuration Manager Portal Application (link when available)

## Enable Azure AD Application Proxy

I you want to publish applications with Azure AD Application Proxy, there are some requirements:

- You need an Azure AD tenant configured with licenses for Azure AD Premium P1 or EMS E3 Suite. Actually it is enough with Azure AD Basic licenses for AAD App Proxy, but if you want to configure Conditional Access you will need at least Premium P1. More on that later.
- If you want to enable SSO for your internal users you have to synchronize those users via Azure AD Connect.
- You have to Enable Azure AD Application Proxy for your AAD tenant directory, and download and install one or more Application Proxy Connectors.

The diagram below shows the communication flow from when the user launch the published application, authenticates to Azure AD, and then via the Application Proxy Connector installed internally access the web based portal. Single Sign-On is achieved via the Application Proxy Connector authentication on behalf of the user via Kerberos Constrained Delegation.
[![image](/uploads/2017/02/image_thumb36.png "image")](/uploads/2017/02/image36.png)
So the first step is to go to the Azure Portal, and open the Azure Active Directory blade, which at the moment is in preview. From there go to the Application Proxy section and make sure that the Application Proxy is enabled as shown below:
[![image](/uploads/2017/02/image_thumb37.png "image")](/uploads/2017/02/image37.png)
In the image above we also see that there already are some Azure AD App Proxy Connectors installed and active. They are also configured in two different groups, and these groups are used later when we publish the application. At the top of the blade, you can download a new Connector installation file.

## Download and install Application Proxy Connector

The Application Proxy Connector must be installed on a server that can reach the internal web portal server. In this case I want to install the Connector locally on the Configuration Manager server that also hosts the Cireson Portal for Configuration Manager. I could have used one of my existing connectors, but they are installed respectively on an Azure VM environment and on a separate network from our Configuration Manager environment.
Following the download link from above, I download and start the Application Proxy Connector installation on my SCCM server.
[![image](/uploads/2017/02/image_thumb38.png "image")](/uploads/2017/02/image38.png)
During installation you must provide a global administrator admin account:
[![image](/uploads/2017/02/image14_thumb.png "image")](/uploads/2017/02/image141.png)
After finishing the installation of the connector, we will se the new connector with the server name in the portal.
We can now create a group, and place the connector installed in the group:
[![image](/uploads/2017/02/image_thumb39.png "image")](/uploads/2017/02/image39.png)

## Publish the Configuration Manager Portal App

To start publishing the Configuration Manager Portal Application, go to Enterprise Applications and select Add, and from the Add your own app section select to add an “On-premises application”:
[![image](/uploads/2017/02/image_thumb40.png "image")](/uploads/2017/02/image40.png)
Next, specify the Name of the Application and the Internal Url. In this case I have installed it internally as <http://configmgrportal>. For External Url, you have a choice for the alias and domain. By default the alias will be the Application Name without spaces, appended with –<tenant name>.msappproxy.net.
[![image](/uploads/2017/02/image_thumb41.png "image")](/uploads/2017/02/image41.png)
You can change the domain to one of your verified domains, which I have done here together with changing the alias so that the External Url now will be <https://configmgrportal.skill.no>. By the way, you have to upload a SSL certificate if you want to use your own domain, either a wildcard certificate or a certificate with the appropriate FQDN. We will look at that later.
[![image](/uploads/2017/02/image_thumb42.png "image")](/uploads/2017/02/image42.png)
Note that I need to add a CNAME entry at my DNS provider as stated in the info box above. I will do that right now before I proceed.
I set Pre Authentication to Azure Active Directory, as I want everyone accessing the External Url to be a valid Azure AD user from my tenant. I also select to translate URL in headers, and select my previously configured App Proxy Connector Group.
Press Add to add the application to the directory. After that you are presented with a Quick start menu like below:
[![image](/uploads/2017/02/image_thumb43.png "image")](/uploads/2017/02/image43.png)
First I go to Properties, and optionally you can upload a logo which I have done here, note also that User assignment is required is set to yes, this means that no user cannot access the published application until I have added users or groups to it.
[![image](/uploads/2017/02/image_thumb44.png "image")](/uploads/2017/02/image44.png)
After saving I go to users and groups, and add some users to test the published application:
[![image](/uploads/2017/02/image_thumb45.png "image")](/uploads/2017/02/image45.png)
These users will now be able to launch the published application, but we have some more configuration to do first. As I want to have Single Sign-On configured for this application, I configure the following settings for Single Sign-On. I set the mode to Integrated Windows Authentication, meaning that the App Proxy Connector will impersonate any Azure AD authenticated user to the on-premises application via Kerberos constrained delegation.
I also need to specify a internal SPN for the application, which will be HTTP/<fqdn-of-server>, where the server is where the internal web application is installed. I will also specify which delegated login identity, which in most cases will work fine with user principal name for synchronized federated users.
[![image](/uploads/2017/02/image_thumb46.png "image")](/uploads/2017/02/image46.png)
After configuring Single Sign-On settings, and if you elected to use your own domain name, you need to upload or specify an existing SSL certificate. Go back to Application Proxy settings and click to view or change certificate settings:
[![image](/uploads/2017/02/image_thumb47.png "image")](/uploads/2017/02/image47.png)
After saving this configuration, the required portal configuration for the application is now complete, but optionally we can configure self service and conditional access, We will get back to that later in part 2 of this blog post.
That leaves only one more step, and that is to configure kerberos delegation for the App Proxy Connector server. In your on-premises Active Directory, find the computer object for the server you installed the App Proxy Connector on, and go to Delegation, and select to trust this computer for delegation to specified services only, and for kerberos only adding the computer name and http service for the server where the internal web application is installed. This should med the same as the internal spn you configured in the portal earlier for Windows integrated authentication.
[![image](/uploads/2017/02/image_thumb48.png "image")](/uploads/2017/02/image48.png)

## Testing Single Sign-On

We can now test the application. Go to <https://myapps.microsoft.com> and log in with one of the assigned users. Among other published apps I will see the Configuration Manager Portal:
[![image](/uploads/2017/02/image_thumb49.png "image")](/uploads/2017/02/image49.png)
And if I launch it, I will see that I can access the Configuration Manager Portal, and I have been automatically signed in with my local AD user via Single Sign-On and Kerberos Constrained Delegation. I also see my url, <https://configmgrportal.skill.no>, which I can access directly if I want without going through the MyApps panel.
[![image](/uploads/2017/02/image_thumb50.png "image")](/uploads/2017/02/image50.png)
So now we have successfully published the Cireson Configuration Manager Portal with Azure AD Application Proxy, using SSO with Azure AD, and User Assignment so that only users that are pre-authenticated and assigned the application by Azure AD, will have access to it.
Stay tuned for part 2 of this blog post, where we will configure Conditional Access using Azure MFA and Device Compliance, and what Self Service functionality we have.
