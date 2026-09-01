---
title: "Shutdown and Deallocate an Azure VM using Managed Service Identity and Instance Metadata Service"
date: 2018-01-17T14:16:20Z
draft: false
slug: "shutdown-and-deallocate-an-azure-vm-using-managed-service-identity-and-instance-metadata-service"
tags:
  - "Azure"
  - "Managed Service Identity"
categories:
  - "Azure REST API"
  - "PowerShell"
---

The purpose of this blog post is to show how you can run a PowerShell script on an Azure VM that will shutdown and deallocate the actual VM the script is run on.
First, kudos to Marcel Meurer (Azure MVP), that originated the idea of how to run a PowerShell script that will shut down and deallocate the VM from inside itself, this is a good read: [https://www.sepago.de/blog/2018/01/16/deallocate-an-azure-vm-from-itself](https://www.sepago.de/blog/2018/01/16/deallocate-an-azure-vm-from-itself "https://www.sepago.de/blog/2018/01/16/deallocate-an-azure-vm-from-itself").
Marcels blog learnt me of something I havent used before, Azure Instance Metadata Service, where I can get information on my current VM instance. I wanted to combine this with using Managed Service Identity (MSI), and actually let the VM authenticate to itself for running the shut down command. The shut down command will be using the Azure REST API.
First, let us set up the requirements and permissions to get this to work.

## Configure Managed Service Identity

Managed Service Identity is feature that as of January 2018 is in Public Preview, and by using MSI for Azure Virtual Machines I can authenticate to Azure Resource Manager API without handling credentials in the code. You can read more on the specifics here: [https://docs.microsoft.com/en-us/azure/active-directory/msi-tutorial-windows-vm-access-arm](https://docs.microsoft.com/en-us/azure/active-directory/msi-tutorial-windows-vm-access-arm "https://docs.microsoft.com/en-us/azure/active-directory/msi-tutorial-windows-vm-access-arm").
First, we need to set up the Managed Service Identiy the VMs in question. This is done under the VM configuration, by enabling Managed service identity as shown below:
[![image](/uploads/2018/01/image_thumb.png "image")](/uploads/2018/01/image.png)
After saving the configuration, wait for the Managed service identity to be successfully created. This will create a service principal in Azure AD, and for VMs this will have the same name as the virtual machine name.
Now we need to give that service principal access to its own VM. Under the VMs Access Control (IAM) node, select to add a permission for the service principal as shown under. I have given the role of Virtual Machine Contributor, which means that the MSI will be able to write to and perform operations on the VM like shutdown, restart and more:
[![image](/uploads/2018/01/image_thumb1.png "image")](/uploads/2018/01/image1.png)
So for each VM we want to use this PowerShell script, we will need to do the same 2 operations, enable MSI and add service principal permission to the VM:
[![image](/uploads/2018/01/image_thumb2.png "image")](/uploads/2018/01/image2.png)

## PowerShell script for Shutdown and Deallocate using MSI

The following script will when run on the Azure VM do the following steps: (full script follows below as the images are small)

1. Read instance metadata and save subscription, resource group and vm name info:[![image](/uploads/2018/01/image_thumb3.png "image")](/uploads/2018/01/image3.png)
2. Authorize itself to Managed Service Identity:[![image](/uploads/2018/01/image_thumb4.png "image")](/uploads/2018/01/image4.png)
3. Send an Azure Resource Manager REST API POST command for shutdown and deallocate:[![image](/uploads/2018/01/image_thumb5.png "image")](/uploads/2018/01/image5.png)The REST API call for shutting down a VM uses method POST and the following URI format: https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Compute/virtualMachines/{vm}/deallocate?api-version={apiVersion}([https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/virtualmachines-stop-deallocate](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/virtualmachines-stop-deallocate "https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/virtualmachines-stop-deallocate"))

When this script is run on a VM the following output will display that the REST operation was successful, and shortly after the server goes down and deallocates as excpected.
[![image](/uploads/2018/01/image_thumb6.png "image")](/uploads/2018/01/image6.png)
To summarize, this blog post showed how we can use Managed Service Identity together with Azure Instance Metadata Service, to let the VM manage itself. This example showed how to shut down and deallocate, but you can use the REST API for other operations like restart, get info, update the VM and so on. Best of all with using MSI, is that we don’t have to take care of application id’s, secret keys and more, and having those exposed in the script which can be a security issue.
The complete PowerShell script is shown below:
https://gist.github.com/skillriver/f77a1a608eff58adbadb809d0a765051
