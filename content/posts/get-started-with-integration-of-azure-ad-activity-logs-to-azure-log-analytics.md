---
title: "Get started with integration of Azure AD Activity Logs to Azure Log Analytics"
date: 2018-11-06T22:08:43Z
draft: false
slug: "get-started-with-integration-of-azure-ad-activity-logs-to-azure-log-analytics"
categories:
  - "Azure AD"
  - "Azure Monitor"
  - "Log Analytics"
---

Recently Microsoft announced the availability of forwarding the Azure AD Activity Logs to Azure Log Analyctis. You can read the announcement in full here: [https://techcommunity.microsoft.com/t5/Azure-Active-Directory-Identity/Azure-Active-Directory-Activity-logs-in-Azure-Log-Analytics-now/ba-p/274843](https://techcommunity.microsoft.com/t5/Azure-Active-Directory-Identity/Azure-Active-Directory-Activity-logs-in-Azure-Log-Analytics-now/ba-p/274843 "https://techcommunity.microsoft.com/t5/Azure-Active-Directory-Identity/Azure-Active-Directory-Activity-logs-in-Azure-Log-Analytics-now/ba-p/274843").
By bringing thousands (or even millions depending on your organization size and use of Azure AD), of sign-in and audit log events to Log Analytics you can finally use the power of Log Analytics for query, analyze, visualize and alert on your data.
In this blog post I will show how to get started and provide some useful tips. Most of this is already well documented in the following Microsoft Docs, but I will provide my own perspective and experience and as well let this blog post be an anchor for future detailed blog posts on the subject of analyzing Azure AD sign-in and audit logs in Log Analytics and Azure Monitor:

- Integrate Azure AD logs with Log Analytics using Azure Monitor: [http://aka.ms/AzureADLogAnalytics](http://aka.ms/AzureADLogAnalytics "http://aka.ms/AzureADLogAnalytics")
- Analyze Azure AD activity logs with Log Analytics, sample queries: [https://aka.ms/AzureADLogAnalyticsqueries](https://aka.ms/AzureADLogAnalyticsqueries "https://aka.ms/AzureADLogAnalyticsqueries")
- Install and use the Log Analytics views for Azure Active Directory: [https://aka.ms/AADLogAnalyticsviews](https://aka.ms/AADLogAnalyticsviews "https://aka.ms/AADLogAnalyticsviews")

## Set up Diagnostic Settings to Log Analytics

The first action we need to do is to Turn on diagnostics in the Azure AD Portal. You will need to be a **Global Administrator** or **Security Administrator** to do this:
[![image](/uploads/2018/11/image_thumb.png "image")](/uploads/2018/11/image.png)
PS! Another way to get to this setting to Turn on diagnostics is to either go to Sign-ins or Audit logs under Monotoring, and from there click on Export Data Settings:
[![SNAGHTML591fe33](/uploads/2018/11/snaghtml591fe33_thumb.png "SNAGHTML591fe33")](/uploads/2018/11/snaghtml591fe33.png)
Next select to Send to Log Analytics, and then select either or both of the AuditLogs or SigninLogs.
[![image](/uploads/2018/11/image_thumb1.png "image")](/uploads/2018/11/image1.png)
Note that to be able to export Sign-in data, your organization needs Azure AD Premium P1 or P2 (or EMS E3/E5). This requirement only applies to sign-in logs, not audit logs.
After selecting Log Analytics, and which logs to export, you need to configure which Log Analytics (still named as OMS) workspace to export the data to:
[![image](/uploads/2018/11/image_thumb2.png "image")](/uploads/2018/11/image2.png)
Note that this requires access to an Azure Subscription. You can either select an existing OMS workspace or create a new:
[![image](/uploads/2018/11/image_thumb3.png "image")](/uploads/2018/11/image3.png)
**Important info!** Usually you will need to be a Global Administrator or Security Administrator to be able to access the details of Sign-in logs or Audit logs in Azure AD, but by exporting this data to either an existing or a new Log Analytics workspace, potentially a lot more users can access that data. You need to think about if this is something you want to do, and at least control and govern which users can access that Log Analytics workspace.
For this reason alone it would probably be a better idea to create a dedicated Log Analytics workspace for the Azure AD activity logs:
[![image](/uploads/2018/11/image_thumb4.png "image")](/uploads/2018/11/image4.png)
Regarding pricing, using a Log Analytics workspace for Azure AD Activity Logs alone should not incur a notable cost in most normal environments. In an environment of less than 100 users I found the following consumption per day, which is way below the amount of free data you get included:
[![image](/uploads/2018/11/image_thumb5.png "image")](/uploads/2018/11/image5.png)
If you want to save and use that same query yourself, here it is:

```kusto
Usage| where TimeGenerated > startofday(ago(31d))| where IsBillable == true
| where (DataType == "SigninLogs" or DataType == "AuditLogs") and Solution == "LogManagement"
| summarize TotalVolumeGB = sum(Quantity) / 1024 by bin(TimeGenerated, 1d), Solution| render barchart
```

Choosing a pricing tier depends on whether the Subscription was created before April 2, 2018 or not, or whether you have elected to move to a new pricing model. The older pricing model had a choice of free tier, which had a daily cap of 500 MB and a data retention of 7 days. As the diagram above showed, most organizations will be way below the 500 MB daily cap, but a retention of only 7 days will be considered short for most analyzing needs. So under the older pricing model you would consider a standalone per GB model, giving a retention of 1 month by default, but a cost of $2.30 per GB.
The new pricing model after April 2, 2018 has a simplified pricing model. Here the first 5 GB are free and you have a default retention of 31 days. Additional GBs for ingestion are $2.99 per month, and extra retention after the first 31 days is $0.13 per GB per month. Note that this pricing model is on subscription level and affects all your Log Analytics workspaces, so you need to carefully consider any changes to the new pricing model in your subscription.
After you have selected/created a Log Analytics workspace, and provided a name for the Diagnostic settings, you are ready to Save:
[![image](/uploads/2018/11/image_thumb6.png "image")](/uploads/2018/11/image6.png)
After about 15 minutes you can start explore the Logs in the Log Analytics workspace.

## Start to Analyze Azure AD Activity logs with Log Analytics

To begin analyze the exported Azure AD Activity Logs with Log Analytics, you can either go to the Log Analytics section in your Azure Portal. You can also access the logs directly from Azure Active Directory from under the Monitoring section, which will take you directly to the configured Log Analytics workspace:
[![image](/uploads/2018/11/image_thumb7.png "image")](/uploads/2018/11/image7.png)
By default this will open a search query showing sample data from all your Log Analytics workspace.
I find that a good way to start learning about the sign-in and audit logs is to look at the schema. The SigninLogs and AuditLogs schemas should appear right under LogManagement as shown below:
[![SNAGHTML5fc1b7b](/uploads/2018/11/snaghtml5fc1b7b_thumb.png "SNAGHTML5fc1b7b")](/uploads/2018/11/snaghtml5fc1b7b.png)
To look at the SigninLogs just add that to the query window and select a time range and click Run:
[![image](/uploads/2018/11/image_thumb8.png "image")](/uploads/2018/11/image8.png)
Depending on your sample data you can start filter on the left side, for example to look at only certain app sign ins, or client apps used, location and more..
Similarly for AuditLogs, in the following example I have set a time range of last 7 days:
[![image](/uploads/2018/11/image_thumb9.png "image")](/uploads/2018/11/image9.png)
See the links in the beginning of this blog post for some more sample queries and you can also import some sample views.
So now that we have a working diagnostic setting that exports my Azure AD sign-in and audit logs to Azure Log Analytics, I’m ready to explore some interesting scenarios for analyzing this data. This will be a topic for upcoming blog posts, so stay tuned for that!
Thanks for reading so far, I'm really excited for this feature! ![Smile](/uploads/2018/11/wlemoticon-smile.png)
