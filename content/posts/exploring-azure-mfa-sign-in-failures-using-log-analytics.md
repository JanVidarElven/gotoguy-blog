---
title: "Exploring Azure MFA sign-in failures using Log Analytics"
date: 2018-11-21T22:18:26Z
draft: false
slug: "exploring-azure-mfa-sign-in-failures-using-log-analytics"
categories:
  - "Azure AD"
  - "Azure MFA"
  - "Log Analytics"
---

Most IT admins, pros and end users from organizations that use Office 365 and Azure AD will by now have heard about the big Azure MFA outage on Monday November 19. When something like this happens, it is important to get insights on which users that were affected, and in what type of scenarios they most experienced the problem. Microsoft MVP Tony Redmond wrote a useful blog post ([https://office365itpros.com/2018/11/21/reporting-mfa-enabled-accounts/](https://office365itpros.com/2018/11/21/reporting-mfa-enabled-accounts/ "https://office365itpros.com/2018/11/21/reporting-mfa-enabled-accounts/")) on how to report on possible/potentially affected and MFA enabled users, and how to disable and re-enable those users. But many organizations are now using Conditional Access policies using Azure AD Premium, so this will be of limited help for those.
If I could wish **one thing** from Microsoft for Christmas this year, it would be to be able to manage MFA and Conditional Access policies with Azure AD PowerShell and Microsoft Graph! Admins could then run “break-the-glass” administrative users (or even “break-the-glass service principals”) to disable/re-enable policies when big MFA outages happens. A good CA policy design, trusting compliant devices and secure locations could also go a long way in mitigating such big outage problems.
Tony’s blog post made me think about the feature I recently activated, on integrating Azure AD Activity Logs to Azure Log Analytics, you can read more about this here: [https://gotoguy.blog/2018/11/06/get-started-with-integration-of-azure-ad-activity-logs-to-azure-log-analytics/](https://gotoguy.blog/2018/11/06/get-started-with-integration-of-azure-ad-activity-logs-to-azure-log-analytics/ "https://gotoguy.blog/2018/11/06/get-started-with-integration-of-azure-ad-activity-logs-to-azure-log-analytics/")
By exploring the Sign-in logs in Log Analytics I could get some more insights into how my organization was affected by the MFA outage on November 19. Please see the above blog post on how to get started setting up this integration, the rest of this blog post will show some sample queries for the SigninLogs.

## Querying the SigninLogs for failed and interrupted sign-ins

All the queries seen below are shown in screenshot images, but I have listed all them for you to copy at the end of the blog post.
First I can take a look at the SigninLogs for the specific day of 19th November, and the grouping on the result type and description of the sign-in events. For example I can see that there is a high number of event 50074: User did not pass the MFA challenge. Interestingly there is also a relatively high number of invalid username or password, that could be a separate issue but could also be that users that fails MFA sign-ins tries to log in again thinking they had wrong password first time.
[![image](/uploads/2018/11/image_thumb29.png "image")](/uploads/2018/11/image29.png)
Changing that query a little, I can exclude the successful sign-ins (ResultType 0), and sort on the most count of failures. Two of the events of most interest here is 50074 and 50076:
[![image](/uploads/2018/11/image_thumb30.png "image")](/uploads/2018/11/image30.png)
In this next query I focus on the "50074: User did not pass the MFA challenge" error. By increasing the time range to last 31 days, and adding a bin(TimeGenerated, 1d) to the summarize group, I'll be able to see the count of this error on each day in the last month. This will give me a baseline, and we can see that on the 19th this number spikes. I have added a render to timechart for graphical display. There are also some other days where this number increases, I can look into more insights for that if I want as well, but for now I will focus on the 19th.
[![image](/uploads/2018/11/image_thumb31.png "image")](/uploads/2018/11/image31.png)
Back to the time range of the 19th of November, I can modify the summarize to group by each hour, by using bin(TimeGenerated, 1h). This will show me how the problems evolved during the day. Must errors occurred about 10 am in the morning:
[![image](/uploads/2018/11/image_thumb32.png "image")](/uploads/2018/11/image32.png)
Lets look at some queries for how this error affected my environment. First I can group on the Users and how many errors they experience. Some users were really persistent in trying to get through the MFA error. I have masked the real names. We also see some admin accounts but admins quickly recognized that something was wrong, and actively sought information on the outage. By midday most users were notified on the on-going outage and the number of errors slowly decrease during the day.
[![image](/uploads/2018/11/image_thumb33.png "image")](/uploads/2018/11/image33.png)
In this next query, I group on the Apps the users tried to reach:
[![image](/uploads/2018/11/image_thumb34.png "image")](/uploads/2018/11/image34.png)
And in this following query, what kind of Client App they used. It would be normal that Browser is quite high, as mobile apps and desktop clients are more likely to have valid refresh tokens.
[![image](/uploads/2018/11/image_thumb35.png "image")](/uploads/2018/11/image35.png)
In this query I can look into the device operating system the users tried to sign in from:
![2018-11-21_22-05-27](/uploads/2018/11/2018-11-21_22-05-27.png)
In the following query I can look at which network the users tried to log in from, by identifying IP address:
[![image](/uploads/2018/11/image_thumb37.png "image")](/uploads/2018/11/image37.png)
And in this query we can get more location details from where users tried to sign in:
![2018-11-21_22-07-17](/uploads/2018/11/2018-11-21_22-07-17.png)

## Summary

Querying Log Analytics for Sign-in events as shown above can provide valuable insights into how such an outage can affect users. This can also give me some input on how to design Conditional Access policies. Querying this data over time can also provide a baseline for normal operations in your environment, and make it easier to set alert thresholds if you want to get alerts when number of failures inside a time interval gets higher than usual. Using Azure Monitor and action groups you can be pro-active and be notified if something similar should occur again.
Here are all the queries shown above:

```kusto
// Look at SigninLogs for a custom date time interval and group by sign in results
SigninLogs
| where TimeGenerated between(datetime("2018-11-19 00:00:00") .. datetime("2018-11-19 23:59:59")) 
| summarize count() by ResultType, ResultDescription

// Exclude successful signins and format results with sorting
SigninLogs
| where TimeGenerated between(datetime("2018-11-19 00:00:00") .. datetime("2018-11-19 23:59:59")) 
| where ResultType != "0" 
| summarize FailedSigninCount = count() by ResultDescription, ResultType 
| sort by FailedSigninCount desc

// Look at User did not pass the MFA challenge error last month to see trend
// and present to line chart group by each 1 day
SigninLogs
| where TimeGenerated >= ago(31d)
| where ResultType == "50074"
| summarize FailedSigninCount = count() by ResultDescription, bin(TimeGenerated, 1d)
| render timechart

// Look at User did not pass the MFA challenge error on the MFA outage day
// and present to line chart group by each 1 hour to see impact during day
SigninLogs
| where TimeGenerated between(datetime("2018-11-19 00:00:00") .. datetime("2018-11-19 23:59:59")) 
| where ResultType == "50074" 
| summarize FailedSigninCount = count() by ResultDescription, bin(TimeGenerated, 1h)
| render timechart

// Look at User did not pass the MFA challenge error on the MFA outage day
// and group on users to see affected users
SigninLogs
| where TimeGenerated between(datetime("2018-11-19 00:00:00") .. datetime("2018-11-19 23:59:59")) 
| where ResultType == "50074"
| summarize FailedSigninCount = count() by UserDisplayName
| sort by FailedSigninCount desc

// Look at User did not pass the MFA challenge error on the MFA outage day
// and group on Apps to see affected applications the users tried to sign in to
SigninLogs
| where TimeGenerated  between(datetime("2018-11-19 00:00:00") .. datetime("2018-11-19 23:59:59")) 
| where ResultType == "50074"
| summarize FailedSigninCount = count() by AppDisplayName
| sort by FailedSigninCount desc

// Look at User did not pass the MFA challenge error on the MFA outage day
// and group on client apps to see affected apps the users tried to sign in from
SigninLogs
| where TimeGenerated between(datetime("2018-11-19 00:00:00") .. datetime("2018-11-19 23:59:59")) 
| where ResultType == "50074"
| summarize FailedSigninCount = count() by ClientAppUsed
| sort by FailedSigninCount desc

// Look at User did not pass the MFA challenge error on the MFA outage day
// and group on device operating system to see affected platforms
SigninLogs
| where TimeGenerated between(datetime("2018-11-19 00:00:00") .. datetime("2018-11-19 23:59:59")) 
| where ResultType == "50074"
| summarize FailedSigninCount = count() by tostring(DeviceDetail.operatingSystem)
| sort by FailedSigninCount desc

// Look at User did not pass the MFA challenge error on the MFA outage day
// and group on IP address to see from which network users tried to sign in from
SigninLogs
| where TimeGenerated between(datetime("2018-11-19 00:00:00") .. datetime("2018-11-19 23:59:59")) 
| where ResultType == "50074"
| summarize FailedSigninCount = count() by IPAddress
| sort by FailedSigninCount desc

// Look at User did not pass the MFA challenge error on the MFA outage day
// and group on users location details to see which country, state and city users tried to sign in from
SigninLogs
| where TimeGenerated between(datetime("2018-11-19 00:00:00") .. datetime("2018-11-19 23:59:59")) 
| where ResultType == "50074"
| summarize FailedSigninCount = count() by tostring(LocationDetails.countryOrRegion), tostring(LocationDetails.state), tostring(LocationDetails.city)
| sort by FailedSigninCount desc
```
