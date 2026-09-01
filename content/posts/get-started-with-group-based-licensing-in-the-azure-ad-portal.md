---
title: "Get Started with Group Based Licensing in the Azure AD Portal!"
date: 2017-02-22T08:03:33Z
draft: false
slug: "get-started-with-group-based-licensing-in-the-azure-ad-portal"
categories:
  - "Azure AD"
  - "Azure AD Premium"
  - "Enterprise Mobility + Security"
---

Just the other day I wrote a blog post on how you could use Azure AD v2 PowerShell and Dynamic Groups based on extension attributes to set EMS license plans for your cloud and on-premises users, [https://gotoguy.blog/2017/02/17/assign-ems-license-with-azure-ad-v2-powershell-and-dynamic-groups/](https://gotoguy.blog/2017/02/17/assign-ems-license-with-azure-ad-v2-powershell-and-dynamic-groups/ "https://gotoguy.blog/2017/02/17/assign-ems-license-with-azure-ad-v2-powershell-and-dynamic-groups/").
And now, User and Group based licensing in the Azure AD Portal has been added in Preview! This is a long awaited feature, and works will all of your purchased services, either its EMS, Office 365, Dynamics 365, PowerBI and many more.
Let’s take a quick look on the functionality. Based on the above referenced blog post, I will use the same Dynamic Groups, where membership is defined based on values for extension attributes. So I already have configured Dynamic Groups for EMS E3, EMS E5and Office 365:
[![image](/uploads/2017/02/image_thumb51.png "image")](/uploads/2017/02/image51.png)
The new Licensing functionality are now added to the Azure AD Preview at <https://portal.azure.com>:
[![image](/uploads/2017/02/image_thumb52.png "image")](/uploads/2017/02/image52.png)
When I go to the Licenses blade I get a quick overview over my purchased products and total of assigned licenses:
[![image](/uploads/2017/02/image_thumb53.png "image")](/uploads/2017/02/image53.png)
When I go to All products, a list of my product subscriptions are shown, with an overview of licenses assigned, available and if any are expiring soon:
[![image](/uploads/2017/02/image_thumb54.png "image")](/uploads/2017/02/image54.png)
If I go into one of the products, I will see the already existing licensed users, which in my case are Direct assigned (I did that with the PowerShell script in the previous blog post).
[![image](/uploads/2017/02/image_thumb55.png "image")](/uploads/2017/02/image55.png)
Let’s configure Licensed Groups:
[![image](/uploads/2017/02/image_thumb56.png "image")](/uploads/2017/02/image56.png)
Click + Assign to add a group to License, I will use my Dynamic Group:
[![image](/uploads/2017/02/image_thumb57.png "image")](/uploads/2017/02/image57.png)
Then, at Assignment options, I can optionally configure individual services:
[![image](/uploads/2017/02/image_thumb58.png "image")](/uploads/2017/02/image58.png)
After clicking OK and Assign, the group has been added for processing:
[![image](/uploads/2017/02/image_thumb59.png "image")](/uploads/2017/02/image59.png)
And if I look at Licensed Users again after the change has been processed, I will see that uses now have an inherited license based on the group. Of course, the Direct assignments added by PowerShell are not removed, so I will have to remove those later.
[![image](/uploads/2017/02/image_thumb60.png "image")](/uploads/2017/02/image60.png)
In the same way I can add my Office 365 and EMS E5 Dynamic Groups:
[![image](/uploads/2017/02/image_thumb61.png "image")](/uploads/2017/02/image61.png)[![image](/uploads/2017/02/image_thumb62.png "image")](/uploads/2017/02/image62.png)
By the way, you can go into each group after and look at License status, and Reprocess if needed.
[![image](/uploads/2017/02/image_thumb63.png "image")](/uploads/2017/02/image63.png)
At the Group’s Audit Log we can track the license activity as well:
[![image](/uploads/2017/02/image_thumb64.png "image")](/uploads/2017/02/image64.png)
So there we have it, a long sought after functionality that I’m sure many organizations will have good use for. As this is in Preview, some more testing are should be done before setting it directly into production, and if I find anything special I will update this blog post.
I am sure there will be an announcement and blog post at the Enterprise Mobility + Security blog shortly also: [https://blogs.technet.microsoft.com/enterprisemobility/](https://blogs.technet.microsoft.com/enterprisemobility/ "https://blogs.technet.microsoft.com/enterprisemobility/")
