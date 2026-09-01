---
title: "Oauth Authentication to Microsoft Graph with PowerShell Core"
date: 2020-05-06T13:04:40Z
draft: false
slug: "oauth-authentication-to-microsoft-graph-with-powershell-core"
tags:
  - "PowerShell Core"
categories:
  - "Azure AD"
  - "Microsoft Graph"
  - "PowerShell"
---

In this short blog post I will show you a really simple way to get started authenticating with Oauth to Microsoft Graph using PowerShell Core.



As you might know, PowerShell Core is the open-source, cross-platform (Windows, macOS, and Linux) edition of PowerShell, with the latest version today being PowerShell 7.0 ( <https://docs.microsoft.com/en-us/powershell/scripting/whats-new/what-s-new-in-powershell-70?view=powershell-7>). The latest version of Windows PowerShell is 5.1, and runs side-by-side with PowerShell Core.



I've been using Windows PowerShell mostly previously, as I'm running Windows 10 and use a lot of PowerShell modules that variously depend on SDKs or other Windows Components, but I'm increasingly using PowerShell Core in scenarios for example with Azure Functions PowerShell ( <https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-powershell>). My computer now runs Visual Studio Code and Windows Terminal with different Profiles, so that I can easily change between environments and run side-by-side:


![](/uploads/2020/05/image.png?w=524)



This blog post isn't about the details of PowerShell though, so lets get back to the topic at hand. When running PowerShell against Microsoft Graph you would run requests using the command **Invoke-RestMethod**. The thing that caught my attention was the added parameters of specifying Authentication and Token with the request: <https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod?view=powershell-7#parameters>.



Let's compare the "old" way and the "new" way, but first lets get an Access Token for Microsoft Graph.



## Get Access Token using Graph Explorer



If you want to learn Microsoft Graph and start with some sample queries, Graph Explorer should be your main starting point: <https://developer.microsoft.com/en-us/graph/graph-explorer/preview>. The new preview version of the Graph Explorer lets you get a copy of your Access Token if you sign in with your account as shown below, you can copy it to your clipboard:


![](/uploads/2020/05/image-1.png?w=1024)



This Access Token will run queries as the logged on user (yourself) using the consented permissions in Graph Explorer, so you should only use this token for your own sample queries and not share it with anyone else.



Preferably you would get an Access Token by registering your own App Registration in Azure AD and authenticate using one of the following authentication flows:



- Authorization Code Flow (Delegated User - Web Apps and APIs)
- Device Code Flow (Delegated User - Native Clients, recommended for PowerShell)
- Client Credentials Flow (Application Permissions - Scripts and Background Processes that don't require user interactivity)



But for now I would use use the Access Token from Graph Explorer for the following samples.



## The "old" way, using Authorization Header with Bearer Token



This method works with both Windows PowerShell and PowerShell Core. After aquiring an Access Token you would need to specify an Authorization Header with a Bearer Token for every request. In this example I get the Access Token from the Clipboard, as I copied that from the Graph Explorer.



```powershell
$accessToken = Get-Clipboard  
Invoke-RestMethod -Method Get -Uri "https://graph.microsoft.com/v1.0/me" -Headers @{"Authorization"="Bearer $accessToken"}
```



This should return a response like below:


![](/uploads/2020/05/image-2.png?w=1024)



## The "new" way, using Authentication and Token Parameters



This method only works on PowerShell Core. The Access Token needs to be a secure string, so you need to convert it first like the following:



```powershell
$accessToken = ConvertTo-SecureString (Get-Clipboard) -AsPlainText -Force
```



Another way would be to prompt for the Access Token and paste it with the following command:



```powershell
$accessToken = Read-Host -AsSecureString -Prompt "Enter/Paste Oauth2 Token"
```



And then you would run the request specifying the Authentication parameter to be Oauth, and the Token parameter to be the secure string:



```powershell
Invoke-RestMethod -Method Get -Uri "https://graph.microsoft.com/v1.0/me" -Authentication OAuth -Token $accessToken
```



This should return a response like below:


![](/uploads/2020/05/image-4.png?w=1024)



## Summary



So in summary you can start using the Authentication and Token parameters in PowerShell Core, it would add / override the Authorization Header and Bearer Token for you. There can also be some added security gains as the Token is submitted as a securestring, which means you can try to keep it out of code as clear text.
