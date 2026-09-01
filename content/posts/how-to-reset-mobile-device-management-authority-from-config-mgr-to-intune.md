---
title: "How to reset Mobile Device Management Authority from Config Mgr to Intune"
date: 2016-04-29T10:28:13Z
draft: false
slug: "how-to-reset-mobile-device-management-authority-from-config-mgr-to-intune"
tags:
  - "Microsoft Intune;Configuration Manager"
categories:
  - "Enterprise Mobility Suite"
  - "Microsoft Intune"
---

I have a demo/test environment for Intune enrollment where I have configured Configuration Manager as the Mobile Device Management Authority. I have been thinking about a change in approach, as most of my test devices are either lightly managed PC’s or mobile devices. So I wanted to change and use Microsoft Intune only as the MDM Authority.
Referring to the official documentation for setting Mobile Device Management Authority, [https://technet.microsoft.com/en-us/library/mt346013.aspx](https://technet.microsoft.com/en-us/library/mt346013.aspx "https://technet.microsoft.com/en-us/library/mt346013.aspx"), this can only be set initially when configuring the tenant, and cannot be changed later!
But, there is a way. You can create a Service Request ticket with Microsoft, and request a reset of the mobile device authority.
There are some caveats to this reset request though:

- You will have to retire and delete all registered mobile devices
- You will have to delete all MDM related configurations in Configuration Manager

Basically, this is a real start over with clean sheets. If that is what you want, read on, if not, stop here ![Winking smile](/uploads/2016/04/wlemoticon-winkingsmile.png).
In this blog article I will show the steps I went through to reset my MDM authority.

## Step 1 – Create a Service Request

The first step is to create the Service Request, requesting a reset. Identify the issue by selection feature Intune Service Administration, and symptom Reset mobile device authority. Provide a summary and issue details, like for example below:
[![image](/uploads/2016/04/image_thumb4.png "image")](/uploads/2016/04/image4.png)
Review and continue:
[![image](/uploads/2016/04/image_thumb5.png "image")](/uploads/2016/04/image5.png)
Add details if needed:
[![image](/uploads/2016/04/image_thumb6.png "image")](/uploads/2016/04/image6.png)
Confirm and submit:
[![image](/uploads/2016/04/image_thumb7.png "image")](/uploads/2016/04/image7.png)
Service Request is now pending, awaiting response:
[![image](/uploads/2016/04/image_thumb8.png "image")](/uploads/2016/04/image8.png)

## Step 2 – Await response on Service Request on next steps

After a couple of hours I got a response with a checklist to be completed:
[![image](/uploads/2016/04/image_thumb9.png "image")](/uploads/2016/04/image9.png)
Here’s the checklist:
·  Retire **all** Modern Devices (mobile devices) from within the **Configuration Manager Console.** **It is important that you do not attempt to retire a device from the device itself for this procedure to be executed.** *Let us Know if any devices are in a "pending state'*
·  Point the Intune Subscription to an empty user collection, or, remove all users from the targeted collection.  and confirm in the CloudUserSync.log that all users are removed.
· **Remove all users** from the **Intune User Group**.
·  Run the following SQL Procedure on the CM server to ensure all licenses are removed from the DB:
**Insert into MDMCloudUserNotification Select ItemKey, 3, 0 from User\_Disc where CloudUserId is not null**
·  Then restart the CloudUserSync thread in ConfigMgr (or restart SMS\_Executive if easier) and then when CloudUserSync starts up, it should deprov the users.
Restart SMS Executive
To reset the SMS\_COLLECTION\_EVALUATOR thread through registry, Open Registry console, navigate till below mentioned registry
–> Right click Requested Operation –> Modify –> type ”Stop” and click on ok.
Do refresh till data value reset to “None” and then again edit it with “start” data value
HKEY\_LOCAL\_MACHINE\SOFTWARE\Wow6432Node\Microsoft\SMS\Components\SMS\_EXECUTIVE\Threads\SMS\_COLLECTION\_EVALUATOR | Requested Operation
Confirmed users are removed from cloudusersync.log
Open cloudusersync.log from C:\Program Files\Microsoft Configuration Manager\Logs and look for messages that users are removed
Please ask customers to provide a couple of sample UPNs after they remove all user licenses and **confirm in Viewpoint the sample users no longer have SCCM licenses.**
· **Delete** the iOS APNs certificate
· **Delete** any and all published applications that are for MDM Devices
· **Delete** any and all polices that are for MDM Devices
·  Remove the Windows Intune Connector from within the Configuration Manager Console
Provide info:
**Tenant ID**: xxx.onmicrosoft.com
**Global administrator email**: xxx.domain.com

## Step 3 – Do the checklist

Lets step through the main parts of the checklist.

```powershell
###
```
### Retire all Modern Devices

All Clients of Type Mobile must be retired:
[![image](/uploads/2016/04/image_thumb10.png "image")](/uploads/2016/04/image10.png)
Depending on the Device Type you can either select to only wipe company content or the device completely:
[![image](/uploads/2016/04/image_thumb11.png "image")](/uploads/2016/04/image11.png)
Or for typically a Windows 10 computer managed as a Mobile Device, you can only remove company content:
[![image](/uploads/2016/04/image_thumb12.png "image")](/uploads/2016/04/image12.png)
Warning notification:
[![image](/uploads/2016/04/image_thumb13.png "image")](/uploads/2016/04/image13.png)
After that the clients are in a status of “Pending Retire”, they will eventually be removed when they sync again. Some of my devices are inactive test devices, so I just turn them on and initiate a sync.
[![image](/uploads/2016/04/image_thumb14.png "image")](/uploads/2016/04/image14.png)
After a while I have still some devices left in a pending state. I know that these devices are not existing anymore, so they will not be able to sync. I will let the service request technician know about these, as instructed in the checklist.
In this case, the service request technician instructed me to remove the devices registered for the users in question in the Azure AD management portal (<http://manage.windowsazure.com>), select the user and removing any mobile devices registered.
You can also remove the devices from the user with MSOnline PowerShell module:
```powershell
Get-MsolDevice -RegisteredOwnerUpn *yourupn@domain.com* | Remove-MsolDevice
```
Or for all users that have workplace joined devices:
```powershell
Get-Msoldevice -All | Where {$_.DeviceTrustType -eq 'Workplace Joined'} | Remove-MsolDevice
```
### Point the Intune Subscription to an empty user collection and remove cloud synced users

I created a User Collection with a query that I know will not return any users, for example a non existing domain:
[![image](/uploads/2016/04/image_thumb15.png "image")](/uploads/2016/04/image15.png)
After that I update the Intune Subscription to use that collection:
[![image](/uploads/2016/04/image_thumb16.png "image")](/uploads/2016/04/image16.png)
Connect to the SQL site database, and run the following SQL query to ensure all licenses are removed from the DB:
*Insert into MDMCloudUserNotification Select ItemKey, 3, 0 from User\_Disc where CloudUserId is not null*
After that, restart the “SMS Executive” service, and look in the CloudUserSync.log to confirm that all users are removed.
[![image](/uploads/2016/04/image_thumb17.png "image")](/uploads/2016/04/image17.png)
Reset the SMS\_COLLECTION\_EVALUATOR thread through registry, Open Registry console, navigate to HKEY\_LOCAL\_MACHINE\SOFTWARE\Wow6432Node\Microsoft\SMS\Components\SMS\_EXECUTIVE\Threads\SMS\_COLLECTION\_EVALUATOR
–> Right click Requested Operation –> Modify –> type ”Stop” and click on ok.
Do a refresh till data value reset to “None” and then again edit it with “start” data value
Take another look in cloudusersync.log from <configuration manager install dir>\Logs and look for messages that users are removed.
The service request technician might ask customers to provide a couple of sample UPNs after they remove all user licenses and confirm in Viewpoint the sample users no longer have SCCM licenses.

### Remove MDM configurations from Config Mgr

After the users are removed, MDM configurations must be removed from Configuration Manager.
**Delete** the iOS APNs certificate:
How?
[![image](/uploads/2016/04/image_thumb18.png "image")](/uploads/2016/04/image18.png)
**Delete** any and all published applications that are for MDM Devices:
Under Software Library, find all applications for the Mobile Devices. Before the applications can be deleted, any deployments must be removed first.
**Delete** any and all polices that are for MDM Devices:
Under Asset and Compliance, delete all related to Mobile Devices..

- Compliance Settings|Configuration Baselines and Deployments
- Compliance Settings|Configuration Items
- Compliance Settings|Compliance Policies
- Company Resource Access|Certificate Profiles
- Company Resource Access|Email Profiles
- Company Resource Access|VPN Profiles
- Company Resource Access|Wi-Fi Profiles

Finally, remove the Windows Intune Connector from within the Configuration Manager Console.

## Step 4 - Update the Service Request

After I cleaned up, I provided my info to the service request technician and confirmed that I had completed the checklist:
**Tenant ID**: xxx.onmicrosoft.com
**Global administrator email**: xxx.domain.com
After a few days, I got the response that I should keep my hands off the subscription during the reset process:
[![image](/uploads/2016/04/image_thumb19.png "image")](/uploads/2016/04/image19.png)

## Step 5 – MDM Authority Reset Confirmation

A couple of days later I got the confirmation that the MDM authority was now reset:
[![image](/uploads/2016/04/image_thumb20.png "image")](/uploads/2016/04/image20.png)
Checking in the Intune Management Portal (<http://manage.microsoft.com>), I can now select to set Microsoft Intune as the Mobile Device Management Authority:
[![image](/uploads/2016/04/image_thumb21.png "image")](/uploads/2016/04/image21.png)

## Summary

All in all the whole process for me took 9 days. Some of these days was for me to complete the checklist, the rest was basically waiting for responses on questions, updates and the confirmation.
End result was as expected, I can now register my mobile devices with Microsoft Intune the MDM authority.
If I later want to go back to Configuration Manager as MDM Authority, I would have to do basically the whole reset process again, except that the cleanup will be in Microsoft Intune. A service request will provide details on that as well, and if I do it on a later time, I will put up a blog article on that as well!
