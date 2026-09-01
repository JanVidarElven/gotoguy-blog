---
title: "How to add Azure AD Application Proxy Connector Log to Operations Management Suite"
date: 2015-07-01T08:58:29Z
draft: false
slug: "how-to-add-azure-ad-application-proxy-connector-log-to-operations-management-suite"
tags:
  - "Azure"
  - "Azure AD Application Proxy"
  - "Operations Management Suite"
categories:
  - "Operational Insights"
  - "Operations Managment Suite"
---

If you have published Proxy Applications with Azure AD App Proxy, you will also have installed one or more Application Proxy Connectors in your environment.
When you install the Application Proxy Connector, you will also get an event log for the Connectors Information, Warning or Error events.
I wanted to bring these events to my Operations Management Suite (OMS) environment, so this blog post shows how to do that.
First, let us look at the event log in question. Here I have some events, I also see that I have some warning and error events, showing that I have an issue with connecting to a backend server published with Azure AD App Proxy:
![](/uploads/2015/07/070115_0853_howtoaddazu1.png)
Before I can add this event log to OMS, I need to determine the name of the event log. I select Properties for the log:
![](/uploads/2015/07/070115_0853_howtoaddazu2.png)
The name of the log is **Microsoft-AadApplicationProxy-Connector/Admin**.
Now I can log into Operations Management Suite to configure the log source. I go to Settings and select the Logs section. I then add the name of the Application Proxy Connector log, and select which type of events that I want to collect. In my case I select Error and Warning.
![](/uploads/2015/07/070115_0853_howtoaddazu3.png)
When saving that, OMS will soon start collection event log entries from the Connector Proxy log, assuming of course that the server in question have an agent installed, either directly or via Operations Manager Management Group:
![](/uploads/2015/07/070115_0853_howtoaddazu4.png)
Let us see how it looks when data from the event log are appearing in OMS.
I start by doing a Log Search. I can either specify the query directly, like this: Type=Event EventLog="Microsoft-AadApplicationProxy-Connector/Admin", or I can select from all events and filter my way to the event log I want to.
This is how I specified the query:
![](/uploads/2015/07/070115_0853_howtoaddazu5.png)
I can see that I have some errors and warnings, let us drill into one of them. I do this by clicking [+] show more. I can now see the same error with backend as I had in the local event log:
![](/uploads/2015/07/070115_0853_howtoaddazu6.png)
So, my objective for getting the Connector Proxy event log data to OMS has been fulfilled, and I can start grouping, filtering and searching the log data.
As a last step, let us add a Dashboard view for this data.
First, I select to Save my Search:
![](/uploads/2015/07/070115_0853_howtoaddazu7.png)
Then I go to My Dashboard, and select Customize:
![](/uploads/2015/07/070115_0853_howtoaddazu8.png)
I find my Saved Search and add it to the Dashboard:
![](/uploads/2015/07/070115_0853_howtoaddazu9.png)
If I want to I can customize the Tile Visualization:
![](/uploads/2015/07/070115_0853_howtoaddazu10.png)
When I finish customizing, I now have a Dashboard Tile for Azure AD App Proxy Events, and by clicking it, I am going directly to the Log Search:
![](/uploads/2015/07/070115_0853_howtoaddazu11.png)
Hope this has been helpful, happy log searching in OMS!
