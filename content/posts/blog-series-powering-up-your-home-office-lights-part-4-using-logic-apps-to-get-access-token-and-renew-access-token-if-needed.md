---
title: "Blog Series - Power'ing up your Home Office Lights: Part 4 - Using Logic Apps to Get Access Token and Renew Access Token if needed"
date: 2020-12-05T16:00:50Z
draft: false
slug: "blog-series-powering-up-your-home-office-lights-part-4-using-logic-apps-to-get-access-token-and-renew-access-token-if-needed"
tags:
  - "Key Vault"
  - "OAuth2"
categories:
  - "Logic Apps"
  - "Philips Hue"
---

This blog post is part of the Blog Series: Power'ing up your Home Office Lights with Power Platform. See introduction post for links to the other articles in the series:  
[[https://gotoguy.blog/2020/12/02/blog-series---powering-up-your-home-office-lights-using-power-platform---introduction/](https://gotoguy.blog/2020/12/02/blog-series-powering-up-your-home-office-lights-using-power-platform-introduction)](https://gotoguy.blog/2020/12/02/blog-series---powering-up-your-home-office-lights-using-power-platform---introduction/)



After building the Logic App in part 3 that will authorize and get access token via Oauth2, we will now create another Logic App that will retrieve the Bearer Token from the Key Vault secret, and renew the Token using Refresh Token whenever it is expired.



Here is a short video where I walk through that Logic App scenario:


https://youtu.be/zpqw1TAGh1w



## Create the Logic App and HTTP Trigger



The first thing you need to do, is to create a new Logic App in your Azure subscription. Select the Resource Group you have contributor access to, and give the Logic App a suitable name, as per your naming guidelines. This is the Logic App I created in my environment:


[![](/uploads/2020/12/image-39.png?w=1024)](/uploads/2020/12/image-39.png)



Add a HTTP request trigger for this Logic App as well:


[![](/uploads/2020/12/image-10.png?w=873)](/uploads/2020/12/image-10.png)



In the Logic App Designer, make sure you hit Save on the Logic App before the next step. You will now be shown the URL, but first go down to the “Add new parameter” and select Method and GET for method. This way your Logic App will trigger on HTTP GET requests.


[![](/uploads/2020/12/image-41.png?w=944)](/uploads/2020/12/image-41.png)



## Adding Logic App Identity and Key Vault Access



As this Logic App also will request secrets from Key Vault, we will need to add a Managed Service Identity and add that to the Key Vault access policy.



Go to Identity settings, and set the System assigned Identity to On:


[![](/uploads/2020/12/image-43.png?w=1024)](/uploads/2020/12/image-43.png)



Next, go to your Key Vault and under Access policies, add the the newly created Logic App with the following Secret permissions (Get, Set, List):


[![](/uploads/2020/12/kv-access-2.png?w=1024)](/uploads/2020/12/kv-access-2.png)



## Add Actions for Getting or Renewing Bearer Token



The actions in this Logic App will retrieve the Bearer Token from the Key Vault and return the Access Token as a Response. If Token is expired, it will be renewed using the Refresh token.



Start by adding a HTTP request, and get the Secret for the Bearer Token like the following:


[![](/uploads/2020/12/image-45.png?w=931)](/uploads/2020/12/image-45.png)



Next, add a Compose action, getting the outputs from the Get KV Secret Bearer Token action. This secret was stored as a Json Object, but will be returned as a String, so I have used the following custom expression to convert to Json:


[![](/uploads/2020/12/image-47.png?w=975)](/uploads/2020/12/image-47.png)



`json(outputs('Get_KV_Secret_Bearer_Token')?['body/value'])`



Next, add the following Compose actions for getting the timestamps in Ticks, and converting to Epoch. See the previous blog post for explanation of why this is necessary, but we need to do this to be able to calculate wether the secret is expired or not:


[![](/uploads/2020/12/image-49.png?w=1014)](/uploads/2020/12/image-49.png)



For your convenience, I've added the custom expressions as comments to the actions above, or you can copy it from below:



`ticks(utcNow())`



`ticks('1970-01-01T00:00:00Z')`



`div(sub(outputs('GetNowTimeStampInTicks'), outputs('Get1970TimestampInTicks')), 10000000)`



Next, add a Condition action. Here we will check if the expiry date time of the secret is greater than the current calculated timestamp in Epoch:


[![](/uploads/2020/12/image-51.png?w=937)](/uploads/2020/12/image-51.png)



Use the following custom expression for getting the "exp" attribute from Key Vault Secret:



`outputs('Get_KV_Secret_Bearer_Token')?['body/attributes/exp']`



If the secret hasn't expired, we will return the access token as a Response action as shown below. Note that I will only return the access\_token, not the complete Bearer Token stored in the Key Vault secret, as this also contains the refresh\_token. The reasoning behind this is that the calling clients (users from PowerApps/Automate) only need the access\_token.


[![](/uploads/2020/12/image-53.png?w=968)](/uploads/2020/12/image-53.png)



As you see from above, I've built a Json body and schema for the response, and the custom expression returing the value of access\_token is `outputs('Compose_Bearer_Token')?['access_token']`.



On the False side of the Condition, meaning that the Secret is expired, we will have the logic that renews the Bearer Token. First add two HTTP actions, for getting the Client Id and Client Secret from Key Vault:


[![](/uploads/2020/12/image-55.png?w=952)](/uploads/2020/12/image-55.png)



Next, add another HTTP action, using Method POST we will send a request to the oauth2/refresh endpoint at Hue Remote API:


[![](/uploads/2020/12/image-57.png?w=938)](/uploads/2020/12/image-57.png)



The refresh\_token need to be sent in a Request Body, using the expression: `outputs('Compose_Bearer_Token')?['refresh_token']`



Remember to set Content-Type: application/x-www-form-urlencoded. And Authentication Type should be set to Basic, using the retrieved Client Id and Secret from Key Vault as username and password.



Refreshing the Token correctly will return a new Bearer Token. We now need to get and convert the time stamps to Epoch integer, to calulate when the Access Token expires. This is the same process as we used in the Logic App "logicapp-hue-authorize" in part 3 of this blog series. Add 3 new Compose actions like below:


[![](/uploads/2020/12/image-59.png?w=936)](/uploads/2020/12/image-59.png)



For your convenience, here are the custom expressions used for the above actions:



`addSeconds(utcNow(), int(body('Post_Refresh_Code_with_Basic_Auth_to_Update_Access_Token')?['access_token_expires_in']))`



`ticks(outputs('AccessToken_Expires_Utc'))`



`div(sub(outputs('GetTimestampInTicks'), outputs('Get1970TimestampInTicks')), 10000000)`



Next step is to update the Bearer Token Secret in Key Vault with the new Token we received now and the new expiry date. Add a HTTP action like below:


[![](/uploads/2020/12/image-61.png?w=943)](/uploads/2020/12/image-61.png)



We can now return the access\_token using the HTTP action like below:


[![](/uploads/2020/12/image-63.png?w=975)](/uploads/2020/12/image-63.png)



The last action we need to add is a default response if any accest\_token could not be returned. This is important as we are going to call this Logic App using Power Automate Flows, and we need to have a response for any scenario. Add this after the condition action like below:


[![](/uploads/2020/12/image-65.png?w=1024)](/uploads/2020/12/image-65.png)



For the Null Response action, change the Configure run after setting like the following:


[![](/uploads/2020/12/image-67.png?w=925)](/uploads/2020/12/image-67.png)



That should be it. Remember to secure outputs for any actions that return credential information:


[![](/uploads/2020/12/image-70.png?w=1024)](/uploads/2020/12/image-70.png)



## Verify Logic App



We can now test the Logic App. You can use Postman, Invoke-RestMethod in PowerShell, or just run in the Browser your Logic App Http Trigger Url:


[![](/uploads/2020/12/image-73.png?w=890)](/uploads/2020/12/image-73.png)



This should return your Access Token:


[![](/uploads/2020/12/image-75.png?w=755)](/uploads/2020/12/image-75.png)



Looking at the Run History for the Logic App, we should see a sucessful run:


[![](/uploads/2020/12/image-77.png?w=1024)](/uploads/2020/12/image-77.png)



## Summary and Next Steps



That should conclude this blog post. In this post, and the previous, we have built the logic behind authorizing and getting the Bearer Token for Philips Hue Remote API, as well as providing and refresh the Token when needed.



In the next part we are going to start building the solution in Power Automate. Thanks for reading, see you in the next part!
