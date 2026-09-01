---
title: "Configure Azure AD Authentication for Project Honolulu version 1803"
date: 2018-03-16T07:03:01Z
draft: false
slug: "configure-azure-ad-authentication-for-project-honolulu-version-1803"
categories:
  - "Azure AD"
  - "Azure AD Conditional Access"
  - "Project Honolulu"
  - "Windows Server 1709"
---

Just a few days ago a new version of Project Honolulu, technical preview 1830, was released for Windows Server Insiders, [https://blogs.windows.com/windowsexperience/2018/03/13/announcing-project-honolulu-technical-preview-1803-and-rsat-insider-preview-for-windows-10/](https://blogs.windows.com/windowsexperience/2018/03/13/announcing-project-honolulu-technical-preview-1803-and-rsat-insider-preview-for-windows-10/ "https://blogs.windows.com/windowsexperience/2018/03/13/announcing-project-honolulu-technical-preview-1803-and-rsat-insider-preview-for-windows-10/").
One of the major updates to that version was the support for changing access control from local group/Active Directory to **Azure AD Authentication**. Configuring Azure AD Authentication will provide the ability to pre-authenticate users with their Azure AD credentials, as well as restrict access to selected users or even integrate with Azure AD Conditional Access.
In this blog post I will provide some steps, examples and screenshots for how I did that configuration in my own environment.
This scenario builds on the previous installation I have made with Windows Server 1709 (Server Core) and Project Honolulu, see blog article for how my setup is: <http://gotoguy.blog/2018/02/13/installing-windows-server-version-1709-on-intel-nuc-skull-canyon-and-configure-hyper-v-for-remote-management/>

## Update existing version of Project Honolulu to version 1803

Since I had an existing installation of Project Honolulu on this server ELVEN-NUC-HV1.nuc.group, I downloaded the 1803 installation file, connected to the server and ran the following command to silently install and update the existing installation:
msiexec /i HonoluluTechnicalPreview1803.msi /qn /L\*v log1803.txt SME\_PORT=443 SSL\_CERTIFICATE\_OPTION=generate
After that I navigated to the https://elven-nuc-hv1.nuc.group url from my client machine, and verified that I could sign in and see that the Project Honolulu website was updated.
[![image](/uploads/2018/03/image_thumb.png "image")](/uploads/2018/03/image.png)
I also note the certificate warning I receive because my client doesn’t trust the self generated certificate the gateway server installation provided. This will be a problem when using Azure AD Authentication, so in the next step I will make sure the client trusts that.

## Export and trust self signed certificate

First, start a PowerShell session on the Honolulu Gateway Server, and then run the command:

```powershell
Get-ChildItem –Path cert:\LocalMachine\My | FL
```

This will return any certificates in the machine store. As I have previously installed and generated a self signed certificate for Project Honolulu gateway server, I see 2 certificates now, and can note the thumbprint for the most recent one:
[![image](/uploads/2018/03/image_thumb1.png "image")](/uploads/2018/03/image1.png)
Next I will run the following commands for getting the certificate and exporting it to a .cer file:

```powershell
$cert = (Get-ChildItem –Path cert:\LocalMachine\my\<THUMBPRINT>)
```

```powershell
Export-Certificate –Cert $cert –FilePath <path>\<filename>.cer.
```

In my enviroment I ran the following:
![image](/uploads/2018/03/image_thumb2.png "image")After that, transfer the .cer file to the client computer(s) you want to be able to connect to the Project Honolulu website, and run the following commands to get and import the .cer certificate into trusted root store:

```powershell
$cert = (Get-ChildItem –Path <path>\<filename>.cer)
```

```powershell
$cert | Import-Certificate –CertStoreLocation cert:\LocalMachine\Root
```

In my enviroment this looked like this (from an elevated PowerShell window):
[![image](/uploads/2018/03/image_thumb3.png "image")](/uploads/2018/03/image2.png)
I took the extra step of verifying that the self signed certificate indeed was imported into trusted root store:
[![image](/uploads/2018/03/image_thumb4.png "image")](/uploads/2018/03/image3.png)

## Change Access Control to Azure AD

Now I am ready to change access control in Project Honolulu. Click on the Settings cogwheel, and under Settings click Access.
My current settings are set to Active Directory or Local groups, so I click on Change access control:
[![image](/uploads/2018/03/image_thumb5.png "image")](/uploads/2018/03/image4.png)
I then change to Azure Active Directory (AAD), and see the prerequisites for connecting the gateway to Azure:
[![image](/uploads/2018/03/image_thumb6.png "image")](/uploads/2018/03/image5.png)
I downloaded the New-AadApp.ps1 script, note that this script requires the modules AzureRM.Resources and AzureAD to be installed at the machine where you run the script. If you don’t have them installed, you can install these using Install-Module, as shown in this example:
[![image](/uploads/2018/03/image_thumb7.png "image")](/uploads/2018/03/image6.png)
I chose to run this script on my client computer (not on my server core gateway computer), and with the following command:
.\New-AadApp1803.1.ps1 –GatewayEndpoint https://elven-nuc-hv1.nuc.group
(PS! I didn't have the AzureAD module installed, but the AzureADPreview module instead. A simple change in the Requires section of the script fixed that;)
Running the script prompted me to specify a Global Administrator account for the tenant I wanted to register the Azure AD App in, and after sucessfully authenticating I got confirmation. Note the AAD Application name and other Id’s:
[![image](/uploads/2018/03/image_thumb8.png "image")](/uploads/2018/03/image7.png)
Back at the Access Control settings, refresh the browser, note the changed instructions show in the dialog below, and then Save. This will restart the gateway service.
[![image](/uploads/2018/03/image_thumb9.png "image")](/uploads/2018/03/image8.png)
After refreshing the browser again, you will be prompted by the following consent for permissions (provided that you already had an active logged on session, or else you will prompted to log in to the tenant you registered the app in):
[![image](/uploads/2018/03/image_thumb10.png "image")](/uploads/2018/03/image9.png)
After successfully authenticating and accepting, I’m logged into the Project Honolulu website. Under Settings and Azure, I can verify that I’m logged in and sign out again if needed.
[![image](/uploads/2018/03/image_thumb11.png "image")](/uploads/2018/03/image10.png)

## Logging on with other users from the tenant

Remember by default all members of the Azure AD tenant will have **user** **access** to the Honolulu gateway service. That includes any B2B Guest Users!
Each user logging in need to first time consent to permissions, in the following screenshots I have logged on with a normal user account and then a B2B guest account:
[![image](/uploads/2018/03/image_thumb12.png "image")](/uploads/2018/03/image11.png)[![image](/uploads/2018/03/image_thumb13.png "image")](/uploads/2018/03/image12.png)
Only local administrators on the gateway machine will have administrator access to the Honolulu gateway.
Under Access Settings you can click on a link to go directly to the Azure AD App that got registered when you ran the script earlier:
[![image](/uploads/2018/03/image_thumb14.png "image")](/uploads/2018/03/image13.png)
Clicking on that link and logging in with a Global Administrator, you will get to your SME-<name> app. From there you can go to users and groups, and all users that have logged in until now will be listed. By default they will not have any role assigned, but you can change role between Gateway Administrator or Gateway User as I have done below:
[![image](/uploads/2018/03/image_thumb15.png "image")](/uploads/2018/03/image14.png)
If you want to restrict which users or groups that are allowed to log into the Project Honolulu site with their Azure AD Credentials, you can go to Properties and then enable the setting for require user assignment:
[![image](/uploads/2018/03/image_thumb16.png "image")](/uploads/2018/03/image15.png)
After enabling this setting users that aren’t added to the list of users or groups either directly or via group membership will not be allowed to log on to Project Honolulu.

## Summary and next steps

In this blog post I have shown a first look for enabling Azure AD Authentication for Project Honolulu version 1803 technical preview.
The next step is to look into configuring Azure AD Conditional Access for this application, that will come in a later update to this blog article, stay tuned!
A couple of issues is also on my list:

- I’m prompted to log on with local admin credentials in addition to the Azure AD credentials
- When I follow the link from Access Control settings I’m able to find the Azure AD App, but I cannot see it by just browsing the Enterprise Applications list. Based on the documentation I this should have work. This means for now I cannot add that App to any Conditional Access policies as it is not browseable.
- The .\New-AadApp1803.1.ps1 script cannot be run on the Windows Server 1709 core version, as there is no GUI and I get iframe errors, it could be that this is related to the issue above, as I ran the script on my client instead.

I will also look into these issues in an update to this blog post. Please comment below if you are seeing similar issues or have any other experiences. Thanks for reading :)
