---
title: "Blog Series - Power'ing up your Home Office Lights: Part 2 - Prepare Azure Key Vault for storing your API secrets"
date: 2020-12-03T15:05:17Z
draft: false
slug: "blog-series-powering-up-your-home-office-lights-part-2-prepare-azure-key-vault-for-storing-your-api-secrets"
tags:
  - "Azure"
  - "Key Vault"
categories:
  - "Philips Hue"
---

This blog post is part of the Blog Series: Power'ing up your Home Office Lights with Power Platform. See introduction post for links to the other articles in the series:  
[[https://gotoguy.blog/2020/12/02/blog-series---powering-up-your-home-office-lights-using-power-platform---introduction/](https://gotoguy.blog/2020/12/02/blog-series-powering-up-your-home-office-lights-using-power-platform-introduction)](https://gotoguy.blog/2020/12/02/blog-series---powering-up-your-home-office-lights-using-power-platform---introduction/)



Continuing on Part 1, where we created an App Registration for Hue Remote API, I will need a secure place to store the App credentials like Client ID and Secret. I will also need to store the Access Token and Refresh Token, so that I can retrieve it when I need to call the Hue Remote API, and use the Refresh Token to renew the Access Token when it expires.



To start with, here is a short video where I explain the concept:


https://youtu.be/FeixHqhaYvs



## Choosing Azure Key Vault as Secret Storage



Client ID and Secret from the App registration are credentials that needs to be protected from unauthorized access. Likewise, if unauthorized users get hold of your Access Token, they can access your Hue Bridge remotely and create user access for themselves to your Hue Lights.



If you are planning to build this solution only for yourself, and no other users will share your Hue Power Apps and Flows, then you can store the credentials and tokens in a personal storage, for example in a SharePoint Online List. Just make sure that this resource never will be shared with other users internally, or externally. This would also be a logical choice if you don't have access to an Azure subscription for yourself.



In my case, I wanted to be able to share the user part of the solution with other users, while making sure that my credentials and tokens were as protected as possible. So I decided to create some logic around that in Azure, and to store my secrets in Azure Key Vault.



## Setting up Azure Resources for Key Vault



You will need access to an Azure Subscription to do this part. Your organization might provide you with access to a subscription, or there are several pathways to starting with Azure for free, amongst others Visual Studio subscription, Azure for Free, Azure for Students to name a few.



At a minimum you will need Contributor access to a Resource Group, where you can deploy the following:



- Azure Key Vault resource for storing secrets for Power Platform and Hue Remote API.
- Adding the secrets necessary for the solution.
- Access policy that allows you, and later the Logic Apps access to get, set and list secrets from the Key Vault.



In your resource group, create a new Key Vault. The name needs to be globally unique, so it makes sense to use any naming convention:


[![](/uploads/2020/12/image-7.png?w=755)](/uploads/2020/12/image-7.png)



For the purpose of the Hue Remote API, you will need to create the following 3 secrets:


[![](/uploads/2020/12/image-8.png?w=1024)](/uploads/2020/12/image-8.png)



The "secret-hue-client-id" and "secret-hue-client-secret" are created manually with the client id and secret from the Hue App registration.



The "secret-hue-bearer-token" will be populated via the Logic App we will look into in a later part in this blog series. Note that this secret has an expiration date, which is when the token expires. I will get into that later as well.



## Managing Access to the Key Vault



You need to configure the Key Vault access policy so that you, and any services that interact with the Key Vault have the right access to get, set or list secrets.



In this case, I have configured my Hue Logic Apps with access via Managed Service Identity (MSI), at this point you might not have these in place yet, but we will get there also in a later part:


[![](/uploads/2020/12/kv-access-1.png?w=947)](/uploads/2020/12/kv-access-1.png)



With that we can conclude this part, in the next part of the blog series we will start looking into the Logic Apps for Hue authorization and managing access token.



Thanks for reading, see you in the next part :)
