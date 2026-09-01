---
title: "How to enable Conditional Access for Azure RemoteApp Programs"
date: 2016-02-06T15:44:11Z
draft: false
slug: "how-to-enable-conditional-access-for-azure-remoteapp-programs"
tags:
  - "Azure"
  - "Azure AD Premium"
  - "Enterprise Mobility"
categories:
  - "Azure AD"
  - "Azure RemoteApp"
  - "Enterprise Mobility Suite"
---

Last week I published a blog article on how to publish the System Center Service Manager and Operations Manager Consoles as Azure RemoteApp Programs. (See <http://systemcenterpoint.wordpress.com/2016/02/02/publish-operations-and-service-manager-consoles-as-azure-remoteapp-programs/>)
One great feature if you are using Azure AD Premium is that you can enable Conditional Access for your Azure RemoteApp Programs. Conditional Access will enable your organization to require Multi-Factor Authentication or required that the programs only can be accessed when at work. In this blog post I will show how this can be configured.

## Requirements for Conditional Access for Azure RemoteApp Programs

The following requirements must be met to enable Conditional Access for Azure RemoteApp Programs:

- Conditional Access are an Azure AD Premium feature, so your organization must be licensed for that
- You must have created at least one Azure RemoteApp Collection
- At least one user/group must be assigned to a Program in the Azure RemoteApp Collection

If all these requirements are met, you will see this "Microsoft Azure RemoteApp" Application in your Azure AD:
![](/uploads/2016/02/020616_1540_howtoenable1.png)

## Configuring Conditional Access for Microsoft Azure RemoteApp

Select the Microsoft Azure RemoteApp Application and go to the Configure tab:
![](/uploads/2016/02/020616_1540_howtoenable2.png)
When enabling Access Rules, you can select to enable it for All Users, or for selected Groups. Both options can have exceptions for groups that you don't want to have Access Rules:
![](/uploads/2016/02/020616_1540_howtoenable3.png)
For the Rules you have 3 options for Conditional Access:
![](/uploads/2016/02/020616_1540_howtoenable4.png)
You can require Multi-Factor Authentication for the groups/users you selected above, every time they launch a RemoteApp Program Session. I
Another scenario, if you define your work network locations, you can require MFA when not at work, or block the application completely.
To configure trusted IPs, click on the link to get to the MFA Service Settings:
![](/uploads/2016/02/020616_1540_howtoenable5.png)

## User Experience for Azure RemoteApp Conditional Access

So, how does this look for the user when accessing Azure RemoteApp Programs?

### Require Multi-Factor Authentication

I launch my selected Azure RemoteApp Client, and clicking on a RemoteApp Program:
![](/uploads/2016/02/020616_1540_howtoenable6.png)
When launching the program, I'm prompted for MFA as expected:
![](/uploads/2016/02/020616_1540_howtoenable7.png)
If I sign in with the Azure RemoteApp HTML5 Preview client, <https://www.remoteapp.windowsazure.com/web>, the Multi-Factor Authentication will be performed before you see your Work Resources.

### Block access when not at work

If I selected the Access Rule for Blocking Access when not at work, I will get this message if I'm not on a trusted network:
![](/uploads/2016/02/020616_1540_howtoenable8.png)

## Conclusion

Meeting the requirements, we can verify that Conditional Access can be enabled for selected groups of users, and it will apply to all the Azure RemoteApp Programs you have published. Note that you cannot enable this specifically for selected Azure RemoteApp Programs, it will be for all the RemoteApp Programs or none.
