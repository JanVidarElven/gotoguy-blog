---
title: "Get and Set Automatic Replies like OOF with Microsoft Graph"
date: 2019-07-11T13:23:01Z
draft: false
slug: "get-and-set-automatic-replies-like-oof-with-microsoft-graph"
tags:
  - "Automatic Replies"
  - "Exchange Online"
  - "Graph Explorer"
categories:
  - "Microsoft Graph"
  - "Office 365"
---

Hi, a short blog post this time as Summer Vacation 2019 is here shortly! And on that note, the topic of the post is to show how you can get and set automatic replies with Microsoft Graph. Automatic replies, previously known as Out of Office (OOF) messages is a mailbox setting for each Exchange Online enabled user.



The Microsoft Graph API documentation for mailbox settings is located here: <https://docs.microsoft.com/en-us/graph/api/user-get-mailboxsettings?view=graph-rest-1.0&tabs=http>, and besides automatic replies you can also get and set locale (language and country/region), time zone, and working hours.



But for now we will only focus on automatic replies, using the automaticRepliesSetting resource type: <https://docs.microsoft.com/en-us/graph/api/resources/automaticrepliessetting?view=graph-rest-1.0>.



This resource type has the following settings:



```json
{
   "externalAudience": "String",
   "externalReplyMessage": "string",
   "internalReplyMessage": "string",
   "scheduledEndDateTime": {"@odata.type": "microsoft.graph.dateTimeTimeZone"},
   "scheduledStartDateTime": {"@odata.type": "microsoft.graph.dateTimeTimeZone"},
   "status": "String"
 }
```



Let’s look at some different samples, and I will use Graph Explorer (<https://aka.ms/ge>). Please note that every end user already have user permission to get or set their own mailbox settings, but you need an Exchange Admin role to get or set the settings for other users in your organization. In addition, if you create your own app registration for Microsoft Graph, you need to make sure the app has either MailboxSettings.Read or MailboxSettings.ReadWrite permission.



In Graph Explorer, after you sign in with your work account, you can modify these permissions if needed:


[![image](/uploads/2019/07/image_thumb.png)](/uploads/2019/07/image.png)



After signing out and in again you will be prompted to consent, if you havent already:


[![image](/uploads/2019/07/image_thumb-1.png)](/uploads/2019/07/image-1.png)



## Get Current Mailbox Settings



To get your own current settings you can run the following:


> GET /me/mailboxSettings



In Graph Explorer this would look like this, and you might have some previous values set here. In my example automatic replies have a status of disabled:


[![image](/uploads/2019/07/image_thumb-2.png)](/uploads/2019/07/image-2.png)



To get another users mailbox settings you can run the following (but then you must be an Exchange Admin):


> GET /users/{id|userPrincipalName}/mailboxSettings



## Simple Update of Status



Lets see how Microsoft Graph can be used to change the status value, there are 3 different settings:



- **disabled**. No automatic replies are sent.
- **alwaysEnabled**. Automatic replies are sent as specified.
- **scheduled**. Automatic replies are sent if between a specific time period.



First, change the method i Graph Explorer to PATCH:


[![image](/uploads/2019/07/image_thumb-3.png)](/uploads/2019/07/image-3.png)



Then you need to supply a request body. This sample is just for enabling automatic replies:



```json
{
    "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#Me/mailboxSettings",
    "automaticRepliesSetting": {
        "status": "alwaysEnabled",
    }
}
```



So paste that body to Graph Explorer and then Run Query:


[![image](/uploads/2019/07/image_thumb-4.png)](/uploads/2019/07/image-4.png)



You should then get a successful response. Likewise you can set the status to “disabled” again, or to “scheduled”. But using scheduled means that you must set some datetime values as well.



## Set Scheduled Automatic Replies



To set scheduled automatic replies, in your request body include the resource types scheduledStartDateTime and scheduledEndDateTime. You can read more about that resource type here, including available time zones: <https://docs.microsoft.com/en-us/graph/api/resources/datetimetimezone?view=graph-rest-1.0>. This is a sample specifying a scheduled automatic replies:



```json
{
    "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#Me/mailboxSettings",
    "automaticRepliesSetting": {
        "status": "scheduled",
        "scheduledStartDateTime": {
            "dateTime": "2019-07-15T08:00:00.0000000",
            "timeZone": "Europe/Berlin"
        },
        "scheduledEndDateTime": {
            "dateTime": "2019-08-09T16:00:00.0000000",
            "timeZone": "Europe/Berlin"
        }
    }
}
```



### Customize internal and external reply messages



The last part is where we put it all together, specifying the following values:



- **internalReplyMessage**: Plain text or HTML formatted message sent to all internal users in your organization as the automatic reply.
- **externalReplyMessage**: Plain text or HTML formatted message sent to all external users as the automatic reply, but depending on this value:
- **externalAudience**: If “none”, no external users will get automatic replies, if “contactsOnly” replies will only be sent to users in your contacts, and if “all” every external user will get a reply.



So this is a working sample of a complete request body:



```json
{
    "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#Me/mailboxSettings",
"automaticRepliesSetting": {
        "status": "scheduled",
        "externalAudience": "contactsOnly",
        "internalReplyMessage": "<html>\n<body>\n<div></div>\n<div>Hi, I'm enjoying summer vacation 2019. I'm back at work August 12th!</div>\n<div><br>\n</div>\n<div>Kindly Regards</div>\n<div>Jan Vidar Elven</div>\n<div></div>\n</body>\n</html>\n",
        "externalReplyMessage": "<html>\n<body>\n<div></div>\n<div>Hi, I'm enjoying summer vacation 2019. I'm back at work August 12th!</div>\n<div><br>\n</div>\n<div>I'll only read e-mails intermittently, and rarely respond before I'm back. Please contact management if anything urgent business needs follow up. Contact info on our website.</div>\n<br>\n</div>\n<div>Kindly Regards</div>\n<div>Jan Vidar Elven</div>\n</div>\n<div></div>\n</body>\n</html>\n",
        "scheduledStartDateTime": {
            "dateTime": "2019-07-15T08:00:00.0000000",
            "timeZone": "Europe/Berlin"
        },
        "scheduledEndDateTime": {
            "dateTime": "2019-08-09T16:00:00.0000000",
            "timeZone": "Europe/Berlin"
        }
    }
}
```



In Graph Explorer:


[![image](/uploads/2019/07/image_thumb-5.png)](/uploads/2019/07/image-5.png)



And I can verify in my Outlook settings:


[![image](/uploads/2019/07/image_thumb-6.png)](/uploads/2019/07/image-6.png)



## Summary and Usage Scenarios



Beside that it is always fun to learn something new about the Microsoft Graph, and automation, the reality is that for many users they will just click to enable or disable automatic replies directly in their Outlook client, both Office Outlook, Outlook Mobile and Outlook on the Web supoorts this. Finding out how to do it with Graph took me just under 2 hours, including writing this blog post. But then again, I learned something new! And I picked up a couple of more tips and tricks on different JSON Request Body constructs ;)



Anyway, in a bigger picture, Graph API is great for customizing, integrating, reporting and automating, so if your organization maybe have create a vacation calendar, you could use the Graph API to automatically enable or disable out of office replies, this is just one example, many more will exist. Please share with me in the comments if you have done or plan to do something with this or similar.


![Smile](/uploads/2019/07/wlemoticon-smile.png)



But first: Summer Vacation 2019! And I’m all set with automatic replies !
