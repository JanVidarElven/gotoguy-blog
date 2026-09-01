---
title: "Blog Series - Power'ing up your Home Office Lights: Part 3 - Using Logic Apps to Authorize and Get Access Token using Oauth and Hue Remote API"
date: 2020-12-04T11:15:45Z
draft: false
slug: "blog-series-powering-up-your-home-office-lights-part-3-using-logic-apps-to-authorize-and-get-access-token-using-oauth-and-hue-remote-api"
tags:
  - "Logic App"
  - "OAuth2"
  - "OpenID Connect"
categories:
  - "Azure AD"
  - "Logic Apps"
  - "Philips Hue"
  - "Smart House"
---

This blog post is part of the Blog Series: Power'ing up your Home Office Lights with Power Platform. See introduction post for links to the other articles in the series:  
[[https://gotoguy.blog/2020/12/02/blog-series---powering-up-your-home-office-lights-using-power-platform---introduction/](https://gotoguy.blog/2020/12/02/blog-series-powering-up-your-home-office-lights-using-power-platform-introduction)](https://gotoguy.blog/2020/12/02/blog-series---powering-up-your-home-office-lights-using-power-platform---introduction/)



Now that we have registered the application for Hue Remote API, and stored the client Id and Secret in Azure Key Vault, we can start build the Logic App that will authorize and get access token via Oauth2.



Here is a short video where I introduce the concept:


https://youtu.be/HkNEDpw9GVc



## Create the Logic App and HTTP Trigger



The first thing you need to do, is to create a new Logic App in your Azure subscription. Select the Resource Group you have contributor access to, and give the Logic App a suitable name, as per your naming guidelines:


[![](/uploads/2020/12/image-9.png?w=719)](/uploads/2020/12/image-9.png)



Next, select HTTP request to be the trigger for the Logic App:


[![](/uploads/2020/12/image-10.png?w=873)](/uploads/2020/12/image-10.png)



After that you will see the following in the Logic App designer:


[![](/uploads/2020/12/image-11.png?w=637)](/uploads/2020/12/image-11.png)



Make sure you hit Save on the Logic App before the next step. You will now be shown the URL, but first go down to the "Add new parameter" and select Method and GET for method. This way your Logic App will trigger on HTTP GET requests, which is required for the Authorization Code flow with Hue:


[![](/uploads/2020/12/image-12.png?w=640)](/uploads/2020/12/image-12.png)



Now copy this URL, and make sure that no one but you can access this URL, as this is a SAS (Shared Access Signature) URL that anyone in the world can send requests to if they know the URL. Save the Logic App.



Go back to your App Registration in the Hue Developers Portal, and change your temporary http://localhost/logicapp Callback URL to your Logic App URL:


[![](/uploads/2020/12/image-13.png?w=661)](/uploads/2020/12/image-13.png)



This means that from now on, the Logic App will handle the authorization code for the Hue App. But first we will need to let the Logic App access the Key Vault.



## Adding Logic App Identity and Key Vault Access



For the Logic App, under Settings and Identity, set system assigned managed identity to On:


[![](/uploads/2020/12/image-14.png?w=522)](/uploads/2020/12/image-14.png)



After this setting is saved, you can later see the status and the object id of the service principal.


[![](/uploads/2020/12/image-15.png?w=1024)](/uploads/2020/12/image-15.png)



Next, under your Key Vault, click on Access Policies and Add Access Policy, from there selec the Get, Set and List Secret Management operations, and for principal search for and add the Logic App. This should look like this after adding:


[![](/uploads/2020/12/kv-access-1.png?w=947)](/uploads/2020/12/kv-access-1.png)



With permissions in place, we are now ready to add actions to the Logic App.



## Add Actions for getting Access Token



The first ting we need to do is to get the authorization code after the Hue App registration redirects back to the callback URL. This is returned as a querystring appended to the URL. Add a "Compose" action and use the following expression for getting the request queries:


[![](/uploads/2020/12/image-16.png?w=620)](/uploads/2020/12/image-16.png)



(I've added the custom expression to comments for better visibility).



Then we need to get the Client Id and Secret from the Kay Vault. Add a HTTP action next, where we will use the Azure Rest API for getting the secret, and authenticate with the Managed Service Identity:


[![](/uploads/2020/12/image-17.png?w=625)](/uploads/2020/12/image-17.png)



The URI above points to my Azure Key Vault URI, and the specified secret. The documentation for getting secrets can be seen here: [Get Secret - Get Secret (Azure Key Vault) | Microsoft Docs](https://docs.microsoft.com/en-us/rest/api/keyvault/getsecret/getsecret?WT.mc_id=AZ-MVP-5001872).



The same applies to getting the Client Secret, add another HTTP action:


[![](/uploads/2020/12/image-18.png?w=618)](/uploads/2020/12/image-18.png)



The get an access token from Hue Remote API we must either use Basic Authentication or Digest Authentication. Since I'm running this as a Logic App in a controlled environment and trusting the SSL encryption I will use Basic Authentication. In addition, I will secure the outputs from getting Client Id and Secret from Key Vault, so that other users cannot see those values from the run history:


[![](/uploads/2020/12/image-19.png?w=722)](/uploads/2020/12/image-19.png)



This setting has been enabled for both the actions getting KV Secret Client Id and Client Secret:


[![](/uploads/2020/12/image-20.png?w=616)](/uploads/2020/12/image-20.png)



For obtaining an Access Token with Basic Authentication the following header is required: **Authorization: Basic <base64(clientid:clientsecret)>**



This means that we need to base64 encode the clientid + ":" + clientsecret. This can be done using this lengthy expression, here in a "initialize variable" action:


[![](/uploads/2020/12/image-21.png?w=629)](/uploads/2020/12/image-21.png)



This above action is just for reference though, as the HTTP action supports base64 encoding out of the box. So when posting to the token endpoint, the best way is to use the following:


[![](/uploads/2020/12/image-22.png?w=627)](/uploads/2020/12/image-22.png)



*(PS! Another way to do Basic Authentication in a HTTP action would be to add the Authorization header manually in the Action above with: "Basic <your calculated base64>" as value, and leaving the Authentication type to None.)*



From the above settings, in the URI add the authorization code we got from the request queries earlier, using the expression:



`outputs('Compose_Authorization_Code')?['code']`



When selecting Authentication type to Basic, the username (client id) and password (secret) will automatically be base64 encoded. The values for username and password are the valies from the Get KV Secret Client actions earlier, in the following format:



`body('Get_KV_Secret_Client_Id')?['value']`



And this action will return the Bearer Token from Hue Remote API if everything is correctly inputted.



I also make sure that the output of this action is secured from viewing:


[![](/uploads/2020/12/image-23.png?w=617)](/uploads/2020/12/image-23.png)



With the Bearer Token now retrieved, the next actions is to calculate the expiry time and write the Token back to the Key Vault secret.



## Add Actions for getting expiry time and write Token to Key Vault



The Bearer Token returned by Hue Remote API will be in the format of the following masked response:


[![](/uploads/2020/12/image-24.png?w=393)](/uploads/2020/12/image-24.png)



The \_expires\_in values are in seconds, so that means that the Access Token is valid for 7 days, and the Refresh Token about 112 days. It would then make sense to only refresh the token when needed.



Lets start by calculating when the access\_token expires, with the following expression in a Compose action:


[![](/uploads/2020/12/image-27.png?w=625)](/uploads/2020/12/image-27.png)



`addSeconds(utcNow(), int(body('Post_Auth_Code_with_Basic_Auth_to_Get_Access_Token')?['access_token_expires_in']))`



The above expression takes the current time and add the number of seconds for when the access token expires.



This will return a new datetime 7 days ahead. This value will be used to set the expiry time on the Key Vault secret for Bearer Token. By setting an expiry time I can later calculate if I need to refresh the Access Token or not.



But it's not that easy.. The calculated time above will need to be converted to Epoch (32-bit "Unix") integer format to be able to set the Key Vault secret "exp" attribute. This isn't so clear when seeing the API docs, [Set Secret - Set Secret (Azure Key Vault) | Microsoft Docs](https://docs.microsoft.com/en-us/rest/api/keyvault/setsecret/setsecret#secretattributes?WT.mc_id=AZ-MVP-5001872), so took me a little trial and error. And I found great help in this blog article: <https://devkimchi.com/2018/11/04/converting-tick-or-epoch-to-timestamp-in-logic-app/>.



Based on this I need to convert the timestamp to Ticks (64-bit). Ticks is a built in function in Logic Apps, but to be able to convert to Epoch I will need to calculate the difference in ticks between when the Access Token expire, and the first value of Epoch which is `1970-01-01T00:00:00Z`. This is well explained in the above reference blog, but here are my resulting actions.



After calculating the Access Token expiry, I add a compose action which converts this to Ticks:


[![](/uploads/2020/12/image-28.png?w=629)](/uploads/2020/12/image-28.png)



Using the following expression: `ticks(outputs('AccessToken_Expires_Utc'))`



Then I need to find the `1970-01-01T00:00:00Z` value in Ticks:


[![](/uploads/2020/12/image-29.png?w=621)](/uploads/2020/12/image-29.png)


[![](/uploads/2020/12/image-29.png?w=621)](/uploads/2020/12/image-29.png)



Using this expression: `ticks('1970-01-01T00:00:00Z')`



Then we can convert this to Epoch by subtracting the two Ticks values calculated above, and divide by 1 million:


[![](/uploads/2020/12/image-30.png?w=693)](/uploads/2020/12/image-30.png)



This is the expression used above: `div(sub(outputs('GetTimestampInTicks'), outputs('Get1970TimestampInTicks')), 10000000)`



We now have the correct format for the "exp" attribute to update the Key Vault secret. Add a new HTTP action and configure like below:


[![](/uploads/2020/12/image-31.png?w=630)](/uploads/2020/12/image-31.png)



Remember to secure the Output for this action also:


[![](/uploads/2020/12/image-32.png?w=627)](/uploads/2020/12/image-32.png)



Finally we can finish this Logic App by adding a Response action and do a quick test to verify that everything works as expected.



## Adding Response action and verify Logic App



Add a Response action with status code 200 and a body like below:


[![](/uploads/2020/12/image-26.png?w=1024)](/uploads/2020/12/image-26.png)



Tips: It can be difficult to troubleshoot the Logic App when securing outputs, so you might hold back in that when testing. It will show your secrets in the run history though, so it might be best to do this in a test enviroment depending on your needs.



Now we can test. Construct the URL for authorizing the App again, like we did in Part 1:



https://api.meethue.com/oauth2/auth?clientid=&response\_type=code&state=elvenanystring&appid=elven\_demo\_hue\_app&deviceid=elven\_demo&devicename=Elven Demo



Paste it in the Browser, and after granting access to the App in Hue Developer portal:


[![](/uploads/2020/12/image-33.png?w=952)](/uploads/2020/12/image-33.png)



You should be redirected to the Logic App:


[![](/uploads/2020/12/image-34.png?w=1024)](/uploads/2020/12/image-34.png)



.. and with a respons success!



Looking at the Run history, we can verify the steps were successful:


[![](/uploads/2020/12/image-36.png?w=663)](/uploads/2020/12/image-36.png)



You can also look into the inputs and outputs of the actions, except the actions where we secured the output:


[![](/uploads/2020/12/image-37.png?w=642)](/uploads/2020/12/image-37.png)



We can also verify that the Key Vault secret storing the Bearer Token has been updated and have an Expiration Date one week forward:


[![](/uploads/2020/12/image-38.png?w=1024)](/uploads/2020/12/image-38.png)



## Summary and next steps



That concludes this blog post. Thanks for reading this far, in the next part we will build the Logic App that will respond back the Access Token and renew using Refresh Token if needed.
