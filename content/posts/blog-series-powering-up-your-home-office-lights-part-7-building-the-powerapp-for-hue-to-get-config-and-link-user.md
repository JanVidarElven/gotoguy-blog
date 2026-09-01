---
title: "Blog Series - Power'ing up your Home Office Lights: Part 7 - Building the PowerApp for Hue to Get Config and Link user"
date: 2020-12-08T20:45:26Z
draft: false
slug: "blog-series-powering-up-your-home-office-lights-part-7-building-the-powerapp-for-hue-to-get-config-and-link-user"
categories:
  - "Microsoft Flow"
  - "OAuth2"
  - "Philips Hue"
  - "Power Automate"
  - "PowerApps"
---

This blog post is part of the Blog Series: Power'ing up your Home Office Lights with Power Platform. See introduction post for links to the other articles in the series:  
[[https://gotoguy.blog/2020/12/02/blog-series---powering-up-your-home-office-lights-using-power-platform---introduction/](https://gotoguy.blog/2020/12/02/blog-series-powering-up-your-home-office-lights-using-power-platform-introduction)](https://gotoguy.blog/2020/12/02/blog-series---powering-up-your-home-office-lights-using-power-platform---introduction/)



With the Power Automate Flows we've built in the previous parts, we should now be able to get the Link and Whitelist the user and get the Hue Bridge Configuration details. It is time to build the main screen of the "Hue PowerApp"!


[![](/uploads/2020/12/image-139.png?w=1024)](/uploads/2020/12/image-139.png)



Here is a short video where I talk about the basics of the main screen of the PowerApp we are going to build:


https://youtu.be/QybfBE2\_nWU



## Building the PowerApp and Main Screen



In my solution I wanted to build a canvas app with a phone layout, to be able to use it when on my mobile as well. Start by logging in to [make.powerapps.com](https://make.powerapps.com), and creating a new app from Blank, and either phone or tablet layout by your preference:


[![](/uploads/2020/12/image-141.png?w=437)](/uploads/2020/12/image-141.png)



This next step is up to your preference and personal choice, but what I did was the following:



- Added a custom background color from your palette (if you have a branding profile) or you could choose one of the built-in themes:


[![](/uploads/2020/12/image-145.png?w=410)](/uploads/2020/12/image-145.png)



- Add a Header logo
- Add elements like frames and icons. I often use a Label control and set the border for it to create a frame like figure.
- Add label controls for your text and placeholders for where you will update values later. Set font colors for labels and labels where you will have values.
- Add some Images for where you want to add an action to the OnSelect event.
- Add Button controls or Icons for navigating between screens.
- Use a naming convenvtion for your controls.



In the end, adding and formatting all controls, and before I add any data to the PowerApp, my Hue PowerApp ends up like this:


[![](/uploads/2020/12/2020-12-08_16-35-42.png?w=1024)](/uploads/2020/12/2020-12-08_16-35-42.png)



I've uploaded Images for the Authorization and Linking, for your convenience I've attached those here:


[![](/uploads/2020/12/philips_hue_logo_connect_oauth.png?w=1024)](/uploads/2020/12/philips_hue_logo_connect_oauth.png)


[![](/uploads/2020/12/huelinkbutton.png?w=1024)](/uploads/2020/12/huelinkbutton.png)



After finishing the PowerApp main screen design, we can proceed to adding actions and getting data.



## Connecting the PowerApp to Power Automate Flows



Start by selecting the Refresh Icon, on the Action menu, click the On Select button to change to the OnSelect event, and click the Power Automate button:


[![](/uploads/2020/12/image-147.png?w=1024)](/uploads/2020/12/image-147.png)



Under Data, select to associate the "Hue - Get Access Token and Config" Flow:


[![](/uploads/2020/12/image-149.png?w=412)](/uploads/2020/12/image-149.png)



This will start populating the OnSelect event field, which you would edit so that you use the "Se"t function and save the response from calling the Flow in the variable HueResponse like this: `Set(HueResponse,'Hue-GetAccessTokenandConfig'.Run())`


[![](/uploads/2020/12/image-151.png?w=909)](/uploads/2020/12/image-151.png)



Lets test this action. Before this I have removed my user from the Microsoft List "Elven Hue Users", this list is empty now:


[![](/uploads/2020/12/image-154.png?w=864)](/uploads/2020/12/image-154.png)



Hold down the "ALT" button on your keyboard, and click on the Refresh icon. The Flow will now run, you will see the small dots flying over the screen, but you won't see any data yet. But you can check the contents of the "HueResponse" variable. Do this by going to the View menu, and click on the "Variables" button. From there you should see the HueResponse variable, it is of type "Record" and you can click on that Record icon:


[![](/uploads/2020/12/image-155.png?w=532)](/uploads/2020/12/image-155.png)



You should now see something like the following values, if I hadn't deleted the username from my List earlier I would see values for all these fields:


[![](/uploads/2020/12/image-157.png?w=958)](/uploads/2020/12/image-157.png)



If I compare this with the response output from the Flow I triggered with the refresh icon above, I can see that the output really reflects the contents of the "HueResponse" variable:


[![](/uploads/2020/12/image-159.png?w=645)](/uploads/2020/12/image-159.png)



Lets add these values to the labels I prepared in the PowerApp.



For the label containing the Hue name value, add the following to the Text property: `If(HueResponse.access_token="","Hue not Connected!",If(HueResponse.username="","Connection to Hue OK, but User not linked!",HueResponse.name))`



This should return something like this:


[![](/uploads/2020/12/image-161.png?w=1024)](/uploads/2020/12/image-161.png)



Proceed to add the following to the Text property for each of the remaining configuration value labels:



`HueResponse.ipaddress  
HueResponse.apiversion  
HueResponse.internet  
HueResponse.remoteaccess  
HueResponse.devicetype`



They won't show any value in the PowerApp yet though. First we need to get the user registered at the Hue Remote API, which is the next step. Select the following image:


[![](/uploads/2020/12/image-163.png?w=499)](/uploads/2020/12/image-163.png)



On the Action menu, for the OnSelect event, add the Power Automate Flow for Link and Whitelist User. Change the OnSelect event so that also this is using "Set" function and taking the response from the Flow to the same HueResponse variable, but you also need to supply an input to this flow. For this we will use the HueResponse.access\_token, so your OnSelect event should look like this:



`Set(HueResponse, 'Hue-LinkandWhitelistUser'.Run(HueResponse.access_token))`


[![](/uploads/2020/12/image-165.png?w=931)](/uploads/2020/12/image-165.png)



Lets test this button. Hold down "ALT" on your keyboard, and click on the image. The Flow should now run, register a user at Hue Remote API, create a new List item and return the configuration to the PowerApp:


[![](/uploads/2020/12/image-167.png?w=600)](/uploads/2020/12/image-167.png)



Checking the HueResponse record variable now:


[![](/uploads/2020/12/image-169.png?w=1024)](/uploads/2020/12/image-169.png)



A couple of more things remain on the main screen. First, on the App's OnStart event, add the same event as the refresh icon, this would get the config automatically at start:


[![](/uploads/2020/12/image-171.png?w=912)](/uploads/2020/12/image-171.png)



Next, select this Image:


[![](/uploads/2020/12/image-173.png?w=609)](/uploads/2020/12/image-173.png)



On the OnSelect event, add the following:



`Launch("https://api.meethue.com/oauth2/auth?clientid=<your_client_id>&response_type=code&state=<youranystring>&appid=<your_app_id>&deviceid=<your_device_id>&devicename=<your device name>")`



Replace the <your\_...> values with the client id and app id from the Hue Remote API app registration, and your values for device id and name.



Clicking this image will now launch the Hue Developers portal, asking you to Grant permission to the App, and return to the Logic App that retrieves the Bearer Token and store that in the Key Vault as we have seen in previous parts of this blog series.



## Summary and Next Steps



We've now built the foundation and first part of the PowerApp to retreive the configuration, create and link username, and if needed authorizing and getting a new Bearer Token via Hue Remote API if needed.



In the next part we will build the screen for getting lights and setting lights state and color.



Thanks for reading, see you in the next part!
