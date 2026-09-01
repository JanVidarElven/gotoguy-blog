---
title: "Blog Series - Power'ing up your Home Office Lights: Part 1 - Get to know your Hue Remote API and prepare for building your solution"
date: 2020-12-02T13:41:10Z
draft: false
slug: "blog-series-powering-up-your-home-office-lights-part-1-get-to-know-your-hue-remote-api-and-prepare-for-building-your-solution"
tags:
  - "Power Platform"
categories:
  - "Philips Hue"
  - "Power Automate"
  - "PowerApps"
  - "Smart House"
---

This blog post is part of the Blog Series: Power'ing up your Home Office Lights with Power Platform. See introduction post for links to the other articles in the series:  
[https://gotoguy.blog/2020/12/02/blog-series---powering-up-your-home-office-lights-using-power-platform---introduction/](https://gotoguy.blog/2020/12/02/blog-series-powering-up-your-home-office-lights-using-power-platform-introduction)



In this first part I wanted to introduce the requirements and preparations for automating with your Home Lights API. In my case I'm using Philips Hue, as Hue has a well developed API that also can be accessed from remote. And since I'm on the topic of automating with Power Platform, I need to be able to access the API from remote.



In principle, you could use this guide against any light system that has an API, but of course I will show all the examples and config based on Philips Hue in this blog series.



In this blog post I will show you how to set up and be ready for the next parts of this blog series. If you want to dive deeper into understanding the API and testing from remote, I would recommend you read this blog post I published earlier this year about authentication, exploring and controlling using Postman:



[Remote Authentication and Controlling Philips Hue API using Postman | GoToGuy Blog](https://gotoguy.blog/2020/05/21/remote-authentication-and-controlling-philips-hue-api-using-postman/)



Here's a quick video introduction to this articles topic, and below we will cover the necessary overview of how you should prepare for the next parts of the blog series:


https://youtu.be/C2T5tDGYl0c



## Create a New Remote Hue API app



The first thing you need to do after you have created a Hue Developer account, is to create a new Remote Hue API app here: <https://developers.meethue.com/my-apps/>.


![](/uploads/2020/05/image-5.png?w=992)



You need to specify the following required fields:



- App name: A display name for your remote app
- Callback URL: This is needed for the Oauth2 consent and returning an authorization code. It is here where we will specify the HTTP request URL for the Logic App we will create in Part 3 of this blog series. For now, you can just enter some dummy URL like http://localhost/mylogicapp.
- Application description: A short description for your remote app.
- Optionally you can specify contact details.



After submitting your new app is ready, and also an AppId, ClientId and ClientSecret will be provided, for example:


[![](/uploads/2020/12/image-2.png?w=985)](/uploads/2020/12/image-2.png)



As you can see from above image, I've already configured the correct URL for my Logic App, meaning the Callback URL from above will trigger the Logic App below.


[![](/uploads/2020/12/image-4.png?w=877)](/uploads/2020/12/image-4.png)



But as previously mentioned, you can now just specify something like http://localhost/mylogicapp.



## Test if we can successfully get Authorization Code



As explained at [Remote Authentication - Philips Hue Developer Program (meethue.com)](https://developers.meethue.com/develop/hue-api/remote-authentication/), the initial step in the authorization flow is granting permissions for the login user to the resources. This will be done using the following sample request:



```http
GET https://api.meethue.com/oauth2/auth?clientid=<clientid>&appid=<appid>&deviceid=<deviceid>&devicename=<devicename>&state=<state>&response_type=code
```



Using a Demo App Registration,



**ClientId**: J9NckRHRPGAoYppWGtjnNJtriTOo5R4Q



**AppId:** elven\_power\_platform\_demo\_app



lets construct that URL, I've highlighted the parts you need to replace for your environment:



https://api.meethue.com/oauth2/auth?clientid=**J9NckRHRPGAoYppWGtjnNJtriTOo5R4Q**&appid=**elven\_power\_platform\_demo**\_app&deviceid=**elvendemo**&devicename=**ElvenDemoLocal**&state=**anydemostring**&response\_type=code



Now, copy that URL, and paste it into your Browser, and hit Enter.



If you aren't logged in with your Hue Developers account already, you must do so, and after that you will need to accept the following permission grant:


[![](/uploads/2020/12/image-5.png?w=953)](/uploads/2020/12/image-5.png)



Now, if you are using localhost as the callback URL, the following response is perfectly normal:


[![](/uploads/2020/12/image-6.png?w=677)](/uploads/2020/12/image-6.png)



Note the above authorization code, which is returned to the application together with the state string I supplied for verification. This Code, will together with the ClientId and Secret be used for accessing the Token endpoint and getting an Access Token. But that will come later in this series.



## Summary and next steps



We have now prepared the necessary App Registration at Hue Developers portal, and laid the necessary foundations for the next steps in building the logic behind remote authentication.



If you want to explore more about authentication and access tokens, you can do that with the link in the beginning of the blog post using Postman.



Thanks for reading, hope to see you in the next part.
