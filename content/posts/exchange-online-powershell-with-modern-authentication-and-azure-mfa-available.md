---
title: "Exchange Online PowerShell with Modern Authentication and Azure MFA available!"
date: 2017-01-12T10:57:31Z
draft: false
slug: "exchange-online-powershell-with-modern-authentication-and-azure-mfa-available"
tags:
  - "Exchange Online"
  - "MFA"
categories:
  - "Azure AD"
  - "Azure MFA"
  - "PowerShell"
---

A while back I wrote a blog post on how you could use Azure AD Privileged Identity Management to indirectly require MFA for Office 365 Administrator Roles activation before they connected to Exchange online via Remote PowerShell. See <http://gotoguy.blog/2016/09/09/how-to-enable-azure-mfa-for-online-powershell-modules-that-dont-support-mfa/>.
In december a new Exchange Online Remote PowerShell Module was released (in preview), [https://technet.microsoft.com/en-us/library/mt775114(v=exchg.160)](https://technet.microsoft.com/en-us/library/mt775114(v=exchg.160 "https://technet.microsoft.com/en-us/library/mt775114(v=exchg.160)"), that uses Modern Authentication and that supports Azure Multi-Factor Authentication. Lets try it out:
First you need to verify that Modern Authentication is enabled in your Exchange Online organization, as this is not enabled by default: [https://support.office.com/en-us/article/Enable-Exchange-Online-for-modern-authentication-58018196-f918-49cd-8238-56f57f38d662?ui=en-US&rs=en-US&ad=US](https://support.office.com/en-us/article/Enable-Exchange-Online-for-modern-authentication-58018196-f918-49cd-8238-56f57f38d662?ui=en-US&rs=en-US&ad=US "https://support.office.com/en-us/article/Enable-Exchange-Online-for-modern-authentication-58018196-f918-49cd-8238-56f57f38d662?ui=en-US&rs=en-US&ad=US")
In my Exchange Online organization I verify that Modern Authentication is enabled:
[![image](/uploads/2017/01/image_thumb.png "image")](/uploads/2017/01/image.png)
Next logon to your Exchange Online Admin Center, and go to Hybrid to download and configure the Exchange Online PowerShell Module:
[![image](/uploads/2017/01/image_thumb1.png "image")](/uploads/2017/01/image1.png)
The configure button activates a click once install:
[![image](/uploads/2017/01/image_thumb2.png "image")](/uploads/2017/01/image2.png)
After installation I’m ready to connect:
[![image](/uploads/2017/01/image_thumb3.png "image")](/uploads/2017/01/image3.png)
Lets try it out on a MFA enabled admin user:
[![image](/uploads/2017/01/image_thumb4.png "image")](/uploads/2017/01/image4.png)
And as expected, I’m prompted to provide my verification code:
[![image](/uploads/2017/01/image_thumb5.png "image")](/uploads/2017/01/image5.png)
And after verification I can administer Exchange Online:
[![image](/uploads/2017/01/image_thumb6.png "image")](/uploads/2017/01/image6.png)
So with that we are finally able to log in to Exchange Online PowerShell more securely with Azure Multi-Factor Authentication as long as Modern Authentication is enabled for your organization!
