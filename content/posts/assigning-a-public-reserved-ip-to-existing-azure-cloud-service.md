---
title: "Assigning a Public Reserved IP to existing Azure Cloud Service"
date: 2014-10-17T17:32:13Z
draft: false
slug: "assigning-a-public-reserved-ip-to-existing-azure-cloud-service"
tags:
  - "Azure"
  - "PowerShell"
categories:
  - "Cloud OS"
---

I have been running a SQL Server AlwaysOn Cluster in Azure for my System Center environment. I use this mostly for Demo and Development for partner solutions, so I like to shutdown and deallocate the cloud services when I'm not using them. This would also mean that the Public IP address for my Cloud Services would be deallocated and a new IP adresse would be created when I start the Cloud Service deployment again.
So, I have been looking into the new possibility of creating a reservation for the Public IP address, as described here: http://msdn.microsoft.com/en-us/library/azure/dn690120.aspx.
As described in the link:

- You must reserve the IP address first, before deploying.
- At this time, you can’t go back and apply a reservation to something that’s already been deployed.

Unfortunately, I had already deployed my cloud service and VMs.
The solution? Well, If I'm willing to accept a small downtime, I can easily remove and re-deploy my Cloud Service and VMs while keeping my data and configurations!
My solution was using Azure PowerShell, and save the VM configuration to XML files, then delete the VMs (NB! Important not to delete the disks). After that I recreate the VMs from the config XML files, and specify my IP address reservation which I had already created before. Now my Cloud Service and VM deployment have a reservation, and in that way my SQL AlwaysOn listener keeps a fixed IP address.
The complete solution is listed in the script window below, the script is meant to run interactively snippet by snippet. Please make sure that you do a backup first if this is required.

```powershell
# PowerShell command to set a reserved IP address for Cloud Service in Azure
# Reference:
# Reserved IP addresses: http://msdn.microsoft.com/en-us/library/azure/dn690120.aspx

# Log on to my Azure account
Add-AzureAccount

# Set active subscription
Get-AzureSubscription -SubscriptionName "mysubscriptionname" | Select-AzureSubscription

# Create a Public Reserved IP for SQL AlwaysOn Listener IP
$ReservedIP = New-AzureReservedIP -ReservedIPName "SCSQLAlwaysOnListenerIP" -Label "SCSQLAlwaysOnListenerIP" -Location "West Europe"

$workingDir = (Get-Location).Path

# Define VMs and Cloud Service
$vmNames = 'az-scsql02', 'az-scsql01', 'az-scsqlquorum'
$serviceName = "mycloudsvc-az-scsql"

# Export VM Config and Stop VM
ForEach ($vmName in $vmNames) {

    $Vm = Get-AzureVM –ServiceName $serviceName –Name $vmName
    $vmConfigurationPath = $workingDir + "\exportedVM_" + $vmName +".xml"
    $Vm | Export-AzureVM -Path $vmConfigurationPath

    Stop-AzureVM –ServiceName $serviceName –Name $vmName -Force

}

# Remove VMs while keeping disks
ForEach ($vmName in $vmNames) {

    $Vm = Get-AzureVM –ServiceName $serviceName –Name $vmName
    $vm | Remove-AzureVM -Verbose

}

# Specify VNet for the VMs
$vnetname = "myvnet-prod"

# Re-create VMs in specified order
$vmNames = 'az-scsqlquorum', 'az-scsql01', 'az-scsql02'

ForEach ($vmName in $vmNames) {

    $vmConfigurationPath = $workingDir + "\exportedVM_" + $vmName +".xml"
    $vmConfig = Import-AzureVM -Path $vmConfigurationPath

    New-AzureVM -ServiceName $serviceName -VMs $vmConfig -VNetName $vnetname -ReservedIPName $ReservedIP.ReservedIPName -WaitForBoot:$false

}
```
