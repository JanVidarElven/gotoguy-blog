---
title: "Keep your Cireson Self Service Portal Website Ready and Alive"
date: 2015-01-07T17:39:43Z
draft: false
slug: "keep-your-cireson-self-service-portal-website-ready-and-alive"
tags:
  - "Cireson"
  - "IIS"
  - "Self-Service Portal"
categories:
  - "Service Manager"
---

Cireson have done a great job optimizing the performance of the Self Service Portal for Service Manager.

Since the Self Service Portal is running on a web site in IIS, some additional configurations can help you keeping the portal site ready and alive.

From my experience working with the Self Service Portal, some operations can take a while to respond if you have not been active for a while. This is especially true when using the portal in a pilot or test environment where traffic is more intermittent.

Two settings I recommend to configure are the Idle Time-out and Application Pool Recycling settings.

**Idle Time-out**

The Idle Time-out will cause the application pool in IIS to terminate when there is no traffic. The default setting is 20 minutes, and after that the first user to access the web site, will have to wait while the app pool creates a new w3wp.exe worker process, waiting for creating the app pool, loading the ASP.NET or another framework, and then load the web application.

You find the Idle Time-out in Internet Information Services Manager, under Application Pools. Right-click the CiresonPortal application pool and select Advanced Settings. There you will find the default value of 20 minutes:

![](/uploads/2015/01/010715_1736_keepyourcir1.png)

I recommend changing it to zero, which means it will never time out:

![](/uploads/2015/01/010715_1736_keepyourcir2.png)

Following this setting, you should also configure the automatic recycling of the pool next.

**Application Pool Recycling**

It is a good idea to recycle the application pool regularly. You find the Recycling settings by right clicking the Application Pool and choosing Recycling:

![](/uploads/2015/01/010715_1736_keepyourcir3.png)

The default setting is to recycle the application pool every 1740 minutes, which is 29 hours. The reason for why exactly 29 hours is that it is the first prime number after 24, explained here <http://weblogs.asp.net/owscott/why-is-the-iis-default-app-pool-recycle-set-to-1740-minutes>.

![](/uploads/2015/01/010715_1736_keepyourcir4.png)

For the CiresonPortal pool, I recommend setting a specific time that suits you, for example every morning, which I have done here:

![](/uploads/2015/01/010715_1736_keepyourcir5.png)

**PS! Installing Cireson Portal Updates**

Please remember that every time you use the setup program to update the Cireson Self-Service Portal installation, you will have to re-configure the Idle Time-out and Recycling settings.
