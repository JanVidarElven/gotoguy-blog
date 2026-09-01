---
title: "Blog Series - Power'ing up your Home Office Lights: Part 5 - Using Power Automate Flow to Get Access Token and Config"
date: 2020-12-06T22:08:50Z
draft: false
slug: "blog-series-powering-up-your-home-office-lights-part-5-using-power-automate-flow-to-get-access-token-and-config"
tags:
  - "Microsoft Lists"
categories:
  - "Logic Apps"
  - "Microsoft Flow"
  - "Philips Hue"
  - "Power Automate"
  - "PowerApps"
---

This blog post is part of the Blog Series: Power'ing up your Home Office Lights with Power Platform. See introduction post for links to the other articles in the series:  
[[https://gotoguy.blog/2020/12/02/blog-series---powering-up-your-home-office-lights-using-power-platform---introduction/](https://gotoguy.blog/2020/12/02/blog-series-powering-up-your-home-office-lights-using-power-platform-introduction)](https://gotoguy.blog/2020/12/02/blog-series---powering-up-your-home-office-lights-using-power-platform---introduction/)



In previous parts we have built the logic for authorizing and getting Bearer Token for Hue Remote API, and storing that as a Secret in Azure Key Vault, now it's time to move over to the user side of things. In this part we will build a Power Automate Flow that retreives the Access Token and checks if the user has been set up for configuration. Here is a short video where I walk through that Flow:


https://youtu.be/at\_AarpccPI



## Setting up a User State & Config Source



As the PowerApp and Flows we will build are stateless, in the sense it will get data from configured variables and data connections, we need to store some user state and configuration somewhere. The Hue Remote API require that we need to register a so called "whitelist identifer", a username to be used when sending request to the Hue Remote API, for example: https://api.meethue.com/bridge/<whitelist\_identifier>/lights



The way I have built the solution is that the Authorization part, getting, retreiving and if needed refreshing the Bearer Token, are done in the Logic Apps layer, and common for every user that uses the Power Platform solution. On the user side of things, I want every user that share the solution to have their own whitelist identifier.



This means that first time a user use the solution, the user must register their device and retreive the username to be used as the whitelist identifier. Subsequently users will use their own identifer when calling the Hue Remote API.



So we need something set up to store this information about users' states and configuration, and I have chosen to use a SharePoint List/Microsoft List to do this. This List has been created in a Team where the users of the solution are members.



These are the steps I have done to set it up:



1. Created a new Team in Microsoft Teams. I've named my Team "Elven Hue Lights"
2. Created a new SharePoint List/Microsoft List in that Team. You can either to this directly in the Team by adding Microsofts Lists to a Tab, and select to create a new List from Blank, or open Lists from the Office 365 launcher. I created a List like this:


[![](/uploads/2020/12/image-79.png?w=1024)](/uploads/2020/12/image-79.png)



3. Then, in addition to the Title column, add the following columns, single line of text, for storing "Whitelist Identifier" and "Device Type":


[![](/uploads/2020/12/image-81.png?w=934)](/uploads/2020/12/image-81.png)



This list will be used by the following Power Automate Flow, so that is the next step to set up.



## Create the Flow for Hue Access Token and Config



Create the following Power Automate Flow, of type Instant and using PowerApps as trigger, and using the name "Hue - Get Access Token and Config":


[![](/uploads/2020/12/image-83.png?w=1024)](/uploads/2020/12/image-83.png)



After the Trigger action for PowerApps, add a HTTP action. This action will send a GET request to the Logic App we created in the previous part "logicapp-hue-get-accesstoken". So paste the Request Url for that Logic App in the URI field below:


[![](/uploads/2020/12/image-85.png?w=934)](/uploads/2020/12/image-85.png)



After getting the Access Token from the Logic App, add an Initialize variable to get the calling users Displayname via the triggerOutputs header and x-ms-user-name value:


[![](/uploads/2020/12/image-87.png?w=917)](/uploads/2020/12/image-87.png)



Next, add a Get Item action from SharePoint, this will retreive any items matching the User Display Name from the List we created for Hue Users. Specify the correct Site Address and List Name, and add a Filter query where Title equals the variable of the User Display Name we got in the previous step:


[![](/uploads/2020/12/image-89.png?w=939)](/uploads/2020/12/image-89.png)



Next, add a Condition action, where we will evaluate the returned statusCode from the Logic App. This will be either 204 (No Content) or 200 (OK), as we configured back in the Logic App:


[![](/uploads/2020/12/image-91.png?w=938)](/uploads/2020/12/image-91.png)



If Yes, add a Response action, this will return a JSON response object back to the PowerApp, but in this case it will be empty:


[![](/uploads/2020/12/image-93.png?w=977)](/uploads/2020/12/image-93.png)



A quick comment on the above Response body, which will be clearer later in the Flow. I've prepared a structured response that will possibly return not only the access\_token, but also the name (Hue Bridge), and the Bridge IP address, API version etc. But for now, this is empty data.



Let's move over to the No side of the Condition. Inside "If no", add another Condition, and name it "If Username is Empty". This condition should apply if the Get Item action from the List returns no matching user for the display name:


[![](/uploads/2020/12/image-95.png?w=1024)](/uploads/2020/12/image-95.png)



I'm using an expression `empty(body('Get_My_Hue_User')?['value'])` and if that is equal to the expression `true`.



Under "If yes", meaning that the Get Item returns empty results, add another Response action like the following:


[![](/uploads/2020/12/image-98.png?w=905)](/uploads/2020/12/image-98.png)



In the above case, as we don't have a matching user configuration stored, we can return the JSON object with only the access\_token.



Next, under "If no", meaning that a matching user was found in the List, add a HTTP action. This action will call the https://api.meethue.com/bridge/<whitelistidentifier>/config, getting the configuration of the Hue Bridge, and using the access\_token as Bearer Token in the Authorization Header:


[![](/uploads/2020/12/image-99.png?w=974)](/uploads/2020/12/image-99.png)



Note! Even though the Get Item action that is filtered for the user display name, in reality will return only one item (or empty), it is still returned as an array of results. So I'm using the expression and function "first" to return only the first item as a single item. So to get the Whitelist Identifier the expression to be used is:



`first(body('Get_My_Hue_User')?['Value'])?['WhitelistIdentifier']`



After this action, add another Response action, this time returning values for all config values in my custom JSON object:


[![](/uploads/2020/12/image-101.png?w=927)](/uploads/2020/12/image-101.png)



Ok, quite a few custom expressions used above, so for your convenience I'll list them here:



`body('Get_Hue_Access_Token')?['access_token']  
body('Get_Config_Existing')?['name']  
body('Get_Config_Existing')?['ipaddress']  
body('Get_Config_Existing')?['apiversion']  
body('Get_Config_Existing')?['internetservices/internet']  
body('Get_Config_Existing')?['internetservices/remoteaccess']  
first(body('Get_My_Hue_User')?['Value'])?['WhitelistIdentifier']  
first(body('Get_My_Hue_User')?['Value'])?['DeviceType']`



That should be this Flow complete.



## Test and Validate Flow



We can now validate the Flow using a simple test run. Save the Flow and click on the Test button and "I'll perform the trigger action". This should now complete successfully:


[![](/uploads/2020/12/image-104.png?w=1024)](/uploads/2020/12/image-104.png)



As expected the username should be returned as empty as we haven't yet configured the user for Hue Remote API. So the Flow will return access\_token only:


[![](/uploads/2020/12/image-105.png?w=1024)](/uploads/2020/12/image-105.png)



## Summary and Next Steps



This Flow will be central later and used on every PowerApp launch to retrieve the access\_token and configuration from the Hue Bridge. But first we need to build the Flow for linking User configuration and Whitelist Identifier. That will be in the next part!



Thanks for reading this far, see you in the next part of this blog series.
