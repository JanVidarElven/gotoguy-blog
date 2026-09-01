---
title: "Session Recap, PowerShell Scripts and Resources from session on Azure AD Management Skills at NICConf 2017"
date: 2017-02-12T10:26:34Z
draft: false
slug: "session-recap-powershell-scripts-and-resources-from-session-on-azure-ad-management-skills-at-nicconf-2017"
tags:
  - "Azure AD Premium"
  - "Graph"
categories:
  - "Azure AD"
  - "Enterprise Mobility + Security"
  - "PowerShell"
---

Last week at NICConf I presented two sessions on Management of Microsoft Azure AD, [Application Publishing with Azure AD - the New Management Experience!](http://www.nicconf.com/application-publishing-with-azure-ad--the-new-management-experience) and [Take your Azure AD Management Skills to the Next Level with Azure AD Graph API and Powershell!](http://www.nicconf.com/-take-your-azure-ad-management-skills-to-the-next-level-with-azure-ad-graph-api-and-powershell)
In the last session i presented demos and scripts with some technical details, so in this blog post I will link to those PowerShell scripts together with some explanations. See also my slides for the sessions published here: <https://docs.com/jan-vidar-elven-1/7677/nicconf-2017>, and the session recording might be available later which I will link to.
First i talked about the new Azure AD PowerShell v2 module and install info:
https://gist.github.com/skillriver/35fba9647fbfbe3e99718f0ad734b241
Then connecting and exploring some objects and license info:
https://gist.github.com/skillriver/df58d6658d15907f56c56a81a7d2cf3e
Then performing some Administration tasks including creating Dynamic Groups, setting user thumbnail photo, adding licenses and changing passwords:
https://gist.github.com/skillriver/947e83ad729fdb3200857ea4d1e4c722
In the next part of my session I went on to talk about the Azure AD Graph API and the Microsoft Graph API. The Microsoft Graph API will eventually be the "one API to rule them all", as Azure AD also can be accessed by that API, but there are still use cases for the Azure AD Graph API.
In either case, to be able to use the APIs you must create and register an Azure AD Application of type Web App/Api, and give that Application the needed permissions to access the APIs. I showed in my session how to do this in the portal, and here you have a PowerShell Script for creating that same type of Application, this example for accessing the Azure AD Graph API:
https://gist.github.com/skillriver/b46c51e2902a331a91221c6828bd320c
Note that for the above script, you will need to note some output and manual operations:

- Take a note of the Application ID, you will need that later:
  ![azureadapp](/uploads/2017/02/azureadapp.png)
- Take note of the Key Secret, you will need that later also:
  ![azureadappkeysecret](/uploads/2017/02/azureadappkeysecret.png)
- Application must be manually granted permission here, as this per now cannot be automated with PowerShell:
  ![azureadappgrantpermission](/uploads/2017/02/azureadappgrantpermission.png)

By the way, you should newer share this App Id and key secret publically (as I have just done here ;) Other people could use that same information to access your APIs and Azure AD info, so take care to protect that info! (Of course I have deleted that info after showing this here ;)
Now, with this App registered in Azure AD, we can now start managing Azure AD via REST API calls, for example from PowerShell. The following script shows how we can get Self Service Password Registration Activity via the Azure AD Graph API, specifically we will use the Reporting API (<https://msdn.microsoft.com/en-us/library/azure/ad/graph/howto/azure-ad-reports-and-events-preview>). Note that the script will need the App Id and Key value noted from above:
https://gist.github.com/skillriver/e77a2aa15975445867241b0dc430afcd
With that last export to a Csv file I can import it to Power BI as a table, and create a report and a dashboard on it, for example showing which password reset registration method the users configured, what user and role type did the registration and the count and date for the registrations:
![PowerBIReport.PNG](/uploads/2017/02/powerbireport.png)
In the session we also looked at the new Content Pack for Azure AD, showing sign-in and audit events, and also how you can get data from the Microsoft Graph API using a OData Feed:
[gallery ids="1160,1161" type="rectangular"]
I hope this scripts will be as useful for you as it is for me! Good luck with taking your management of Azure AD to the next level with Azure AD PowerShell and Graph APIs!
