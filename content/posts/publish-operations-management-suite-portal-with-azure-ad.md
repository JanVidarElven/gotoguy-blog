---
title: "Publish Operations Management Suite Portal with Azure AD"
date: 2016-01-21T07:26:03Z
draft: false
slug: "publish-operations-management-suite-portal-with-azure-ad"
tags:
  - "Azure AD Premium"
  - "Enterprise Mobility"
  - "Operations Management Suite"
categories:
  - "Azure"
  - "Azure AD"
  - "Enterprise Mobility Suite"
  - "Operations Managment Suite"
---

To be able to access the Operations Management Suite Portal for your OMS workspace, you will need to have an account with either administrator or user access to the workspace.
This could be a Microsoft Account, or if you have added an Azure Active Directory Organization to your OMS workspace, you can add Azure users or groups to your workspace.
![add organization](https://i-technet.sec.s-msft.com/dynimg/IC826709.jpeg "add organization")
When users from your Azure AD has been granted either administrator or user access to the OMS workspace, you can notify them that they can log on to the portal.
But, where should they go to log in? The simplest way could be to tell them to go to <http://www.microsoft.com/oms>, and hit the Sign In link at the top. After signing in they will be instructed to choose the OMS workspace and then be directed to the OMS portal.
Another method is to tell them the workspace url for the portal directly. This would be something like: <https://<workspaceid>.portal.mms.microsoft.com/#Workspace/overview/index>
You will find the Workspace ID under Settings, and sometimes you can also use the Workspace Name in the above URL as well.
[![image](/uploads/2016/01/image_thumb.png "image")](/uploads/2016/01/image.png)
So you can communicate to users in your organization one of the methods above on how to access the portal. Chances are that most users will forget this info after a short while. They will either search after your e-mail, or ask you again at some time.
In this blog post I will show how you can publish the Operations Management Suite Portal as an Azure AD Application, utilizing Single Sign-On, so that users can access it easily with My Apps or the App Launcher in Office 365!

## Step 1 – Add Organizational User or Group Accounts to OMS Workspace

First you will need to add the Azure AD User or Group Account to your OMS Workspace. Select account type Organizational Account, and if they should be users or administrators. In the Choose User/Group type in and search for the users or groups you want to add:
[![image](/uploads/2016/01/image_thumb1.png "image")](/uploads/2016/01/image1.png)

## Step 2 – Creating the Azure AD Application

Next, log on as an Azure AD Global Administrator to the classic Azure management portal (manage.windowsazure.com). Under Active Directory, select your Azure AD, and then select Applications. Select Add to start adding a new Application. Select to Add an application my organization is developing:
[![image](/uploads/2016/01/image_thumb2.png "image")](/uploads/2016/01/image2.png)
Next, specify a name for the application, and type of web application:
[![image](/uploads/2016/01/image_thumb3.png "image")](/uploads/2016/01/image3.png)
Specify URL for SIGN-ON and APP ID UR. This will be the OMS Portal url. using either workspace name or ID which you have discovered before:
[![image](/uploads/2016/01/image_thumb4.png "image")](/uploads/2016/01/image4.png)
Finishing that and the Application has been added to Azure AD:
[![image](/uploads/2016/01/image_thumb5.png "image")](/uploads/2016/01/image5.png)

## Step 3 – Adding Users and Groups to the Application

Next I need to add which Users or Groups that will see the published application. At the Users and Groups page for my application, I’m notified that user assignment are not currently required to access Operations Management Suite Portal. That is correct, because users can access the portal directly if they know the URL or sign in at the Microsoft OMS site.
Adding Users or Groups here will enable the application to be visible for the users at the My Apps / App Launcher:
[![image](/uploads/2016/01/image_thumb6.png "image")](/uploads/2016/01/image6.png)
I search for and select to Assign the Groups (or Users) I want to have the application visible for.

## Step 4 – Logo and optional configuration

After adding users, the application is ready to test, but first I would want to add my own logo.
[![image](/uploads/2016/01/image_thumb7.png "image")](/uploads/2016/01/image7.png)
In this example I’m using a transparent png image with dimensions 215x215, and a central image dimension of 94x94.
[![image](/uploads/2016/01/image_thumb8.png "image")](/uploads/2016/01/image8.png)
[![image](/uploads/2016/01/image_thumb9.png "image")](/uploads/2016/01/image9.png)
At the Configure page, other settings can be set such as requiring user assignment, access rules with Multi-Factor Authentication and Self-Service access for users that has not been specifically assigned access.
I this scenario I only wanted to get the application published to users, so I will not configure any more settings. We are ready to test.

## Part 5 – User Access to the Published Application

Users can now access My Apps at <https://myapps.microsoft.com>. When logging in with the Azure AD User a list of published applications will be visible, and I can see the OMS Portal Application:
[![image](/uploads/2016/01/image_thumb10.png "image")](/uploads/2016/01/image10.png)
And, logged in to Office 365, I can select the App Launcher and show all my apps at <https://portal.office.com/myapps>.
[![image](/uploads/2016/01/image_thumb11.png "image")](/uploads/2016/01/image11.png)
I can pin the application to the App Launcher if I want for quicker access.
[![image](/uploads/2016/01/image_thumb12.png "image")](/uploads/2016/01/image12.png)
So to conclude this blog post, users now have a quickly accessible shortcut to the Operations Management Suite Portal using single sign-on with Azure AD.
