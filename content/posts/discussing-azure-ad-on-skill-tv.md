---
title: "Discussing Azure AD on Skill TV"
date: 2015-06-26T07:45:36Z
draft: false
slug: "discussing-azure-ad-on-skill-tv"
tags:
  - "Azure"
  - "Azure AD Premium"
  - "Enterprise Mobility"
---

Recently I did an interview on our video blog at Skill TV, talking about Azure AD with our HR Manager Elham Binai.
![](/uploads/2015/06/062615_0741_azureadonsk1.png)

The interview is in Norwegian and can be seen here: <https://www.youtube.com/watch?v=pkRHW-ZJC2w>
I have below provided a translated version from our interview transcript. While some questions and answers flowed a little bit different in the real recording, the transcript quite covers it all. Apologize for a couple of cuts as well, we had some problems with noise from spotlight fans and had to pause recording when that happened.
Here it goes:

### Elham: Today I am lucky to have Jan Vidar Elven with me here at Skill TV. He is an Architect in our Infrastructure Department and an expert on the Azure Active Directory, which is the topic of today. Welcome you are, Jan Vidar.

*Jan Vidar: Thanks for that, Elham. Very glad to come and talk about something I am very engaged in and work a lot with!*

### Elham: Jan Vidar, in recent years we have moved us more and more to the Cloud. More companies are using these Cloud solutions. However, it has not been without challenges, many companies are concerned that their business secrets should leak out, afraid of hackers, unfortunate leaks etc. ... simply the security around the cloud. What are your thoughts about this?

*Jan Vidar: Well, when you move the solutions out in the cloud, so also follows users identities and access control with these. It is then important to have confidence that the authentication and authorization take place in a secure manner, so that one can be assured that no one but those who should HAVE access GET access to their solutions. It is this and more Azure Active Directory delivers. Azure AD is a platform for identity management and access control solutions in the cloud, AND for the local data center.*

### Elham: What are the challenges around users now? Moreover, what does it require when it comes to security around systems that companies use? We live in a world where users use many devices and they take these with them everywhere ... This offers some challenges. How can you resolve it with Azure AD?

*Jan Vidar: The challenge of users now is two-part. One is that they increasingly use the PC's and mobile devices delivered to them by their workplace at home or on the go. The second is that they are using their personal mobile phones, tablets and laptops to log on to the company's solutions. Very often, these are also to the disposal of the other members in the family. When the solutions are located in the cloud, it can be a concern that only the use of your user name and password is not enough, especially when some Apps store the credentials as well.*
*A solution to this in Azure AD is to make use of Multi-factor authentication. Multi-factor authentication is free for Office 365 users and Azure AD administrators. With the MFA do you get an SMS, a phone call or a notification in a separate App where you have to authenticate authentication before you can access. We can also choose to use MFA only when the user is outside the company's network. In the Premium version of Azure AD, MFA is included in hybrid scenarios so that you can protect your own solutions in the on premise data center as well.*
*Another way to solve the challenges is to require that devices be registered before you get access to log on to the solutions in the cloud. You can also require that the devices should be in compliance with company policy, for example require that they have a password on the lock screen. Requirements for registration of mobile devices can be set up in the Office 365, which is powered by the MDM platform in Microsoft Intune, or you can use of the entire platform to configure Intune MDM and MAM, Mobile Device Management and Mobile Application Management, for device management, application management and policies for the company's Devices and Apps. All this is linked to the user's identity in the Azure AD.*

### Elham: Many IT managers believe that things were easier in the past, where they were very close to their solutions and data and now might feel that they have lost control ... What is your experience around that?

*Jan Vidar: Not only are the users and devices spread, but the data exchanged in the solutions both internally between each other and externally with others is also important to have control on. When it was easier in the past, it probably meant that you had the solutions in the local data center, you had them integrated with Active Directory, and had one simple and transparent Single Sign-On, a user name and a password to all or at least most services at the same time that we had control of the data locally. When we now apply the solutions in the cloud, we must have a solution that facilitates the same, and at the same time to have control of the data. Azure AD together with Azure Rights Management Services can associate the identity and protection at the file level. However, this only applies to the solutions in the cloud and the Apps that IT has control over and know about.*

### Elham: The IT department don't have much control over all the cloud apps and outside the local firewall and it concerns many, what is your advice around this? Users are going to use it anyway, what should our customers think about?

*Jan Vidar: What we are talking about here is what is we call shadow IT; users find their own solutions where there is lack of personalized services from the company. Email, file sharing, social media, productivity applications are areas for SaaS applications used by users in business context. This is concerns applications, user names, passwords, and data that IT has no control over. What can IT do? Azure AD has the ability to facilitate applications from a catalog of over 2400 SaaS applications, you can also add your own self-developed applications and as well publish internal applications from the local data center. That way one can arrange for authentication via Azure AD, Single Sign-On for those applications that support it, or Same Sign-On with password storage for other applications. In this way IT can take control of your applications and facilitate the access of its users. IT can also run discovery, and reports to find out what the users actually use on the devices they has to identify if there are applications it is important to provide and facilitate.*

### Elham: We know Active Directory, but now it can also be located in Azure if you wish it? It can then be managed in both cloud and on premise, explain this a bit more.

*Jan Vidar: By integrating local Active Directory with Azure AD through synchronization, companies can manage users and groups in one place at the same time as you can give access to solutions in the cloud. With hybrid identities and Single Sign-On, users can relate to the same user name and password for either using solutions in the cloud or in the local data center, at the same time that IT has control of the authentication, both who, what, where and when.*

### Elham: IT can actually go in and see how, when and where users have logged in from - and have more control over the activities?

*Jan Vidar: Yes, Azure AD Premium will provide opportunities to monitor and run reports on authentications and application usage, as well as view suspicious pattern in sign-on, credentials that may have been lost, or devices that may be infected, for example.*

### Elham: Does this work on any device? Single Sign-On? You have only one password and can log in once?

*Jan Vidar: Yes, both iOS, Android and Mac are supported in addition to Windows and Windows Phone. Office applications, SSO, Device Management and Rights Management is supported on these, and all linked together with your identity in Azure AD. With the upcoming Windows 10, these devices can also be joined directly into Azure AD, and you can log on with your Azure AD identity. One can also use a pin code associated with the device for even easier authentication, or use biometric authentication with Windows Hello!*

### Elham: How will this take away the uncertainty around the Cloud, security, and control over users?

*Jan Vidar: It all starts with control of identities, and Azure AD will facilitate this for the solutions running in the cloud, and not necessarily just for Microsoft solutions but also for SaaS solutions that support SSO and Federation with Azure AD. With control of the devices and rights management for the files as well, as well as security mechanisms for authentication and conditional access, you have the tools you need to get started. Azure AD can also provide for Self Service IT, where users can reset their passwords, or access to an application if they want it.*

### Elham: Azure AD has really simplified my life without me noticing it, I can log in from anywhere and on any device. If customers would like to know more about this then you can come visit and tell about how Azure AD can simplify a lot for IT departments as well as security. Thank you so much for that I got to talk to you today.

*Jan Vidar: Thank you for inviting me!*
