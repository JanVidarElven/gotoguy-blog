---
title: "Protecting Norwegian National ID Number with Azure Information Protection and RMS"
date: 2016-11-25T13:48:23Z
draft: false
slug: "protecting-norwegian-national-id-number-with-azure-information-protection-and-rms"
tags:
  - "Azure AD"
  - "Cybersecurity"
categories:
  - "Azure Information Protection"
  - "Azure RMS"
  - "Enterprise Mobility + Security"
  - "Enterprise Mobility Suite"
---

In Norway we have a National Identification Number which is an 11-digit personal identifier, which also is referred to a Birth Number as this is given to every Norwegian borned at birth.
The number consists of:

- 6 first digits are birth date in the form of: ddmmyy
- 3 next digits are personal, with the last of those 3 indicating whether you are male (odd number) or female (even number)
- The last 2 digits are control digits, based on modulus functions on the first digits

(Source: [http://www.skatteetaten.no/en/person/National-Registry/Birth-and-name-selection/Children-born-in-Norway/National-ID-number/](http://www.skatteetaten.no/en/person/National-Registry/Birth-and-name-selection/Children-born-in-Norway/National-ID-number/ "http://www.skatteetaten.no/en/person/National-Registry/Birth-and-name-selection/Children-born-in-Norway/National-ID-number/"))
The special thing about Norwegian National ID Numbers are that they are not only used for personal identification, but also in some official scenarios is used for source of authentication. This makes this ID number highly sensitive, and should not be shared around in for example documents and emails.
In this blog post I will look at how Azure Information Protection can automatically detect and classifiy documents that contains the Norwegian National ID Number, and more over how we can use Azure Rights Management Services (RMS) to automatically apply a RMS template which encrypts and sets permissions for these classified documents.
I will show this step by step, so read on for details.

## Activate Azure Rights Management Services and Azure Information Protection for your Azure AD

The requirement for setting this up is that you have a Tenant with an Azure AD Directory, and licensed with EMS Suite (E3 or E5), Secure Productive Enterprise (SCE) or Azure Information Protection P1 or P2 licenses. You will need the EMS E5/AIP P2 if you want to be able to automatically classify and label documents, as E3/P1 only enables users for manual classification and labeling. You can get EMS E5 trial licenses if needed.
To active Azure RMS, if you havent already done this, go to: <https://account.activedirectory.windowsazure.com/RmsOnline/Manage.aspx>
If you get this message you are OK to proceed to next step:
[![image](/uploads/2016/11/image_thumb1.png "image")](/uploads/2016/11/image1.png)
Next, in a new browser window, sign in to the [Azure portal](https://portal.azure.com/) as a global admin for your tenant.
On the hub menu, click New, and then select Security + Identity. In the Security + Identify blade, select Azure Information Protection. In the Azure Information Protection blade, click Create. This will enable Azure Information Protection and make it accessible for your configured services later. If you selected to pin the blade, you will have easy access for configuring Azure Information Protection later:
[![image](/uploads/2016/11/image_thumb2.png "image")](/uploads/2016/11/image2.png)

## Configure Classification and Labeling

In this step we will configure the classification and labeling for the Norwegian National ID Number.
First, when I start the default configuration of Azure Information Protection, I will se these built-in classification labels:
[![image](/uploads/2016/11/image_thumb3.png "image")](/uploads/2016/11/image3.png)
These classification labels should be sufficient for a lot of protection scenarios, but in this case I will add a new label for protecting restricted content like the Norwegian National ID Number. I select to add a new label, as shown below:
[![image](/uploads/2016/11/image_thumb4.png "image")](/uploads/2016/11/image4.png)
I give the new label the name Restricted, and provide a custom tooltip for the users to see. I can select another color if I want, and for now I don’t want to add an Azure RMS template for protection.
Further down, I add visual markings, by providing a Header text:
[![image](/uploads/2016/11/image_thumb5.png "image")](/uploads/2016/11/image5.png)
And a watermark:
[![image](/uploads/2016/11/image_thumb6.png "image")](/uploads/2016/11/image6.png)
Next I can specify conditions for automatically applying a label. This is where I will check for any Norwegian National ID Numbers. First I add the Condition:
[![image](/uploads/2016/11/image_thumb7.png "image")](/uploads/2016/11/image7.png)
Then I select Custom type of condition, because the built-in ones does not contain the Norwegian ID number. Under Custom I specify a name for the condition, and select to match based on a regular expression. See explanation below. I can also match on case sensitivity (if letters) and number of occurances if I want.
[![image](/uploads/2016/11/image_thumb8.png "image")](/uploads/2016/11/image8.png)
So, the main part here is the Regular Expression (RegEx) that will discover if there could be a possible match on a Birth Number/Norwegian National ID Number.
I will not dive into details on Regular Expressions here on my blog, but in short the following expression will match if the first 6 digits are a valid date. For example 31 days in the months Jan, Mar, May, July; Aug, Oct and Dec, and 30 days in the rest. In addition, this will not check for leap years, so will accept 29 days for each Feb to simplify. The last 5 digits are accepted if they are 0-9.
**(0[1-9]|[1-2][0-9]|31(?!(?:0[2469]|11))|30(?!02))(0[1-9]|1[0-2])\d{7}**
This expression could be even better, and I might look into that later:

- If the 3 digits after the date were checked to be in the right group based on birth year
- If the last 2 digits were in fact modulus calculating on the previous

But for now this should be sufficient.
After adding that condition, I specify a tooltip for the end users:
[![image](/uploads/2016/11/image_thumb9.png "image")](/uploads/2016/11/image9.png)
All that is left now is to save and publish my new classification label:
[![image](/uploads/2016/11/image_thumb10.png "image")](/uploads/2016/11/image10.png)

## Download and Install the Azure Information Protection Client

Next step is to Install the Azure Information Protection client on a PC that has Office installed. Download the client from from the Microsoft download center, <https://www.microsoft.com/en-us/download/details.aspx?id=53018>.
Run AzInfoProtection.exe and follow the prompts to install the client. As we have configured the tenant with the default and customized label, it doesnt matter if you install the demo labels as the tenant settings will override.
After installing the client and starting any Office program we will se the toolbar as shown below:
[![image](/uploads/2016/11/image_thumb11.png "image")](/uploads/2016/11/image11.png)

## Testing Automatic Classification of National ID Number

If I open a new document in Word and type in as below for an example valid National ID Number:
[![image](/uploads/2016/11/image_thumb12.png "image")](/uploads/2016/11/image12.png)
I then have to save the document, because the validation of conditions for classification labels happens at save time.
And as expected, the document has now been automatically classified as Restricted, with the explanation that a Norwegian National ID Number has been detected:
[![image](/uploads/2016/11/image_thumb13.png "image")](/uploads/2016/11/image13.png)
I also see the watermark and the header text for the document:
[![image](/uploads/2016/11/image_thumb14.png "image")](/uploads/2016/11/image14.png)
At this point we are able to automatically classify the document as restricted and sensitive, but the document can still be shared unencrypted if the user wants to do that.
In the next step we will see how we can configure automatic data protection for this classification label.

## Configure Data Protection

If we want to configure automatic data protection for classified documents I will need to either use an existing or create a new Azure RMS Template. In this case I will create a new template. This must, for now, be done in the old Azure Portal at manage.windowsazure.com, and under your Azure Active Directory and Rights Management settings.
[![image](/uploads/2016/11/image_thumb15.png "image")](/uploads/2016/11/image15.png)
When you enable Azure Rights Management for your tenant you will have two default RMS templates specified:

- <organization name> - Confidential
- <organization name> - Confidential View Only

I will now create a new RMS template for my organization, which I will use for protecting documents that are classified as Restricted. First I specify language, name and description for the new template:
[![image](/uploads/2016/11/image_thumb16.png "image")](/uploads/2016/11/image16.png)
After creating the RMS template I can now configure rights, scope and optional configurations.
[![image](/uploads/2016/11/image_thumb17.png "image")](/uploads/2016/11/image17.png)
Under Rights I have added a couple of groups from my Organization where I configure a Rights role of Viewer:
[![image](/uploads/2016/11/image_thumb18.png "image")](/uploads/2016/11/image18.png)
The Viewer Role has the following custom rights, which suits my scenario where I want to restrict sharing for Restricted Sensitive Information.
[![image](/uploads/2016/11/image_thumb19.png "image")](/uploads/2016/11/image19.png)
I can define the scope of the RMS template, which defines who in my organization can apply this template. I want everybody to be able to use this template, so I will not change any scoping settings now:
[![image](/uploads/2016/11/image_thumb20.png "image")](/uploads/2016/11/image20.png)
At the configuration section I can choose to Publish the template, and change settings for additional languages, content expiration and offline access. I have left the default settings on and publish the RMS template as ready to use:
[![image](/uploads/2016/11/image_thumb21.png "image")](/uploads/2016/11/image21.png)
With the new RMS template ready, I can now go back to Azure Information Protection and Configure the Protection settings for my “Restricted” classification label. I select my new RMS template from the dropdown menu:
[![image](/uploads/2016/11/image_thumb22.png "image")](/uploads/2016/11/image22.png)
After that I hit Save, and then Publish the policy:
[![image](/uploads/2016/11/image_thumb23.png "image")](/uploads/2016/11/image23.png)
I can now see that my Restricted classification label both have Marking, Protection and Conditions defined:
[![image](/uploads/2016/11/image_thumb24.png "image")](/uploads/2016/11/image24.png)

## Testing Automatic Protection

We will now test this in a new Word document. Once again I type a National ID Number and Save the document. And now I see that the document both is automatically classified and protected:
[![image](/uploads/2016/11/image_thumb25.png "image")](/uploads/2016/11/image25.png)
As I am the owner of the document, I can share it internally to any user in my organization, but they will be prohibited to do any operations besides viewing the document.
And if I share the document to an external user outside my organization, they will be prohibited to view the document and contents as well, as they are not able to open and view the document without an Azure AD user from my organization:
[![image](/uploads/2016/11/image_thumb26.png "image")](/uploads/2016/11/image26.png)
If I wanted to restrict my users from even sharing it internally, I would need to configure an Office 365 Data Loss Prevention (DLP) Policy, which can apply to Exchange Online, SharePoint Online and/or OneDrive for Business, and look for Norwegian National ID Number there. But that would be a topic for another blog post!

## Classifying and Protecting Outlook E-mail

Does this only apply to Office documents? No, when you install the Azure Information Protection client you get the opportunity to classify and protect e-mails sent with the Outlook client as well.
When I send an e-mail message that contains a Norwegian National ID Number and after I hit the Send button, the automatic classification and protection will be applied to the e-mail:
[![image](/uploads/2016/11/image_thumb27.png "image")](/uploads/2016/11/image27.png)
The external receipient of the e-mail will se this message, and will not be able to see the e-mail content:
[![image](/uploads/2016/11/image_thumb28.png "image")](/uploads/2016/11/image28.png)

## Conclusion

In this blog post I have shown how you can use Azure Information Protection (AIP) to classify Office documents and Outlook e-mails and how you can use conditions to automatic apply that classification based on for example a Norwegian National ID Number detection with the use of a regular expression.
In addition I have shown how you can use Azure RMS and a template to automatically encrypt that document and set the permissions for the users in my organization that only allows viewing.
