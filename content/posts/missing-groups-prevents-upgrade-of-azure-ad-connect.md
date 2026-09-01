---
title: "Missing groups prevents upgrade of Azure AD Connect"
date: 2016-04-13T21:43:22Z
draft: false
slug: "missing-groups-prevents-upgrade-of-azure-ad-connect"
tags:
  - "Enterprise Mobility"
categories:
  - "Azure AD"
  - "Enterprise Mobility Suite"
---

This is just a short blog article on a problem I experienced when upgrading Azure AD Connect from a previous version. This was a small environment where the Azure AD Connect server was running on the Domain Controller.
When starting the upgrade process I noticed that a message was displayed that a “Group with name ADSyncAdmins was not found in the Machine context”. When I clicked to Upgrade anyway, an error message was displayed that it was “Unable to upgrade the Synchronization Service”:
[![image](/uploads/2016/04/image_thumb1.png "image")](/uploads/2016/04/image1.png)
Looking into the event log, I found this error:
Product: Microsoft Azure AD Connect synchronization services -- Error 25037.The groups entered do not all exist or cannot be found. Verify that each group name is correct, and then try again.
[![image](/uploads/2016/04/image_thumb2.png "image")](/uploads/2016/04/image2.png)
Since this was a Domain Controller, and there is no Local Users and Groups, I created the ADSyncAdmins group in Active Directory, as a Domain Local Security group. Trying the upgrade again, I got a new group that was missing:
[![image](/uploads/2016/04/image_thumb3.png "image")](/uploads/2016/04/image3.png)
So I ended up creating these 4 groups that was missing:

- ADSyncAdmins
- ADSyncBrowse
- ADSyncOperators
- ADSyncPasswordSet

After that I was able to successfully finish the upgrade of Azure AD Connect.
