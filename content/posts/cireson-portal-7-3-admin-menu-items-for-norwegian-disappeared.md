---
title: "Cireson Portal 7.3 &ndash; Admin Menu Items for Norwegian Disappeared"
date: 2017-02-17T12:07:19Z
draft: false
slug: "cireson-portal-7-3-admin-menu-items-for-norwegian-disappeared"
tags:
  - "Cireson;ITSM;Service Manager"
categories:
  - "Cireson Portal"
  - "Service Manager"
---

After upgrading a couple of customers and our own environment til the latest Cireson Portal 7.3, I saw that the new re-arranged Admin menu was missing some expected menu elements. This is what I saw:
[![image](/uploads/2017/02/image_thumb22.png "image")](/uploads/2017/02/image22.png)
After investigating I found that the reason was if the logged on Admin user was configured with Norwegian display language. When I switched to English, I saw this Admin menu:
[![image](/uploads/2017/02/image_thumb23.png "image")](/uploads/2017/02/image23.png)
To solve this I navigated to the Localization Settings and checked the list for NOR that missed translations, and provided Norwegian translations for every related setting for the Admin menu (both the links and the labels at each admin section):
[![image](/uploads/2017/02/image_thumb24.png "image")](/uploads/2017/02/image24.png)
After that I could switch back to Norwegian display language again, now showing the correct Admin menu:
[![image](/uploads/2017/02/image_thumb25.png "image")](/uploads/2017/02/image25.png)
