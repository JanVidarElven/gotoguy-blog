---
title: "How to configure Conditional Access for Azure AD PIM"
date: 2018-05-04T12:11:10Z
draft: false
slug: "how-to-configure-conditional-access-for-azure-ad-pim"
tags:
  - "Azure AD PIM"
  - "Azure MFA"
  - "Intune"
categories:
  - "Azure AD"
  - "Azure AD Conditional Access"
  - "Azure AD Privileged Identity Management"
---

Azure AD Privileged Identity Management is a really great security feature for controlling those Azure AD and Azure Subscription administrator roles. By implementing Azure AD PIM you can let users with admin roles elevate themselves when they need to, using just in time (JIT) and eligible roles instead of permanent admin roles. You can even implement approval workflows and audit trails, so if you haven't looked into it you should really take a look!
With Azure AD PIM you can require Azure MFA when activating admin roles, but outside that you cannot set conditions and access control scenarios like you can do with Azure AD Conditional Access.
But now recently there is a new option in public preview for assignments to users and groups for Conditional Access policies, you can assign the CA policy to directory roles!
[![image](/uploads/2018/05/image_thumb.png "image")](/uploads/2018/05/image.png)
So I was wondering how this would work together with Azure AD Privileged Identity Management, for example in the following scenario:
I have an Exchange Administrator that from time to time performs Exchange Online admin tasks, and have configured this admin user with Azure AD PIM and eligible for Exchange Administrator Role among others:
[![image](/uploads/2018/05/image_thumb1.png "image")](/uploads/2018/05/image1.png)
Lets say that I only want this user to perfom Exchange Administrator tasks from a Compliant Device. Even though the Azure AD PIM role is protected by MFA at activation, making the user secure and trusted, I really want the device he is using to be secure and compliant with any management profiles I have defined using Intune MDM. Especially when he is doing admin stuff in our Exchange Online tenant or even running some Exchange Online PowerShell commands.
Lets set up this scenario.

## Creating Azure AD Conditional Access Policy for Directory Role

The first thing I set up is the CA policy for my specific Directory Role in this scenario. I specify a name and then select the Directory role of Exchange administrator as shown below:
[![image](/uploads/2018/05/image_thumb2.png "image")](/uploads/2018/05/image2.png)
Next for Cloud apps I select Exchange Online:
[![image](/uploads/2018/05/image_thumb3.png "image")](/uploads/2018/05/image3.png)
For Access controls I select to require the device to marked as compliant:
[![image](/uploads/2018/05/image_thumb4.png "image")](/uploads/2018/05/image4.png)
After that I enable the policy and save. We are now ready to test the user experience.

## Testing Azure AD PIM Role Activation and Conditional Access

So now we can test the scenario. Remember that the idea is that the CA policy only will kick in when the user has activated his Azure AD PIM role assignment as Exchange Administrator.
PS! If this user also has a Exchange Online license and mailbox, the same CA policy will apply and require the device to be compliant as long as the Exchange Administrator role is active. That could pose some not intended side effects, requiring the devices that access Exchange Online for normal mailbox access to be compliant as well, but as long as the Exchange Online Admin isn’t available as a Cloud app in Conditional Access we have to do it this way.
With my admin user, I first go to <http://aka.ms/myroles>, which will redirect me to my roles defined in Azure AD PIM. Lets sign in first:
[![image](/uploads/2018/05/image_thumb5.png "image")](/uploads/2018/05/image5.png)
And here is my eligible roles:
[![image](/uploads/2018/05/image_thumb6.png "image")](/uploads/2018/05/image6.png)
I select the action link to activate my Exchange Administrator role, and then to verify my identity with Azure MFA:
[![image](/uploads/2018/05/image_thumb7.png "image")](/uploads/2018/05/image7.png)
After verifying I can specify a reason or adjust the activation duration:
[![image](/uploads/2018/05/image_thumb8.png "image")](/uploads/2018/05/image8.png)
After that I’m activated and has an access valid for the set period of time:
[![image](/uploads/2018/05/image_thumb9.png "image")](/uploads/2018/05/image9.png)
Now, let’s go to to the Exchange Online Admin portal: <https://outlook.office365.com/ecp>. After signing in, if I’m not already signed in, I will get this message:
[![image](/uploads/2018/05/image_thumb10.png "image")](/uploads/2018/05/image10.png)
The details will tell me that the access rules require a compliant device:
[![image](/uploads/2018/05/image_thumb11.png "image")](/uploads/2018/05/image11.png)
We could also check using Exchange Online PowerShell module, and I get the same message:
[![image](/uploads/2018/05/image_thumb12.png "image")](/uploads/2018/05/image12.png)
Note that this message only works with the Connect-EXOPSSession that use Modern Authentication. The “old” way of using remote PowerShell and credential object to Exchange Online use basic (legacy) authentication so we cannot control that information flow, but the admin user will be denied there as well:
![ExoPS](/uploads/2018/05/exops.png)
To conclude this blog post, I have shown that by combining the new preview feature of Directory Roles assningments for Azure AD Conditional Access, and Azure AD Privileged Identity Management, we can implement more complex scenarios for conditions and access rules for using those directory roles. In my example I used compliant device, but you could also use any other of the conditions and access controls available.
