---
title: "Notifying End Users that Incident is Closed When They Reply by Exchange Connector"
date: 2016-03-31T06:21:36Z
draft: false
slug: "notifying-end-users-that-incident-is-closed-when-they-reply-by-exchange-connector"
categories:
  - "Service Manager"
---

A common challenge by using Exchange Connector and Service Manager is that when the Incident is set to status Closed, users still can reply to the Incident Record by using E-mail. Even though the Incident is Read-Only when Closed, it is still possible to create related End User Comments via the Exchange Connector.
While the Exchange Connector cannot be configured in a way that it will not create those End User Comments based on Status, it would be nice to at least inform the user that the Incident is now Closed, and that they must create a new Incident record either via E-mail or the HTML portal.
There have been some solutions to this in the community. Some use different Incident Templates that sets the Incident to Active whenever users reply, and the re-Close them with another template (<https://itblog.no/3192>). Some extends the Incident Work Item Class by adding an UpdatedByEndUser property, and use that to control their notification subscriptions (<http://www.scsm.se/?p=564>).
I have been using another solution for a while at different implementations, and it seems to work fine. So I thought I would write a short blog post on that.

## Overview

My solution will use a periodic notification subscription, targeting the Incident class, and using some criteria that will check that:

- The Incident Status is Closed
  AND
- The End User Comment Entered Date is >= Incident Closed DateAND
- Incident Closed Date >= yyyy-MM-ddThh:mm:ss

I will get more into why I use these criteria later in the post.
In addition to this notification subscription, I also have "normal" subscriptions like sending e-mails to End Users when the Incident is created and resolved, as well as sending e-mails to End User when the Assigned User provides Analysts Comments, and sending e-mails to Assigned User when the End User Comments. I will not get into those here.
So let's start to set this up.

## Creating a New Management Pack

I will create a new Management Pack to store this notification subscription and the e-mail template I will use.
![](/uploads/2016/03/033116_0616_notifyingen1.png)
After creating the Management Pack, I export it and give it a more meaningful ID and file name.
Usually I do this by using search and replace on the generated ID with my own ID name as shown below:
![](/uploads/2016/03/033116_0616_notifyingen2.png)
After, save the MP as SkillSCSM.NotifyClosedIncident.xml, and delete the original MP and re-import this one.

## Closed Incident E-Mail Notification Template

Next I will create the E-Mail Notification Template that will be used by the subscription to notify end users that the Incident is Closed and instruct them to create a new Incident.
This Notification Template will target the Incident Class, and I will use my new MP:
![](/uploads/2016/03/033116_0616_notifyingen3.png)
I specify a subject and HTML body:
![](/uploads/2016/03/033116_0616_notifyingen4.png)
After this I am ready to start creating the subscription.

## Notification Subscription for End User Comments on Closed Incidents

I will create the Notification Subscription by specifying to "Periodically notify when object meet a criteria" and target the class to Incident.
By using this periodic subscription, there are some risks, that I will mitigate with my criteria. The risks are that this will backtrack and fire for all old incidents from before the subscription was created, and that changes to the criteria later could mean that it will send out notifications once more to users that already have received it. But, as long as the criteria is defined correctly, this should not be a problem.
![](/uploads/2016/03/033116_0616_notifyingen5.png)
When specifying criteria, there are something I cannot achieve with the wizard and have to do in the XML later.
For now, you would have to add these criteria via the wizard:

- [Incident] Status equals Closed
  AND
- [Trouble Ticket] Closed Date greater than or equal to (your date today)
  AND
- Has User Comment [Work Item Comments Log] Entered date greater than or equal to (your date today)

For testing purposes, you could also add criteria for ID so that you set it to a fixed Incident ID while you are testing.
Later, in the XML I will change one of the criteria so that: Has User Comment Entered date >= Trouble Ticket Closed Date.
I will select to Notify once:
![](/uploads/2016/03/033116_0616_notifyingen7.png)
Specify my E-Mail Notification Template:
![](/uploads/2016/03/033116_0616_notifyingen8.png)
![](/uploads/2016/03/033116_0616_notifyingen9.png)
Finish and Create.

## Editing the Management Pack XML

Exporting my MP XML I now can see the following criteria in the image below:

- First, Status are set to Equal the Enumeration GUID for Closed
- The second and third expressions are the ClosedDate and Comment EnteredDate, which are set to static. I will change these to evaluate to each other in the next step
- The fourth expression is just for testing, as I have specified a single Incident ID, this I will remove later.

![](/uploads/2016/03/033116_0616_notifyingen10.png)
In the XML, edit the 3rd expression, to an expression like this. I want the EnteredDate for the End User Comment to be later (GreaterEqual) than the Incident ClosedDate. Note also that I keep the manual ClosedDate to today's date. This is because I don't want this rule to affect old Incidents, as when I import this MP, all incidents will be evaluated!
![](/uploads/2016/03/033116_0616_notifyingen11.png)
After this change, I can reimport the MP XML, and wait for it to start processing.

## Verifying and Testing

At the Administration Pane in Service Manager Console, under Workflows and Status, I can find the workflow in question. I can see that it has triggered for an Incident where there has been an End User Comment on the Closed Incident:
![](/uploads/2016/03/033116_0616_notifyingen12.png)
The Affected User gets this email:
![](/uploads/2016/03/033116_0616_notifyingen13.png)
Let's try to reply once more with an End User Comment by replying to this email again. From the History I can see that after the Incident was closed, there are two End User Comments. But the Notification will only occur once per Incident. So after the first time I send emails with End User Comments to the Closed Incident, I will get only one notification.
![](/uploads/2016/03/033116_0616_notifyingen14.png)

## Setting the solution from Test to Production

The next step is to set this solution into production. In my XML I had a criteria for just one Incident ID:
![](/uploads/2016/03/033116_0616_notifyingen15.png)
I will remove that now and re-import the XML MP. On the other hand, I will keep the fixed ClosedDate expression. The reason is of course to not send notifications for old Incidents that have had comments after their closed dates.
![](/uploads/2016/03/033116_0616_notifyingen16.png)
To summarize, my criteria expressions will be:

- Status Equal Closed (Enum GUID)
- ClosedDate GreaterEqual (Date) (This Fixed Date should be the date you import the Management Pack, and updated every time you do maintenance on the MP XML)
- (Comment) EnteredDate GreaterEqual (TroubleTicket) ClosedDate

## Maintenance and important things to note

There are some situations that are important to note with this solution. As this is a periodic notification subscription, with an "only once" recurrence, Service Manager will keep track of which Incidents for which the workflow engine sends Closed Incident notifications based on the criteria defined.
But there is an important exception to be aware of:

- Changing and re-importing the MP XML. When you do that you risk that all subscriptions will run again. Therefore, remember to update the Fixed Date criteria, so that older Incidents that are closed are not sending out notifications to the users that have commented.

For example, changing my MP XML above resulted in a second notification to the end user:
![](/uploads/2016/03/033116_0616_notifyingen17.png)
Editing the Notification Subscription must now be done in XML from now on. Trying to edit it in the Console will result in a greyed out dialog:
![](/uploads/2016/03/033116_0616_notifyingen18.png)
To summarize, I now have a solution for sending out e-mails to End Users that send comments to Incidents after it is Closed. They will only get that notification once, not every time they comment on Closed Incidents.
Thanks for reading, hope it has been helpful!
