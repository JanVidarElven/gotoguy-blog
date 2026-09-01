---
title: "Alert on On-premises Connectivity for Self Service Password Reset using Azure Monitor and Azure AD Activity Logs in Log Analytics"
date: 2018-11-11T12:07:21Z
draft: false
slug: "alert-on-on-premises-connectivity-for-self-service-password-reset-using-azure-monitor-and-azure-ad-activity-logs-in-log-analytics"
categories:
  - "Azure"
  - "Azure AD"
  - "Azure Monitor"
  - "Log Analytics"
  - "Self-Service Password Reset"
---

Recently I wrote a blog post on how to get started with integration of Azure AD Activity Logs to Azure Log Analytics. Setting up this is a requirement for the solution in this blog post, so make sure you have set this up first: [http://gotoguy.blog/2018/11/06/get-started-with-integration-of-azure-ad-activity-logs-to-azure-log-analytics/](http://gotoguy.blog/2018/11/06/get-started-with-integration-of-azure-ad-activity-logs-to-azure-log-analytics/ "http://gotoguy.blog/2018/11/06/get-started-with-integration-of-azure-ad-activity-logs-to-azure-log-analytics/").
In this blog post I wanted to show a practical example on how to create an alert for when Azure AD Self Service Password fails in password writeback because of connectivity error to the On-premises environment.

## Build the query

If you know the schema, you can write the query directly, but more often than not you will work out these scenarios by exploring your actual log data. In my example we had a concrete example where password resets failed because of On-premises connectivity error. Looking into the Azure Log Analytics logs, I started with this simple query against AuditLogs:
[![image](/uploads/2018/11/image_thumb10.png "image")](/uploads/2018/11/image10.png)
After that I looked into the filters, and found that I could filter on Failures:
[![image](/uploads/2018/11/image_thumb11.png "image")](/uploads/2018/11/image11.png)
This resultated in some failure results. Exploring the results in the bottom right windows, I found that the failures had a ResultDescription of “OnPremisesConnectivityError”:
[![image](/uploads/2018/11/image_thumb12.png "image")](/uploads/2018/11/image12.png)
By clicking on the plus sign above I add that to the query:
[![image](/uploads/2018/11/image_thumb13.png "image")](/uploads/2018/11/image13.png)
I want to save my query next, so that I have it available for later:
[![image](/uploads/2018/11/image_thumb14.png "image")](/uploads/2018/11/image14.png)
Now that I have the results I want I can proceed to create an Alert Rule. Btw, here is the full query (I have since amended it to include OnPremisesConnectivityFailure in addition):

```kusto
AuditLogs
| where Category == "Self-service Password Management"
| where ResultType == "Failure"
| where ResultDescription == "OnPremisesConnectivityError" or ResultDescription == "OnPremisesConnectivtyFailure"
```

## Create an Alert Rule

Next, I can create a new Alert Rule for this query, something you can do directly from the query:
[![image](/uploads/2018/11/image_thumb15.png "image")](/uploads/2018/11/image15.png)
This next step would bring me over to the Azure Monitor and Rules Management section. The alert target (OMS/Log Analytics Workspace) and target hierarchy (Azure Subscription and Resource Group) should already be specifed:
[![image](/uploads/2018/11/image_thumb16.png "image")](/uploads/2018/11/image16.png)
Now I need to configure the alert criteria. Note that currently monthly cost for this alert is $1.50. Click on the criteria to configure the signal logic:
[![image](/uploads/2018/11/image_thumb17.png "image")](/uploads/2018/11/image17.png)
Here we see the query from before, as well as we need to set a threshold for number of results, and a period and frequency. Pricing details can be found at: [https://azure.microsoft.com/en-us/pricing/details/monitor/](https://azure.microsoft.com/en-us/pricing/details/monitor/ "https://azure.microsoft.com/en-us/pricing/details/monitor/"). If you look at Alert signals and Log section, you’ll see that alerts with frequency of 5 minutes is $1.5, 10 minutes $1 and 15 minutes $0.5. This is per log monitored. I changed my period and frequency to 15 minutes:
[![image](/uploads/2018/11/image_thumb18.png "image")](/uploads/2018/11/image18.png)
After I click done I see that the alert criteria is correctly configured with a price of $0.50:
[![image](/uploads/2018/11/image_thumb19.png "image")](/uploads/2018/11/image19.png)
Next I need to specify the alert details, for example like below. You also have the option to supress multiple alerts inside a time window. I configured 60 minutes:
[![image](/uploads/2018/11/image_thumb20.png "image")](/uploads/2018/11/image20.png)
Next I need to either select an existing action group or create a new. An action group decides which action to take when an alert occures:
[![image](/uploads/2018/11/image_thumb21.png "image")](/uploads/2018/11/image21.png)
I’ll create a new action group for now. In this action group I will select to send an e-mail to a group in my company. As you see in the image below I have several options for action type, examples of use can be:

- Trigger e-mail, SMS, push or other notifications.
- Trigger Azure Functions for running some code logic.
- Trigger Logic App for executing a business flow logic.
- Trigger a webhook for posting a status, for example to a Microsoft Teams webhook.
- Send the Alert via ITSM connector to create an incident in your connected ITSM system.
- Trigger a Runbook in Azure Automation to run your own PowerShell runbooks, or you can use one of the built-in runbooks for restart, stop, remove or scale up/down VM.

[![image](/uploads/2018/11/image_thumb22.png "image")](/uploads/2018/11/image22.png)
When selecting Email I need to specify an e-mail address for the user/group I want to notify:
[![image](/uploads/2018/11/image_thumb23.png "image")](/uploads/2018/11/image23.png)
After that I’m ready to create the Alert rule:
[![SNAGHTML50ef585](/uploads/2018/11/snaghtml50ef585_thumb.png "SNAGHTML50ef585")](/uploads/2018/11/snaghtml50ef585.png)
After I created the rule, the group e-mail address I specified received this e-mail, confirming that it is now part of an action group:
[![image](/uploads/2018/11/image_thumb24.png "image")](/uploads/2018/11/image24.png)
If you want to locate and change this alert rule at a later stage, you will find it under Azure Monitor and Alert Rules:
[![image](/uploads/2018/11/image_thumb25.png "image")](/uploads/2018/11/image25.png)
Thats it, now we can just wait for future Self-Service Password Reset or Change connectivity errors, and we will get notified.

## Testing the Alert rule Notification

For testing, I just wanted to force the error by logging into my Azure AD Connect Server and stop the service.
After that I tried to reset or change my password, resulting in this error message shown to the user:
[![image](/uploads/2018/11/image_thumb26.png "image")](/uploads/2018/11/image26.png)
Now in this situation, most users will either just wait and try again later, try one more time and then give up, and if you are lucky they will contact their IT admin and notify of the error. More often than not users just leave it there, and not notify anyone. This is where it is useful to get an alert as we have created here, because then you as an IT admin can proactively analyze and fix the error before it affects more users. This is the alert I received to my specified group:

```powershell
##
```
[![image](/uploads/2018/11/image_thumb27.png "image")](/uploads/2018/11/image27.png)
We can directly click on the result to get into details for the error, for example which user was affected, from which IP address and more:
[![image](/uploads/2018/11/image_thumb28.png "image")](/uploads/2018/11/image28.png)
I don’t know about you, but I think this is just brilliant :) With the integration of Azure AD Activity Logs in Log Analytics, I can really explore and analyze a lot of the operations going on in my tenant, and using Azure Monitor I can create alert rules that notifies or trigger other actions to handle those alerts.
Thanks for reading, more blog post will follow on this subject of Azure AD and Log Analytics, so stay tuned!
