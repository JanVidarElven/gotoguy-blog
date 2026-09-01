---
title: "Exporting and Importing PowerApps and Flows Package that use a Custom Connector"
date: 2018-09-18T23:00:43Z
draft: false
slug: "exporting-and-importing-powerapps-and-flows-package-that-use-a-custom-connector"
categories:
  - "Azure AD"
  - "Azure AD Privileged Identity Management"
  - "Microsoft Flow"
  - "Microsoft Graph"
  - "PowerApps"
---

Just recently I published a blog post on how to use PowerApps and Flow with a custom connector using Microsoft Graph API, to create an app for Azure AD PIM (Privileged Identity Management): [https://gotoguy.blog/2018/09/15/create-your-own-azure-ad-pim-app-with-powerapps-and-flow-using-microsoft-graph/](https://gotoguy.blog/2018/09/15/create-your-own-azure-ad-pim-app-with-powerapps-and-flow-using-microsoft-graph/ "https://gotoguy.blog/2018/09/15/create-your-own-azure-ad-pim-app-with-powerapps-and-flow-using-microsoft-graph/").
In this blog post I want to share some instructions and experiences on exporting the PowerApp and Flows to a package, and how you can export the Custom Connector definitions to a swagger file. After that I will show how you in a new environment can import these definitions, and import the PowerApp and Flow package.
Even better, based on the aforementioned blog post on the Azure AD PIM App, I will provide you with download links for the custom connector swagger defininiton for Microsoft Graph, as well as the PowerApp and Flows Package, so you can start from there without having to build all the stuff yourselves ![Smile](/uploads/2018/09/wlemoticon-smile1.png)!

## Export the PowerApps Package

First, start in your Apps gallery of PowerApps, find the Export package (preview) button as shown below:
[![image](/uploads/2018/09/image_thumb117.png "image")](/uploads/2018/09/image119.png)
Specify a package name, environment and optionally a description as I have below:
[![image](/uploads/2018/09/image_thumb118.png "image")](/uploads/2018/09/image120.png)
Next, review the package content. For the Azure AD PIM App, I’ll change the Import Setup to “Create as new”, the same for the 3 Flows, as shown below:
[![image](/uploads/2018/09/image_thumb119.png "image")](/uploads/2018/09/image121.png)
For some of the resources you can select between Create as new or Update, and as I’m planning to import this as a new App with new Flows in the environment, I’ll change this from the default.
[![image](/uploads/2018/09/image_thumb120.png "image")](/uploads/2018/09/image122.png)
The other resources (like the connector and connections) I will select during import. This means these will have to be already existing in the environment I want to import the package to.
I can then download the package:
[![SNAGHTML9abd28](/uploads/2018/09/snaghtml9abd28_thumb.png "SNAGHTML9abd28")](/uploads/2018/09/snaghtml9abd28.png)
The package is downloaded as a zip file:
[![image](/uploads/2018/09/image_thumb121.png "image")](/uploads/2018/09/image123.png)
Inside the zip file there are some manifest json files and the PowerApps and Flows definitions:
[![image](/uploads/2018/09/image_thumb122.png "image")](/uploads/2018/09/image124.png)

## Export the Custom Connector swagger file

The next thing we want to do is to export the custom connector and its operations. Go to Custom connectors in the menu:
[![image](/uploads/2018/09/image_thumb123.png "image")](/uploads/2018/09/image125.png)
Find the “PowerApps Microsoft Graph” connector, and click on the down arrow as shown below. This will download a swagger definition file in JSON format:
[![SNAGHTMLb16f76](/uploads/2018/09/snaghtmlb16f76_thumb.png "SNAGHTMLb16f76")](/uploads/2018/09/snaghtmlb16f76.png)
You can open and inspect that JSON file in your favorite JSON editor, here is mine shown in Visual Studio Code:
[![image](/uploads/2018/09/image_thumb124.png "image")](/uploads/2018/09/image126.png)

## Community Download

Courtesy of gotoguy.blog, I’ll provide you with a download for both the PowerApps/Flows package, as well as the Custom Connector Swagger JSON file. This is helpful if you want to skip right ahead to the next Import section.
These files are placed at my GitHub, in the following repositories:

- [https://github.com/skillriver/PowerAppsFlowCustomConnector](https://github.com/skillriver/PowerAppsFlowCustomConnector "https://github.com/skillriver/PowerAppsFlowCustomConnector"). Under the folder MicrosoftGraphApi you will find an always updated version of my PowerApps Microsoft Graph custom connector operations. Look to the Readme.md file for details. PS! I will add more operations to this connector later, and the file will be updated.
- [https://github.com/skillriver/PowerAppsFlowPackage](https://github.com/skillriver/PowerAppsFlowPackage "https://github.com/skillriver/PowerAppsFlowCustomConnector"). Under the folder AzureADPIMApp you will find the previously exported PowerApp and Flows for the Azure AD PIM App. See readme.md file for details.

## Import the Custom Connector swagger file

In the new/target environment we will first have to import the swagger file for the Custom Connector. Here you have 2 options:

1. You can create a new custom connector, and Import from an OpenAPI file/URL:
   [![image](/uploads/2018/09/image_thumb125.png "image")](/uploads/2018/09/image127.png)
2. Or, if you already have a Custom Connector for Microsoft Graph, you can select to Update the existing connector from OpenAPI file/URL:
   [![image](/uploads/2018/09/image_thumb126.png "image")](/uploads/2018/09/image128.png)

For sake of education, lets try both variants. The first time you will have to create a new custom connector anyway, but later you will only need to update if there are any changes. I will use OpenAPI URL, as the swagger file is avaiable at my GitHub here: [https://raw.githubusercontent.com/skillriver/PowerAppsFlowCustomConnector/master/MicrosoftGraphApi/PowerApps-Microsoft-Graph.swagger.json](https://raw.githubusercontent.com/skillriver/PowerAppsFlowCustomConnector/master/MicrosoftGraphApi/PowerApps-Microsoft-Graph.swagger.json "https://raw.githubusercontent.com/skillriver/PowerAppsFlowCustomConnector/master/MicrosoftGraphApi/PowerApps-Microsoft-Graph.swagger.json")

### PS! Prerequisite

Remember that to be able to use a Custom Connector and Microsoft Graph, you will have to create or use an App Registration in Azure AD **in your target enviroment**, like I have described in this blog article, under the section “App Registration”: [https://gotoguy.blog/2017/12/17/access-microsoft-graph-api-using-custom-connector-in-powerapps-and-flows/](https://gotoguy.blog/2017/12/17/access-microsoft-graph-api-using-custom-connector-in-powerapps-and-flows/ "https://gotoguy.blog/2017/12/17/access-microsoft-graph-api-using-custom-connector-in-powerapps-and-flows/").
Take a note of the application ID and secret key:
[![image](/uploads/2018/09/image_thumb127.png "image")](/uploads/2018/09/image129.png)
Remember also to give the App the right Microsoft Graph Permissions, and give Admin grant if needed:
[![image](/uploads/2018/09/image_thumb128.png "image")](/uploads/2018/09/image130.png)

### Import from OpenAPI URL

To create a new custom connector, select to import from OpenAPI URL:

1. Type a name for the Custom connector, and paste in the URL for the swagger json file:
   [![image](/uploads/2018/09/image_thumb129.png "image")](/uploads/2018/09/image131.png)
   Verify the URL and click Continue.
2. Following that, verify that host is graph.microsoft.com and base URL is “/”, and optionally specify a connector icon, color and description:
   [![image](/uploads/2018/09/image_thumb130.png "image")](/uploads/2018/09/image132.png)
3. On the security page you have to specify the client id which is the app id from the registered app in your target Azure AD environment, as well as client secret and resource URL:
   [![image](/uploads/2018/09/image_thumb131.png "image")](/uploads/2018/09/image133.png)
   In my target environment I have pasted in the client id, secret, and the resource URL is https://graph.microsoft.com. Note that the Redirect URL is not available before after the custom connector is saved:
   [![image](/uploads/2018/09/image_thumb132.png "image")](/uploads/2018/09/image134.png)
   Click to go to the next Definition page.
4. At the Definition page, the actions are already in place because they were defined in the OpenAPI swagger file:
   [![image](/uploads/2018/09/image_thumb133.png "image")](/uploads/2018/09/image135.png)
   Click “Create connector”.
5. After the Connector is created and saved, go back to Security, and copy the Redirect URL:
   [![image](/uploads/2018/09/image_thumb134.png "image")](/uploads/2018/09/image136.png)
6. Make sure that the Redirect URL is on the list of the Reply URLs of the Azure AD App Registration:
   [![image](/uploads/2018/09/image_thumb135.png "image")](/uploads/2018/09/image137.png)
7. Back in the Custom Connector, lets test the connector. Go to the Test page and create a connection:
   [![image](/uploads/2018/09/image_thumb136.png "image")](/uploads/2018/09/image138.png)
8. After establishing a connection with your user account, you can go ahead and test one or more of the operations and verify that they run successfully:
   [![image](/uploads/2018/09/image_thumb137.png "image")](/uploads/2018/09/image139.png)

After testing this the custom connector is ready to use.

### Update from OpenAPI URL

I you want to update an existing custom connector, select to Update from OpenAPI URL:

1. Provide the URL for the swagger json file:
   [![image](/uploads/2018/09/image_thumb138.png "image")](/uploads/2018/09/image140.png)
2. As with when creating a new custom connector, verify that host is graph.microsoft.com and base URL is “/”, and optionally specify a connector icon, color and description:
   [![image](/uploads/2018/09/image_thumb139.png "image")](/uploads/2018/09/image141.png)
3. When updating an existing connector, you only have to specify the client secret again:
   [![image](/uploads/2018/09/image_thumb140.png "image")](/uploads/2018/09/image142.png)
   If you don’t have the original secret stored securely somewhere, you have to go to the App Registration in Azure AD and generate a new one.
4. Verify that the Operations now has been updated from the imported OpenAPI swagger json file:
   [![image](/uploads/2018/09/image_thumb141.png "image")](/uploads/2018/09/image143.png)
   Click Update Connector to save the changes.
5. After this, go to Test, and either use an existing connection or create a new, and the Test some of the operations to verify:
   [![image](/uploads/2018/09/image_thumb142.png "image")](/uploads/2018/09/image144.png)

Now we are ready import the PowerApp and the Flows that will use this custom connector.

## Import the PowerApps and Flows Package

We can now import the package we exported earlier, or if you want to use the community download from my GitHub repository, make sure that you download the zip package before this next step.
Start by selecting Import package (preview) from the PowerApps menu:
[![image](/uploads/2018/09/image_thumb143.png "image")](/uploads/2018/09/image145.png)
Then browse to the zip packaged to start uploading:
[![image](/uploads/2018/09/image_thumb144.png "image")](/uploads/2018/09/image146.png)
When the upload is complete, we can review the package content. We have to select during import the connector and connections, marked as red under here:
[![image](/uploads/2018/09/image_thumb145.png "image")](/uploads/2018/09/image147.png)
After selecting the custom connector, and changing the connections to the target environment, we are ready to Import:
[![image](/uploads/2018/09/image_thumb146.png "image")](/uploads/2018/09/image148.png)
Note that you also can change the name of the PowerApp and Flows by clicking on the wrench symbol.
Click Import when you are ready, and verify that the import is successful:
[![image](/uploads/2018/09/image_thumb147.png "image")](/uploads/2018/09/image149.png)
You can now proceed to open the app for customizations and testing. If prompted, click to Allow the permission request:
[![image](/uploads/2018/09/image_thumb148.png "image")](/uploads/2018/09/image150.png)
After opening the Azure AD PIM App, now in the target environment, hold down the ALT key and click Refresh My Roles to test. And you should get the logged on users roles:
[![image](/uploads/2018/09/image_thumb149.png "image")](/uploads/2018/09/image151.png)
Obviously, now in the target environment, you would probably start to customize the logo, colors, label texts and language, if you don't want to proceed with the "Elven" theme ;)
For example something like this from my company:
[![image](/uploads/2018/09/image_thumb150.png "image")](/uploads/2018/09/image152.png)
With that I can conclude this blog post, we have been able to export the custom connector definition and the PowerApps package including the Flows, and import these into a new environment. Now all that is left is to publish and share the PowerApp to be used in your organization.
Thanks for reading, hope it has been helpful!
