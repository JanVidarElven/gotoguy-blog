---
title: "Working with Azure AD Extension Attributes with Azure AD PowerShell v2"
date: 2017-02-18T22:50:36Z
draft: false
slug: "working-with-azure-ad-extension-attributes-with-azure-ad-powershell-v2"
tags:
  - "Graph API"
categories:
  - "Azure AD"
  - "Azure AD Premium"
  - "PowerShell"
---

In a recent blog post, [https://gotoguy.blog/2017/02/17/assign-ems-license-with-azure-ad-v2-powershell-and-dynamic-groups/](https://gotoguy.blog/2017/02/17/assign-ems-license-with-azure-ad-v2-powershell-and-dynamic-groups/ "https://gotoguy.blog/2017/02/17/assign-ems-license-with-azure-ad-v2-powershell-and-dynamic-groups/"), I wrote about how to use extension attributes in local Active Directory and Azure AD, for the purpose of using these extension attributes for determine membership i Azure AD Dynamic Groups.
In the process of investigating my Azure AD users (synchronized and cloud based),  I wanted to see how I could use Azure AD v2 PowerShell CmdLets for querying and updating these extension attributes. This blog post is a summary of tips and commands, and also some curious things I found. There is a link to a Gist with all the PowerShell Commands at the end of the blog post if you prefer to skip to that.
Lets start by looking into one user:
[![image](/uploads/2017/02/image_thumb26.png "image")](/uploads/2017/02/image26.png)
For my example user I have the following output:
[![image](/uploads/2017/02/image_thumb27.png "image")](/uploads/2017/02/image27.png)
In the above linked blog post, I wrote about using the msDS\_cloudExtensionAttribute1 and 2 for assigning licenses, so I see those values and more.
I can also serialize the user object to JSON by using $aadUser.ToJson(), which also will show me the value of the extension attributes:
[![image](/uploads/2017/02/image_thumb28.png "image")](/uploads/2017/02/image28.png)
I can look into and explore the user object with Get-Member:
[![image](/uploads/2017/02/image_thumb29.png "image")](/uploads/2017/02/image29.png)
From there I can see that that the Extension Property, which is of type System.Collections.Generic.Dictionary supports Get and Set. So lets look into how to update those extension attributes. This obviously only work on cloud homed users, as synchronized users must be updated in local Active Directory. This series of commands shows how to add extension attributes for cloud users:
[![image](/uploads/2017/02/image_thumb30.png "image")](/uploads/2017/02/image30.png)
The next thing I thought about, was how can I make a list of all users with their extension attributes? I ended up with the following, where you either can get all users or make a filtered collection, and from there loop through and read any extension attributes:
[![image](/uploads/2017/02/image_thumb31.png "image")](/uploads/2017/02/image31.png)
When I look into my extended users list object, I can list the users and values with extension values:
[![image](/uploads/2017/02/image_thumb32.png "image")](/uploads/2017/02/image32.png)
[![image](/uploads/2017/02/image_thumb33.png "image")](/uploads/2017/02/image33.png)
So to some curios things I found. As explained in the blog post [https://gotoguy.blog/2017/02/17/assign-ems-license-with-azure-ad-v2-powershell-and-dynamic-groups/](https://gotoguy.blog/2017/02/17/assign-ems-license-with-azure-ad-v2-powershell-and-dynamic-groups/ "https://gotoguy.blog/2017/02/17/assign-ems-license-with-azure-ad-v2-powershell-and-dynamic-groups/"), if you are running a Hybrid Exchange organization you would probably use extensionAttribute1..15 instead of the msDS\_cloudExtensionAttribute. In another Azure AD tenant I tested on that, but using the commands above I never could list out the extensionAttribute1..15 on my users. I never found a way to validate and check those values, but if I created a Dynamic Group using for example extensionAttribute1 or 2, members would be populated! So it was obvious that the value was there, I just can’t find a way to check it.
I even tested on Graph API, but did not find any extensionAttribute there either, only msDS\_cloudExtensionAttribute. For example by querying:
[https://graph.microsoft.com/v1.0/users/<userid or upn>?$select=extension\_66868723f2984d3e8c18f0ebd134240f\_msDS\_cloudExtensionAttribute2](https://graph.microsoft.com/v1.0/users/<userid or upn>?$select=extension_66868723f2984d3e8c18f0ebd134240f_msDS_cloudExtensionAttribute2 "https://graph.microsoft.com/v1.0/users/jve.admin@elven.onmicrosoft.com?$select=extension_66868723f2984d3e8c18f0ebd134240f_msDS_cloudExtensionAttribute2")
[![image](/uploads/2017/02/image_thumb34.png "image")](/uploads/2017/02/image34.png)
I can see my extension value.
However, if I try: [https://graph.microsoft.com/v1.0/users/<userid or upn>?$select=extensionAttribute2](https://graph.microsoft.com/v1.0/users/<userid or upn>?$select=extensionAttribute2 "https://graph.microsoft.com/v1.0/users/jve.admin@elven.onmicrosoft.com?$select=extension_66868723f2984d3e8c18f0ebd134240f_msDS_cloudExtensionAttribute2"), I cannot see the value even I know it’s there.
[![image](/uploads/2017/02/image_thumb35.png "image")](/uploads/2017/02/image35.png)
Strange thing, hopefully I will find out some more on this, and please comment if you have any ideas. I will also ask this from the Azure AD team.
Here is the gist with all the commands:
https://gist.github.com/skillriver/534191d66de951b9c27a631a5a741caa
