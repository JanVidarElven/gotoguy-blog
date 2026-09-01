---
title: "Assign EMS License with Azure AD v2 PowerShell and Dynamic Groups"
date: 2017-02-17T09:39:12Z
draft: false
slug: "assign-ems-license-with-azure-ad-v2-powershell-and-dynamic-groups"
tags:
  - "Azure AD Premium"
  - "EMS"
  - "Enterprise Mobility"
categories:
  - "Enterprise Mobility + Security"
  - "PowerShell"
---

While we are waiting for support for group based licensing in the Azure AD Portal I have created this Azure AD v2 PowerShell solution for assigning EMS (Enterprise Mobility + Security) license plans using Azure AD v2 PowerShell module and Dynamic Groups.
The PowerShell CmdLets used here requires the Azure AD v2 PowerShell Module, which you can read about how to install or update here: [https://gist.github.com/skillriver/35fba9647fbfbe3e99718f0ad734b241](https://gist.github.com/skillriver/35fba9647fbfbe3e99718f0ad734b241 "https://gist.github.com/skillriver/35fba9647fbfbe3e99718f0ad734b241")

## Source of Authority, Attributes, Sync and Dynamic Groups

In my scenario I want to use extension attributes to automatically calculate membership using Dynamic Groups in Azure AD. The members of these groups will be assigned the EMS licenses.
Most organizations will have an on-premises Active Directory synchronizing to Azure AD, so the source of authority is important for where I set the value of the extension attributes, as I want my Dynamic Groups to calculate membership for both On-premise and Cloud based users (I have some Cloud based admin account I want to license as well).
So, lets take a look at my local Active Directory environment. If you have Exchange installed in your organization, you will have extended the schema with extensionAttribute1..15.
But in my case, I never have installed any versions of Exchange in my current environment, and only used Exhange Online, so I don’t have those attributes. Instead I have msDS-cloudExtensionAttribute1..20.
So I decided on using the following attributes locally in AD:
[![image](/uploads/2017/02/image_thumb.png "image")](/uploads/2017/02/image.png)
I have previously used ENTERPRISEPACK (SkuPartNumber for Office 365 E3) for licensing Office 365 E3 plans. In this scenario I will use the msDS-cloudExtensionAttribute2 for either EMS (SkuPartNumber for EMS E3) or EMSPREMIUM (SkuPartNumber for EMS E5).
You can also use Active Directory PowerShell to set these values on-premises:
[![image](/uploads/2017/02/image_thumb1.png "image")](/uploads/2017/02/image1.png)
Note that if I had Exchange installed, I could just have used extensionAttribute1 and extensionAttribute2, and these would be automatically synchronized to Azure AD in an Exchange Hybrid deployment. However, in my case I need to manually specify the option for Directory extension attribute sync in Azure AD Connect:
[![image](/uploads/2017/02/image_thumb2.png "image")](/uploads/2017/02/image2.png)
And then selecting to synchronize those two selected attributes:
[![image](/uploads/2017/02/image_thumb3.png "image")](/uploads/2017/02/image3.png)
After these Directory extensions are configured and synchronized to Azure AD, I can check these attributes with the following AAD v2 command:
```powershell
Get-AzureADUser –ObjectId <youruser> | Select -ExpandProperty ExtensionProperty
```
In my environment I will find these attributes:
[![image](/uploads/2017/02/image_thumb4.png "image")](/uploads/2017/02/image4.png)
Note that the msDS\_cloudExtensionAttribute1..2 has now been created in Azure AD for me, and been prefixed with extension\_<GUID>\_, where the GUID represent the Tenant Schema Extension App:
[![image](/uploads/2017/02/image_thumb5.png "image")](/uploads/2017/02/image5.png)
So now I know that my on-premises users with values for msDS\_cloudExtensionAttribute1..2 will be synchronized to the extension attributes in Azure AD. But what about users that are source from Cloud? There are no graphical way to set these extension attributes, so we will have to do that with Azure AD v2 PowerShell. In my example I have a Cloud admin account I want to set this attribute extension for (scripts are linked later in the blog):
[![image](/uploads/2017/02/image_thumb6.png "image")](/uploads/2017/02/image6.png)
With that, I now have configured the users I want with the extension attribute values, and are ready to create the Dynamic Groups.

## Creating Dynamic Groups for Assigning EMS Licenses

Earlier in the blog post I mentioned that I wanted to use the msDS\_cloudExtensionAttribute2 for assigning either EMS E3 or EMS E5 licenses. If I run the following command, I get my Subscriptions, here listed by SkuId an SkuPartNumber. EMSPREMIUM refers to EMS E5, while EMS refers to the original EMS which is now E3.
[![image](/uploads/2017/02/image_thumb7.png "image")](/uploads/2017/02/image7.png)
On that basis I will create 2 Dynamic Groups, one that looks for EMSPREMIUM and one that looks for EMS in the extension attribute. You can create Dynamic Groups in the new Azure AD Portal, or by running these PowerShell commands:
[![image](/uploads/2017/02/image_thumb8.png "image")](/uploads/2017/02/image8.png)
After a while memberships in these dynamic groups will be processed, and I can check members with the following commands:
[![image](/uploads/2017/02/image_thumb9.png "image")](/uploads/2017/02/image9.png)
In my environment I will have this returned, showing users with membership in the EMS E3 and EMS E5 group respectively:
[![image](/uploads/2017/02/image_thumb10.png "image")](/uploads/2017/02/image10.png)
Before I proceed I will save these memberships to objects variables:
[![image](/uploads/2017/02/image_thumb11.png "image")](/uploads/2017/02/image11.png)

## Assigning the EMS licenses based on group membership

With users, attributes and dynamic groups membership prepared, I can run the actual PowerShell commands for assigning the licenses. I also want to make sure that any users previously assigned to another EMS license will be changed to reflect the new, so that they are not double licensed. Meaning, if a user already has an EMS E3 license, and the script adds EMS E5, I will remove the EMS E3 and vice versa.
The full script is linked below, but I will go through the main parts here first. First I will save the SkuId for the EMS subscriptions:
[![image](/uploads/2017/02/image_thumb12.png "image")](/uploads/2017/02/image12.png)
Then I will loop through the membership objects saved earlier:
[![image](/uploads/2017/02/image_thumb18.png "image")](/uploads/2017/02/image18.png)
Next, create License Object for adding and removing license:
[![image](/uploads/2017/02/image_thumb19.png "image")](/uploads/2017/02/image19.png)
Then create a AssignedLicenses object, adding the AssignedLicense object from above. In addition, I check if the user has an existing EMS license to be removed, and if so add that SkuId to RemoveLicenses. If there are no license to remove, I still need to specify an empty array for RemoveLicenses.
[![image](/uploads/2017/02/image_thumb20.png "image")](/uploads/2017/02/image20.png)
And then, update the user at the end of the loop:
[![image](/uploads/2017/02/image_thumb21.png "image")](/uploads/2017/02/image21.png)
After looping through the EMS E3 members, a similar loop through EMS E5 members:
[![image](/uploads/2017/02/image_thumb17.png "image")](/uploads/2017/02/image17.png)
So to summarize, with this script commands you can assign either EMS E3 or E5 licenses based on user membership in Dynamic Groups controlled by extension attributes. In a later blog post I will show how we can consistenly apply these licenses, stay tuned!
Link to the full script is below:
https://gist.github.com/skillriver/d239329c865b3ea225bf0f194b6889f0
Link to script for managing and listing extension attribute properties for your users:
https://gist.github.com/skillriver/534191d66de951b9c27a631a5a741caa
