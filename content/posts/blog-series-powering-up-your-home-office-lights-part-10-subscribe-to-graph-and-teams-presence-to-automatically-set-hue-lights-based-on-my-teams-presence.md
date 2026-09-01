---
title: "Blog Series - Power'ing up your Home Office Lights: Part 10 - Subscribe to Graph and Teams Presence to automatically set Hue Lights based on my Teams Presence!"
date: 2020-12-11T08:58:42Z
draft: false
slug: "blog-series-powering-up-your-home-office-lights-part-10-subscribe-to-graph-and-teams-presence-to-automatically-set-hue-lights-based-on-my-teams-presence"
tags:
  - "OAuth2"
categories:
  - "Microsoft Flow"
  - "Microsoft Graph"
  - "Microsoft Teams"
  - "Philips Hue"
  - "Power Automate"
  - "PowerApps"
---

This blog post is part of the Blog Series: Power'ing up your Home Office Lights with Power Platform. See introduction post for links to the other articles in the series:  
[[https://gotoguy.blog/2020/12/02/blog-series---powering-up-your-home-office-lights-using-power-platform---introduction/](https://gotoguy.blog/2020/12/02/blog-series-powering-up-your-home-office-lights-using-power-platform-introduction)](https://gotoguy.blog/2020/12/02/blog-series---powering-up-your-home-office-lights-using-power-platform---introduction/)



In this last part of the blog series, we will build on the previous blog post where we could get the presence status from Teams to the Hue Power App. Now we will use Microsoft Graph and subscribe to change notifications for presence, so that both the Power App and my Hue Lights will automatically change status based on the presence.



In this blog post I will reuse the Custom Connector I created for managing Microsoft Graph Subscriptions in this previous blog post: [[Managing Microsoft Graph Change Notifications Subscriptions with Power Platform | GoToGuy Blog](https://gotoguy.blog/2020/12/11/managing-microsoft-graph-change-notifications-subscriptions-with-power-platform/)](https://gotoguy.blog/2020/12/11/managing-microsoft-graph-change-notifications-subscriptions-with-power-platform/)



To follow along, you will need at least to create the App Registration and the Custom Connector referred to in that blog post. You can also import the Custom Connector OpenAPI Swagger from this link: <MY GITHUB URL TO HERE>



## Adding the Custom Connector to the PowerApp



In the Hue Power App, go to the View menu, and under Data click to "+ Add data source". Add the MSGraph Subscription Connector as shown below. This way we can refer to this in the Hue Power App.


[![](/uploads/2020/11/image-34.png?w=353)](/uploads/2020/11/image-34.png)



We are going to add the logic to creating the subscription based on this toggle button and the selected light source:


[![](/uploads/2020/11/image-35.png?w=961)](/uploads/2020/11/image-35.png)



But before that we have somethings to prepare first. When creating a Graph Subscription, we will need to prepare a Webhook Url for where Graph will send its notifcations when the Teams presence changes. This will be handled in a Power Automate Flow, so lets create that first.



## Creating the Flow for Graph Notifications and Hue Lights changes



Since I have built this all before, ref. <https://gotoguy.blog/2020/10/24/managing-microsoft-graph-change-notifications-subscriptions-with-power-platform/>, I will make a copy of the "Graph Notification - Presence Change" flow for this use case.


[![](/uploads/2020/11/image-36.png?w=861)](/uploads/2020/11/image-36.png)



If you want to follow along, you will need to follow the instructions in that blog post first. After saving a copy, or if you created a new flow from blank using HTTP request webhook, you will need to copy the HTTP POST URL shown below, as that will be the "notification url" we will refer to later:


[![](/uploads/2020/11/image-37.png?w=907)](/uploads/2020/11/image-37.png)



Next set some value that only you know for the secret client state:


[![](/uploads/2020/11/image-38.png?w=632)](/uploads/2020/11/image-38.png)



The next part of the Flow are used to do a first-time validation of adding the change subscription, with Content-Type text/plain and request query containing a validation token. Microsoft Graph expects a response of status code 200 with the validation token back. If that is returned, Microsoft Graph will successfully create the subscription.


[![](/uploads/2020/11/image-39.png?w=646)](/uploads/2020/11/image-39.png)



For subsequent requests, we must return a 202 Accepted response, and in the next step I parse the notification request body, so that we can look into what change we have been notified for:


[![](/uploads/2020/11/image-40.png?w=652)](/uploads/2020/11/image-40.png)



Following the change notification, we can start looking into the change value. Firstly, I have added a verification of the secret client state I specified earlier, this is prevent misuse of the notification Url if that become known by others or used in the wrong context. After doing a simple test of the client state, where I do nothing if the client state don't match, I can start building the logic behind the changes in presence status:


[![](/uploads/2020/11/image-41.png?w=1024)](/uploads/2020/11/image-41.png)



Inside the Switch Presence Status action, I will based on the availability status change, do a different case for each of the possible Teams Presence status values (see blog series post part 9 for explaining the different presence availability values):


[![](/uploads/2020/11/image-42.png?w=1024)](/uploads/2020/11/image-42.png)



Inside each of these cases I will define the light settings and colors, and after that call the Remote Hue API for setting the light. As you saw in part 8 of this blog series, in order to access the Hue API remotely I will need the following:



- An Access Token to be included as a Bearer token in the Authorization Header
- A username/whitelist identifier
- The actual lightnumber to set the state for
- A request body containing the light state, for example colors, brightness, on/off etc.



Remember, this Flow will be triggered from Microsoft Graph whenever there is a presence state change in Teams. So I need to be able to access/retreive the access token, username and for which lightnumber I created the subscription. This is how I will get it:



- Access Token will be retreived via the Logic App I created in part 4 of the blog series.
- Username/whitelist identifier will be retrieved via the SharePoint List i created in part 6, see below image.
- However, I do need to store the lightnumber I will create the change notification for, and for this I will add a couple more columns in this list:


[![](/uploads/2020/11/image-43.png?w=667)](/uploads/2020/11/image-43.png)



## Customize the Configuration List for storing Subscription Details



I add the following two single-line-of-text columns to my List:



- Subscribe Presence LightNumber. This will be the chosen Hue light I want to change when change notifications occur for Teams presence status.
- Change Notification Subscription Id. This will be the Id I can refer back to when adding and removing the subscription when needed.


[![](/uploads/2020/11/image-44.png?w=1024)](/uploads/2020/11/image-44.png)



## Customize the Flow for getting User Configuration and preparing Light States



Back to the Flow again, we need to add some actions. First, add a initialize variable action after the initialize SecretClientState action like here:


[![](/uploads/2020/11/image-45.png?w=793)](/uploads/2020/11/image-45.png)



I set the type to Object and using the json function to create an empty json object. This variable will later be used for changing the light state.



Next, in the Flow after the "Parse Notification Body" action, add a "Get Items" action from SharePoint connector, and configure it to your site, list name and the following Filter Query:


[![](/uploads/2020/11/image-46.png?w=1024)](/uploads/2020/11/image-46.png)



My filter query:   
`first(body('Parse_Notification_Body')?['value'])?['subscriptionId']`  
will be used to find what username and light that have been set up for presence changes.



Next, lets set the variable for LigthState. Inside each of the Switch Cases, add the action Set Variable, and then set the variable to the chosen xy color code, as a json object like the following. This is for the color green:


[![](/uploads/2020/11/image-47.png?w=641)](/uploads/2020/11/image-47.png)



Do the same for all of the other case, these are the values I have been using:




|  |  |  |
| --- | --- | --- |
| **STATE** | **COLOR** | **JSON VARIABLE** |
| Away | Yellow | json('{ "on": true, "bri": 254, "xy": [ 0.517102, 0.474840 ], "transitiontime": 0 }') |
| Available | Green | json('{ "on": true, "bri": 254, "xy": [ 0.358189, 0.556853 ], "transitiontime": 0 }') |
| AvailableIdle | Green (10% bright) | json('{ "on": true, "bri": 25, "xy": [ 0.358189, 0.556853 ], "transitiontime": 0 }') |
| Busy | Red | json('{ "on": true, "bri": 254, "xy": [ 0.626564, 0.256591 ], "transitiontime": 0 }') |
| BusyIdle | Red (10% bright) | json('{ "on": true, "bri": 25, "xy": [ 0.626564, 0.256591 ], "transitiontime": 0 }') |
| BeRightBack | Yellow | json('{ "on": true, "bri": 254, "xy": [ 0.517102, 0.474840 ], "transitiontime": 0 }') |
| DoNotDisturb | Red | json('{ "on": true, "bri": 254, "xy": [ 0.626564, 0.256591 ], "transitiontime": 0 }') |
| Offline | Grey (10% bright) | json('{ "on": true, "bri": 25, "xy": [ 0.3146, 0.3303 ], "transitiontime": 0 }') |
| PresenceUnknown | White | json('{ "on": true, "bri": 254, "xy": [ 0.3146, 0.3303 ], "transitiontime": 0 }') |




PS! The transitiontime is to get as close to realtime updates as possible. Add the colors similarly for rest of the states:


[![](/uploads/2020/11/image-48.png?w=1024)](/uploads/2020/11/image-48.png)



## Get the Access Token and call Hue Remote API



Now we are ready to get the Access Token, and call the Hue Remote API with the selected light state.



First, add a HTTP action below the Switch Presence Status action, calling the Logic App previously created in part 4 of the blog series:


[![](/uploads/2020/11/image-49.png?w=645)](/uploads/2020/11/image-49.png)



Next, add another HTTP request after, and this will call the Hue Remote API to set the lights:


[![](/uploads/2020/11/image-50.png?w=809)](/uploads/2020/11/image-50.png)



When constructing Hue API URI above, I retreive the whitelist identifier for username with the following expression:



`first(body('Get_My_Hue_User_Subscription')?['Value'])?['WhitelistIdentifier']`



And then which light number with this expression:



`first(body('Get_My_Hue_User_Subscription')?['Value'])?['SubscribePresenceLightNumber']`



That should be the completion of this Flow. Remember to turn it on if needed. We are now ready for the last step.


[![](/uploads/2020/11/image-51.png?w=1024)](/uploads/2020/11/image-51.png)



## Adding the Flow for Creating the Graph Subscription



In the beginning of this blog post I referred to the toggle "Sync Hue Lights with Teams" in the Power App. Now that we have prepared the Flow handling the notification Url, we need to add a new Flow that would handle the creating, or deletion, of Graph Subscriptions. As this is a toggle control, setting it to "On" should create a Graph subscription for the selected lights, and setting it to "Off" should remove that subscription again.



Create a new instant Flow with PowerApps as trigger:


[![](/uploads/2020/11/image-52.png?w=860)](/uploads/2020/11/image-52.png)



Next, add an action for initialize variable for getting the UserDisplayName:


[![](/uploads/2020/11/image-53.png?w=650)](/uploads/2020/11/image-53.png)



Use the following expression for getting the user display name:



`triggerOutputs()['headers']['x-ms-user-name']`



Next, add another initialize variable for getting the light number. After renaming the action, click on "Ask in PowerApps":


[![](/uploads/2020/11/image-54.png?w=866)](/uploads/2020/11/image-54.png)



Add another initialize variable, this time a boolean value, and for getting the value of the toggle sync control:


[![](/uploads/2020/11/image-55.png?w=618)](/uploads/2020/11/image-55.png)



Next, we will retrieve our user config source from the SharePoint list again, this time filtered by the UserDisplayName variable:


[![](/uploads/2020/11/image-56.png?w=624)](/uploads/2020/11/image-56.png)



We now need some logic to the next steps for the flow, lets start by the toogle button which will be either true or false:


[![](/uploads/2020/11/image-58.png?w=635)](/uploads/2020/11/image-58.png)



If yes, that should mean that we either should create a new graph subscription, or update any exisiting ones.



Under Yes, add a new action. This action will call the Custom Connector I created in another blog post (<https://gotoguy.blog/2020/10/24/managing-microsoft-graph-change-notifications-subscriptions-with-power-platform/>). This Custom Connector should have the following actions:


[![](/uploads/2020/11/image-60.png?w=611)](/uploads/2020/11/image-60.png)



Click on the Get Subscription action to add that. For the subscriptionId parameter I will refer to the first returned instance of any exisiting Graph Subscriptions I have in the SharePoint list returned earlier.


[![](/uploads/2020/11/image-59.png?w=762)](/uploads/2020/11/image-59.png)



Here is the expression for your reference:



`first(body('Get_My_Hue_User')?['Value'])?['ChangeNotificationSubscriptionId']`



When running the Flow this action will either:



- Return a 200 OK if the subscription is found, or if the SharePoint List has a blank value for ChangeNotificationSubscriptionId.
- Return a 404 ResourceNotFound if the subscription is not found, this will happen if the subscription is expired. This is an error that will halt the Flow, so we need to handle it.



So lets start by getting the Status Code. I'll do that by adding a compose action with the following expression:



`outputs('Get_Graph_Subscription')['statusCode']`


[![](/uploads/2020/11/image-61.png?w=644)](/uploads/2020/11/image-61.png)



It's also important to set that this action should run even if the Get Graph Subscription action fails:


[![](/uploads/2020/11/image-62.png?w=626)](/uploads/2020/11/image-62.png)



Lets add another condition, where the outputs of the status code should be 200 (OK):


[![](/uploads/2020/11/image-63.png?w=1024)](/uploads/2020/11/image-63.png)



A status code of 200 will either indicate that either we found an existing Graph Subscription matching the configured subscription id from the SharePoint List, or that the list is blank and the Get Graph Subscription will return an empty array or any other Graph Subscriptions you might have. In the first case, we will just update the existing subscription, in the latter case we will create a new subscription. Lets start by adding another compose action:





## Adding the Flow to the Hue Power App



Back in the Hue Power App, we can now link this Flow to the toggle control. With the sync toggle control selected, go to the Action menu, and then click on Power Automate. From there you should see the "Hue - Create Update Remove Graph Subscription" Flow, click to add it. On the OnChange event, add the Run parameters where the lightnumber value is read from the dropdown list and selected items lightnumber, and the toggle button value like this:


[![](/uploads/2020/11/image-57.png?w=1024)](/uploads/2020/11/image-57.png)
