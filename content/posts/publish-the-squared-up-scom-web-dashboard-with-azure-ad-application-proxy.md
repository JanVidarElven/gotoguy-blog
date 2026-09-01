---
title: "Publish the Squared Up SCOM Web Dashboard with Azure AD Application Proxy"
date: 2015-09-24T21:34:10Z
draft: false
slug: "publish-the-squared-up-scom-web-dashboard-with-azure-ad-application-proxy"
tags:
  - "Azure"
  - "Azure AD Application Proxy"
  - "Azure AD Premium"
  - "Squared Up"
categories:
  - "Enterprise Mobility Suite"
  - "Operations Manager"
---

## The Scenario

Squared Up is a Web based Dashboard solution for SCOM environments, and since its built on HTML5 it works on any device or browser as long as you can connect to the Web Server the solution is installed on.
This should be another good scenario for using the Azure AD Application Proxy, as the Squared Up Web Site needs to be installed either on the SCOM Management Server or on a Server that can connect to the Management Server internally.
In this blog article I will describe how to publish the new Squared Up Web Site. This will give me some interesting possibilities for either pass-through or pre-authentication and controlling user access.
There are two authentication scenarios for publishing the Squared Up Web Site with Azure AD App Proxy:

1. Publish without pre-authentication (pass through). This scenario is best used when Squared Up is running Forms Authentication, so that the user can choose which identity they want to log in with. Forms Authentication is also default mode for Squared Up installations.
2. Publish with pre-authentication. This scenario will use Azure AD authentication, and is best used when Squared Up Web Site is running Windows Authentication so that we can have single sign-on with the Azure AD identity.

I will go through both authentication scenarios here.
I went through these steps:

## Create the Application in Azure AD

In this next step, I will create the Proxy Application in Azure AD where the Self Service Portal will be published. To be able to create Proxy Applications I will need to have either an Enterprise Mobility Suite license plan, or Azure AD Basic/Premium license plan. From the Azure Management Portal and Active Directory, under Applications, I add a new Application and select to "Publish an application that will be accessible from outside your network":
![](/uploads/2015/09/092415_2121_publishthes1.png)
I will then give a name for my application, specify the internal URL and pre-authentication method. I name my application "Squared Up SCOM Dashboard", use http://scomdashboardserver/SquaredUp/ as internal URL and choose Passthrough as Pre-Authentication method.
After the Proxy Application is added, there are some additional configurations to be done. If I have not already, Application Proxy for the directory have to be enabled. I have created other Proxy Applications before this, so I have already done that.
![](/uploads/2015/09/092415_2121_publishthes2.png)
I also need to download the Application Proxy connector, install and register this on a Server that is member of my own Active Directory. The Server that I choose can be either on an On-Premise network, or in an Azure Network. As long as the Server running the Proxy connector can reach the internal URL, I can choose which Server that best fits my needs.
When choosing passthrough as authentication method, all users can directly access the Forms Based logon page as long as they know the external URL. Assigning accounts, either users or groups, will only decide which users that will see the application in the Access Panel or My Apps.
![](/uploads/2015/09/092415_2121_publishthes3.png)
I now need to make additional configurations to the application, and go to the Configure menu. From here I can configure the name, external URL, pre-authentication method and internal URL, if I need to change something.
I choose to change the External URL so that I use my custom domain, and note the warning about creating a CNAME record in external DNS. After that I hit Save so that I can configure the Certificate.
![](/uploads/2015/09/092415_2121_publishthes4.png)
Since I have already uploaded a certificate (see previous blog post <https://systemcenterpoint.wordpress.com/2015/06/10/using-a-custom-domain-name-for-an-application-published-with-with-azure-ad-application-proxy/>), I can just verify that it is correct.
![](/uploads/2015/09/092415_2121_publishthes5.png)
When using passthrough I don't need to configure any internal authentication method.
![](/uploads/2015/09/092415_2121_publishthes6.png)
Another feature that is in Preview, is to allow Self-Service Access to the published application. I have configured this here, so that users can request access to the application from the Access Panel (<https://myapps.microsoft.com>).
![](/uploads/2015/09/092415_2121_publishthes7.png)
After I have configured this and uploaded a logo, I am finished at this step, and can test the application using passthrough.

## Testing the application using passthrough

When using Passthrough I can go directly to the external URL, which in my case is <https://scom.skill.no/squaredup>. And as expected, I can reach the internal Forms Based login page:
![](/uploads/2015/09/092415_2121_publishthes8.png)
For the users and groups I have assigned access to, they will also see the Squared Up application in the Access Panel or in My Apps, this application is linked to the external URL:
![](/uploads/2015/09/092415_2121_publishthes9.png)
Now I'm ready to do the next step which is change Pre-Authentication and use Azure AD Authentication and Single Sign-On.

## Change Application to use Azure AD Authentication as Pre-Authentication

First I will reconfigure the Azure AD App Proxy Application, by changing the Preauthentication method to Azure Active Directory.
![](/uploads/2015/09/092415_2121_publishthes10.png)
Next I need to configure to use Internal Authentication Method "Windows Integrated Authentication". I also need to configure the Service Principal Name (SPN). Here I specify HTTP/scomdashboardserverfqdn, in my example this is HTTP/skill-scom02.skill.local.
![](/uploads/2015/09/092415_2121_publishthes11.png)
PS! A new preview feature is available, to choose which login identity to delegate. I will continue using the default value of User principal name.
Since I now will use pre-authentication, it will be important to remember to assign individual users or groups to the Application. This enables me to control which users who will see the application under their My Apps and who will be able access the application's external URL directly.
From the bottom part of the configuration settings I can configure Access Rules, which at this time is in Preview. This is cool, because I can for example require for this Application that users will be required to use multi-factor authentication. I have not enabled that here though.
![](/uploads/2015/09/092415_2121_publishthes12.png)
After I'm finished reconfiguring the Azure AD App Proxy Application, I can save and continue with the other requirements.

## Enable Windows Authentication for Squared Up

The Squared Up Web site supports Windows Authentication, the instructions for configuring that is described here: <http://support.squaredup.com/support/solutions/articles/4136-enable-integrated-windows-authentication-single-sign-on->.
Follow that article and you should be ready for the next step.
It is a good idea at this point to verify that Windows Integrated Authentication is working correctly by browsing internally to <http://scomdashboardserver/SquaredUp>. Your current logged on user (if permissions are correct) should be logged in automatically.

## Configure Kerberos Constrained Delegation for the Proxy Connector Server

I now need to configure so that the Server running the Proxy Connector can impersonate users pre-authenticating with Azure AD and use Windows Integrated Authentication to the Squared Up Server.
I find the Computer Account in Active Directory for the Connector Server, and on the Delegation tab click on "Trust this computer for delegation to specified services only", and to "Use any authentication protocol". Then I add the computer name for the web server that Squared Up is installed on and specify the http service as shown below (I already have an existing delegation set up):
![](/uploads/2015/09/092415_2121_publishthes13.png)
This was the last step in my configuration, and I am almost ready to test.
If you, like me, have an environment consisting on both On-Premise and Azure Servers in a Hybrid Datacenter, please allow room for AD replication of these SPN's and more.

## Testing the published application with Azure AD Authentication!

Now I am ready to test the published proxy application with Azure AD Authentication.
When I go to my external URL <https://scom.skill.no/squaredup>, Azure AD will check if I already has an authenticated session, or else I will presented with the logon page for Azure AD (in Norwegian but you get the picture ;):
![](/uploads/2015/09/092415_2121_publishthes14.png)
Remember from earlier that I have assigned the application either to a group of all or some users or directly to some pilot users for example.
If I log in with an assigned user, I will be directly logged in to the Squared Up Dashboard:
![](/uploads/2015/09/092415_2121_publishthes15.png)
In addition to access the application via the Access Panel (<https://myapps.microsoft.com>), I can use the App Launcher menu in Office 365 and add the Squared Up Dashboard to the App chooser for easy access:
![](/uploads/2015/09/092415_2121_publishthes16.png)
I can also access the Squared Up Application from the "My Apps" App on my Mobile Devices.
So to conclude, Squared Up is another great solution for publishing with Azure AD Application Proxy !
