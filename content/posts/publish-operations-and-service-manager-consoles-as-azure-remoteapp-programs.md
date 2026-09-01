---
title: "Publish Operations and Service Manager Consoles as Azure RemoteApp Programs"
date: 2016-02-02T22:15:35Z
draft: false
slug: "publish-operations-and-service-manager-consoles-as-azure-remoteapp-programs"
tags:
  - "Azure"
  - "Enterprise Mobility"
categories:
  - "Azure RemoteApp"
  - "Enterprise Mobility Suite"
  - "Operations Manager"
  - "Service Manager"
---

This blog post will show how you can publish System Center 2012 R2 Management Consoles like the Operations Console and Service Console as Azure Remote Apps.
I already have an environment in Azure that runs Service Manager and Operations Manager 2012 R2. Now I want remote clients and platforms to be able to run these consoles as remote apps.
When planning, I decided to use a Hybrid Collection, and the overall steps was (as documented in <https://azure.microsoft.com/en-us/documentation/articles/remoteapp-create-hybrid-deployment/>):

1. Decide what image to use for your collection. You can create a custom image or use one of the Microsoft images included with your subscription.
2. Set up your virtual network.
3. Create a collection.
4. Join your collection to your local domain.
5. Add a template image to your collection.
6. Configure directory synchronization. Azure RemoteApp requires that you integrate with Azure Active Directory by either 1) configuring Azure Active Directory Sync with the Password Sync option, or 2) configuring Azure Active Directory Sync without the Password Sync option but using a domain that is federated to AD FS. Check out the configuration info for Active Directory with RemoteApp.
7. Publish RemoteApp apps.
8. Configure user access.

Azure Remote App can only be configured in the classic Azure Management Portal (manage.windowsazure.com), it's on the roadmap for support in the new portal.azure.com and with Azure Resource Manager.

## Step 1 – Create Custom Image for Installing Service Manager and Operations Consoles

There are several options available for creating a custom image. As my System Center environment already was set up in Azure, it made sense to create and use an image on an Azure VM, <https://azure.microsoft.com/en-us/documentation/articles/remoteapp-image-on-azurevm/>.

### Create Azure VM for Image

First I created a VM based on template for Remote Desktop Session Host:
![](/uploads/2016/02/020216_2209_publishoper1.png)
The VM template must be configured to run on a VNet that can contact the Domain Controller for the Domain that the System Center Servers are joined to.
After the VM was provisioned, I joined it to my AD Domain and rebooted.
After that I was ready to install and configure the Service Manager and Operations Consoles with all requirements on the image. I also added the most recent Update Rollups for System Center 2012 R2 Consoles (that already are updated on the System Center Servers of course).
A this point I tested the Service Manager and Operations Consoles, and was successful in connecting the Management Servers.
Finally, the Azure VM needed to be Sysprepped. The desktop contains a validation script, it will validate the image for Azure RemoteApp requirements, and ask to launch Sysprep:
Then:
![](/uploads/2016/02/020216_2209_publishoper2.png)
After running Sysprep the VM shuts down and we are ready for capturing the virtual machine.

### Capture the virtual machine

To capture the image follow the instructions as specified here <https://azure.microsoft.com/en-us/documentation/articles/virtual-machines-capture-image-windows-server/>. 

I give the virtual machine an image name and description, and confirm that I have run Sysprep. Note that the VM will be deleted after the image is captured:
![](/uploads/2016/02/020216_2209_publishoper3.png)
When finished, the captured image is deleted from the virtual machines instances, and available under images:
![](/uploads/2016/02/020216_2209_publishoper4.png)
At this point I have a ready image to use. I can create new VM's based on this image if I want, or I can use it as a RemoteApp image, which I will return to later. Now I'm ready for the next step.

## Step 2 – Set up virtual network

Most will already have this in place if you have an existing Azure Subscription with Azure VMs. The requirement is that the Azure RemoteApp collection and image must be able to connect to the existing infrastructure. In this scenario where I want to use Service Manager and Operations Manager Consoles as Azure RemoteApp, I would need to be able to reach the Management Servers. Basically there are 3 scenarios:

1. The Management Servers and the RemoteApp programs are on the same Azure Virtual Network.
2. The Management Servers are on on-premise infrastructure, and the Virtual Network must be configured with a VPN to the on-premise infrastructure.
3. The Management Servers are on another Virtual Network, and these two Virtual Networks must be connected to each other via Azure Site-to-Site VPN.
   1. A variant on the third scenario, where the Management Servers are created in a Resouce Group in ARM (Azure Resource Manager).

And of course, my scenario was the last one, as I have created my System Center 2012 R2 environment in a Resource Group using Azure Resource Manager J.
Since I cannot configure and deploy Azure RemoteApp in ARM, I needed to create a Site-to-Site VPN between my Azure Service Management environment (ASM) and ARM environment.
There are some good guidance on how to do that in this article: <https://azure.microsoft.com/en-us/documentation/articles/virtual-networks-arm-asm-s2s/>.
Since I already had VNets and VM's in place I had to tweak a little in the guide, but I was able to make it work successfully. I will not get into details on that here, as I will focus on Azure RemoteApp, but that might be stuff for another blog post later :).
PS! Make sure that the Virtual Network has at least one DNS server to provide name resolution!

## Step 3 - Create a collection

At this stage I was ready to create a RemoteApp Collection. I have signed up for a trial as notified in the image below, and selected to create a RemoteApp Collection with a Basic Plan. I specified my Virtual Network and Subnet that has connection to the ARM environment, and select to Join Local Domain.
![](/uploads/2016/02/020216_2209_publishoper5.png)
![](/uploads/2016/02/020216_2209_publishoper6.png)
After creating the RemoteApp Collection, I get a status of Input Required:
![](/uploads/2016/02/020216_2209_publishoper7.png)
At the Quick Start menu, the steps to follow are highlighted:
![](/uploads/2016/02/020216_2209_publishoper8.png)

## Step 4 - Join collection to local domain

The next step is to join the local domain.
I specify my Active Directory Domain information, optionally specifying a OU for the RDS hosts that will provide the service. I also need a service account that has permissions to add computers to the domain.
![](/uploads/2016/02/020216_2209_publishoper9.png)
After successfully joining the domain, the first step is acknowledged and I'm ready for the next step:
![](/uploads/2016/02/020216_2209_publishoper10.png)

## Step 5 - Add template image to collection

I now need to add the previously created Azure VM image I captured to the RemoteApp Collection.

### Import the image into the Azure RemoteApp image library

First I add the image to the RemoteApp library:
![](/uploads/2016/02/020216_2209_publishoper11.png)
I select to import from the Virtual Machines library:
![](/uploads/2016/02/020216_2209_publishoper12.png)
Find my image:
![](/uploads/2016/02/020216_2209_publishoper13.png)
Give it a name for the RemoteApp template and specify a location consistent with my Azure infrastructure:
![](/uploads/2016/02/020216_2209_publishoper14.png)
After that the Upload Pending status will be there for a while, about 15-20 minutes in my case:
![](/uploads/2016/02/020216_2209_publishoper15.png)
And then the RemoteApp image is ready:
![](/uploads/2016/02/020216_2209_publishoper16.png)

### Link collection to existing template image

Now I can link the uploaded image to the collection:
![](/uploads/2016/02/020216_2209_publishoper17.png)
Selecting my image template:
![](/uploads/2016/02/020216_2209_publishoper18.png)
And after that provisioning of the collection with the image starts. This will take a while longer:
![](/uploads/2016/02/020216_2209_publishoper19.png)
While its being provisioned, I can see that the status is pending, and that the operation can take up to 1 hour:
![](/uploads/2016/02/020216_2209_publishoper20.png)
Provisioning status:
![](/uploads/2016/02/020216_2209_publishoper21.png)
Finally, after provisioning:
![](/uploads/2016/02/020216_2209_publishoper22.png)
Then we are ready for the last final steps before we can start testing!

## Step 6 - Configure directory synchronization

Azure RemoteApp requires that you integrate with Azure Active Directory by either 1) configuring Azure Active Directory Sync with the Password Sync option, or 2) configuring Azure Active Directory Sync without the Password Sync option but using a domain that is federated to AD FS.
This is already in place in this environment, so the users I want to configure access for are already in Azure AD.

## Step 7 - Publish RemoteApp apps

I can now publish the Remote App Programs from the provisioned image:
![](/uploads/2016/02/020216_2209_publishoper23.png)
I select the Service Manager Console and Operations Console:
![](/uploads/2016/02/020216_2209_publishoper24.png)
Verify that the RemoteApp programs are published:
![](/uploads/2016/02/020216_2209_publishoper25.png)

## Step 8 - Configure user access

Next I need to configure the users that should have access to the RemoteApp Programs:
![](/uploads/2016/02/020216_2209_publishoper26.png)
After that I'm ready for testing!

## Testing the RemoteApp Programs

Now I can test the RemoteApp Programs.

### HTML5 Remote App Web

First I test with the new HTML5 Remote App Web Client, this is now in Public Preview, and available at the following URL: <https://www.remoteapp.windowsazure.com/web>.
When logging in I'm presented with the following Work Resources:
![](/uploads/2016/02/020216_2209_publishoper27.png)
I can successfully launch the Service Manager and Operations Consoles. I can also easily switch between them in the top menu bar:
![](/uploads/2016/02/020216_2209_publishoper28.png)

### Azure Remote App Desktop App

Next I test with the downloadable Azure RemoteApp Desktop Application. After signing in I can see my work resources and launch them:
![](/uploads/2016/02/020216_2209_publishoper29.png)
The Azure RemoteApp client also seamlessly integrate the RemoteApp Programs at the Start and All Apps Menu in Windows 10:
![](/uploads/2016/02/020216_2209_publishoper30.png)

### Windows 10 Mobile Remote Desktop App

There are Remote Desktop Apps for all mobile platforms (Windows Mobile, iPhone, iOS, Android). Here I have tested the Windows 10 Mobile App:
![](/uploads/2016/02/020216_2209_publishoper31.png)
And I can launch the RemoteApp Program on my phone:
![](/uploads/2016/02/020216_2209_publishoper32.png)

### Windows 10 Continuum Support

There is a new Remote Desktop Preview App out for Windows 10 Mobile that support Continuum, but this Preview App does not currently support Azure RemoteApp. That will come later down the line though, and when that comes I will update this blog post or create a related post with my experiences on that!

## Conclusion

This was quite fun to work with, and the whole process with the 8 steps above worked like a charm. The most challenging thing was to create the Site-to-Site VPN between my ASM and ARM environment in fact. Outside that I never had any errors or problems.
I'm eagerly awaiting Azure RemoteApp support for Azure Resource Manager though!
