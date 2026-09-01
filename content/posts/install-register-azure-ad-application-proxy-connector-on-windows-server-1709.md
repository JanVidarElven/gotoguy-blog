---
title: "Install &amp; Register Azure AD Application Proxy Connector on Windows Server 1709"
date: 2018-02-19T11:43:09Z
draft: false
slug: "install-register-azure-ad-application-proxy-connector-on-windows-server-1709"
tags:
  - "Azure AD Application Proxy"
  - "PowerShell"
categories:
  - "Azure AD"
  - "Enterprise Mobility + Security"
  - "Windows Server 1709"
---

I recently installed the new release of Windows Server, version 1709 on my Intel NUC, [you can read about that here](https://gotoguy.blog/2018/02/13/installing-windows-server-version-1709-on-intel-nuc-skull-canyon-and-configure-hyper-v-for-remote-management/).
I have installed Project Honolulu for remote server management on that server, but as this Intel NUC is usually located on my home lab network, I want to be able to publish and access the Honolulu website using Azure AD Application Proxy.
As the Windows Server 1709 is Server Core, I need to install and configure the Azure AD Application Proxy Connector silently, and these are the steps I did to do that.
First, you need to download the Application Proxy connector install file, and transfer it to the server. You can access the connector download from Application Proxy section in your Azure AD portal:
[![image](/uploads/2018/02/image_thumb.png "image")](/uploads/2018/02/image.png)
After that, run the following command to do a quiet install of the connector, skipping registration interactively:
AADApplicationProxyConnectorInstaller.exe REGISTERCONNECTOR="false" /q
[![image](/uploads/2018/02/image_thumb1.png "image")](/uploads/2018/02/image1.png)
Next we need to register the Application Proxy connector to Azure AD, and for that we need to run some PowerShell commands. There are two ways this can be done, with a Credential Object, or using an Offline Token. Using Credential is simplest, but has the drawback that you cannot use that method if your Global Administrator account is protected with Azure MFA. Lets look at both methods below.
Using Credential Object:
On the Server you want to register the Azure AD App Proxy Connector, start a PowerShell session and run the following commands for setting the Global Administrator user name and password, and then create a Credential Object.
[![image](/uploads/2018/02/image_thumb2.png "image")](/uploads/2018/02/image2.png)
After that, run the following commands to run the RegisterConnector.ps1 script for register the connector using Credential object as authentication:
[![image](/uploads/2018/02/image_thumb3.png "image")](/uploads/2018/02/image3.png)
You can copy the PowerShell commands used above using the Gist linked at the end of this blog post.
Using Offline Token:
If you can’t or don’t want to use a credential object, you have to use a offline token. The following commands will get an access token for the authorization context needed for Application Proxy Connector Registration.
Getting the Token can be run from any client, and then transferred to the server, but you will need to have the [Azure Active Directory Authentication Library (ADAL)](https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-authentication-libraries) installed at the machine you are running the PowerShell commands. The easiest way to get the needed libraries installed is to Install the AzureAD PowerShell Module.
The following commands locates the AzureAD (or AzureADPreview) Module, and then finds the ADAL Helper Library: Microsoft.IdentityModel.Clients.ActiveDirectory.dll, and adds that as a Type to the PowerShell session:
[![image](/uploads/2018/02/image_thumb4.png "image")](/uploads/2018/02/image4.png)
Next, run these commands to define some constants, these values are the same for all tenants:
[![image](/uploads/2018/02/image_thumb5.png "image")](/uploads/2018/02/image5.png)
Now we can run these commands for setting the authentication context and then prompt user for AuthN:
[![image](/uploads/2018/02/image_thumb6.png "image")](/uploads/2018/02/image6.png)
Running the above commands will result in an authentication prompt, this is where you would specify your Global Administrator account, and if MFA enabled this will also work:
[![image](/uploads/2018/02/image_thumb7.png "image")](/uploads/2018/02/image7.png)
After authenticating we can check the result and save the token and tenantId in variables as shown below:
[![image](/uploads/2018/02/image_thumb8.png "image")](/uploads/2018/02/image8.png)
Next, copy the contents of the $token and $tenantId to the Windows Server 1709, and run the following command to create a secure string from the token:
[![image](/uploads/2018/02/image_thumb9.png "image")](/uploads/2018/02/image9.png)
And then run the RegisterConnector.ps1 script with AuthenticationMode as Token and using the secure token and tenant id as parameter values as shown below:
[![image](/uploads/2018/02/image_thumb10.png "image")](/uploads/2018/02/image10.png)
PS! According to the [official documentation](https://docs.microsoft.com/en-us/azure/active-directory/active-directory-application-proxy-silent-installation), there are no description or examples for the mandatory parameter “Feature”, but I found that it accepts the value “ApplicationProxy” as used above.
You can copy the above PowerShell commands from the Gist linked at the end of this blog post.
https://gist.github.com/skillriver/0945e9be4a98cadf9d54dce95c9c160f?file=RegisterAppProxyConnectorCredential.ps1
So to recap, after installing the Application Proxy Connector silently on the Windows Server 1709, and then registering the connector, I can now verify in the Azure AD Portal that the connector is available for use. I can see it has a status of Active, from my home IP address, and I have already placed it in a Connector Group.
[![image](/uploads/2018/02/image_thumb11.png "image")](/uploads/2018/02/image11.png)
I’m now ready to publish Azure AD Proxy Apps using this connector, and in my next blogpost I will publish the Project Honolulu management website using this!
Here is the Gist source for the above linked PowerShell commands:
https://gist.github.com/skillriver/0945e9be4a98cadf9d54dce95c9c160f
