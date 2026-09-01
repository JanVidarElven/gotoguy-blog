---
title: "Blog Series - Power'ing up your Home Office Lights using Power Platform - Introduction"
date: 2020-12-02T12:10:04Z
draft: false
slug: "blog-series-powering-up-your-home-office-lights-using-power-platform-introduction"
tags:
  - "Microsoft Graph"
  - "Microsoft Teams"
categories:
  - "Logic Apps"
  - "Philips Hue"
  - "Power Automate"
  - "PowerApps"
  - "Smart House"
---

Microsoft Power Platform can be used in a variety of creative ways to both learn and create awesome automation solutions, and you can even use this platform for your home automation. In this series of blog posts and introductory videos I will show you how you can control your Home Office Lights (in my case Phillips Hue) via API and Power Platform components like PowerApps, Power Automate, Logic Apps and more.



As an introduction, lets start with the "birds overview" over the solution I've built:


[![](/uploads/2020/11/powerplatform-hue-lights.png?w=1001)](/uploads/2020/11/powerplatform-hue-lights.png)



The main idea was to be able to both interactively, and triggered based on events, to be able to control my Philips Hue Lights using Power Platform components like PowerApps and Power Automate. Why you say? Well, it's cool isn't it! And fun, and a well worth project to invest time in because of the great learning potential. I have learnt tons of new stuff, about Power Platform, Microsoft Graph, SharePoint Lists, and Azure resources like Key Vault, Logic Apps etc. And not to forget, I've learnt a lot about the Hue Remote API and implementation of Oauth!



I will get into the chosen solutions and why I elected to use the technologies mentioned, and how they interact as shown in the diagram above, but first I wanted to provide you with this short introduction video from me on the concept:


https://youtu.be/L6ZwwgkbGg0



This blog post is the introduction to the series of blog posts, and also a part of my contribution to the Festive Tech Calendar 2020 <https://festivetechcalendar.com/>. As soon as the schedule is published, I will at the allocated date later in December do a live stream broadcast where I will talk about this solution and do a Q/A where I will try to answer all your questions. But before that, I will publish the all parts of the blog series and accompanying videos as shown below. Links will become alive as soon as I have published. This way you can follow along and by the time of the live stream, you could have your own solution up and running!



The blog series will consist of the following parts, links will be available as soon as the parts are published:



1. [Power'ing up your Home Office Lights: Part 1 - Get to know your Hue Remote API and prepare for building your solution](https://gotoguy.blog/2020/12/02/blog-series-powering-up-your-home-office-lights-part-1-get-to-know-your-hue-remote-api-and-prepare-for-building-your-solution/).
2. [Power'ing up your Home Office Lights: Part 2 - Prepare Azure Key Vault for storing your API secrets](https://gotoguy.blog/2020/12/03/blog-series-powering-up-your-home-office-lights-part-2-prepare-azure-key-vault-for-storing-your-api-secrets/).
3. [Power'ing up your Home Office Lights: Part 3 - Using Logic Apps to Authorize and Get Access Token using Oauth and Hue Remote API](https://gotoguy.blog/2020/12/04/blog-series-powering-up-your-home-office-lights-part-3-using-logic-apps-to-authorize-and-get-access-token-using-oauth-and-hue-remote-api/).
4. [Power'ing up your Home Office Lights: Part 4 - Using Logic Apps to Get Access Token and Renew Access Token if needed](https://gotoguy.blog/2020/12/05/blog-series-powering-up-your-home-office-lights-part-4-using-logic-apps-to-get-access-token-and-renew-access-token-if-needed/).
5. [Power'ing up your Home Office Lights: Part 5 - Using Power Automate Flow to Get Access Token and Config](https://gotoguy.blog/2020/12/06/blog-series-powering-up-your-home-office-lights-part-5-using-power-automate-flow-to-get-access-token-and-config/).
6. [Power'ing up your Home Office Lights: Part 6 - Using Power Automate Flow to Link Button and Whitelist user](https://gotoguy.blog/2020/12/07/blog-series-powering-up-your-home-office-lights-part-6-using-power-automate-flow-to-link-button-and-whitelist-user/).
7. [Power'ing up your Home Office Lights: Part 7 - Building the PowerApp for Hue to Get Config and Link user](https://gotoguy.blog/2020/12/08/blog-series-powering-up-your-home-office-lights-part-7-building-the-powerapp-for-hue-to-get-config-and-link-user/).
8. [Power'ing up your Home Office Lights: Part 8 - Using Power Automate Flows to Get and Set Lights State](https://gotoguy.blog/2020/12/09/blog-series-powering-up-your-home-office-lights-part-8-using-power-automate-flows-to-get-and-set-lights-state/).
9. [Power'ing up your Home Office Lights: Part 9 - Using Microsoft Graph to get Teams Presence and show state in PowerApp](https://gotoguy.blog/2020/12/10/blog-series-powering-up-your-home-office-lights-part-9-using-microsoft-graph-to-get-teams-presence-and-show-state-in-powerapp/).
10. [Power'ing up your Home Office Lights: Part 10 - Subscribe to Graph and Teams Presence to automatically set Hue Lights based on my Teams Presence](https://gotoguy.blog/2020/12/11/blog-series-powering-up-your-home-office-lights-part-10-subscribe-to-graph-and-teams-presence-to-automatically-set-hue-lights-based-on-my-teams-presence/)!



Well, I certainly have my work cut out, so I better get started. Thanks for reading, please follow the progress and join me on the later live stream!
