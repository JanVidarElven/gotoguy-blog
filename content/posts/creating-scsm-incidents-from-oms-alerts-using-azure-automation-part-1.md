---
title: "Creating SCSM Incidents from OMS Alerts using Azure Automation – Part 1"
date: 2015-12-08T00:03:31Z
draft: false
slug: "creating-scsm-incidents-from-oms-alerts-using-azure-automation-part-1"
tags:
  - "Azure"
  - "Operations Management Suite"
  - "Service Manager"
categories:
  - "Automation"
  - "Operations Managment Suite"
  - "PowerShell"
---

There has been some great announcements recently for OMS Alerts in Public Preview (<http://blogs.technet.com/b/momteam/archive/2015/12/02/announcing-the-oms-alerting-public-preview.aspx>) and Webhooks support for Hybrid Worker Runbooks (<https://azure.microsoft.com/en-us/updates/hybrid-worker-runbooks-support-webhooks/>). This opens up for some scenarios I have been thinking about.
This 2-part blog will show how you can create a new Service Manager Incident from an Azure Automation Runbook using a Hybrid Worker Group, and with OMS Alerts search for a condition and generate an alert which triggers this Azure Automation Runbook for creating an Incident in Service Manager via a Webhook and some contextual data for the Alert.

- Part 1: Create an Azure Automation Runbook that connects to and generates an Incident in Service Manager via a Hybrid Worker
- [Part 2: Create an OMS Alert that searches for a specified log event and triggers the Azure Automation Runbook with some contextual data for the Incident](https://systemcenterpoint.wordpress.com/2015/12/08/creating-scsm-incidents-from-oms-alerts-using-azure-automation-part-2/)

This is the first part of this blog post, so I will start by preparing the Service Manager environment, creating the Azure Automation Runbook, and testing the Incident creation via the Hybrid Worker.

## Prepare the Service Manager Environment

First I want to prepare my Service Manager Environment for the Incident creation via Azure Automation PowerShell Runbooks. I decided to create a new Incident Source Enumeration for 'Operations Management Suite', and also to create a new account with permissions to create incidents in Service Manager to be used in the Runbooks.
To create the Source I edited the Library List for Incident Source like this:
![](/uploads/2015/12/120715_2351_creatingscs1.png)
To make it easier to refer to this Enumeration Value in PowerShell scripts, I define my own ID in the corresponding Management Pack XML:
![](/uploads/2015/12/120715_2351_creatingscs2.png)
And specifying the DisplayString for the ElementID for the Languages I want:
![](/uploads/2015/12/120715_2351_creatingscs3.png)
The next step is to prepare the account for the Runbook. As Azure Automation Runbooks on Hybrid Workers will run as Local System, I need to be able to run my commands as an account with permissions to Service Manager and to create Incidents.
I elected to create a new local Active Directory account, and give that account permission to my Service Manager Management Server.
With the new account created, I added it to the Remote Management Users local group on the Service Manager Management Server:
![](/uploads/2015/12/120715_2351_creatingscs4.png)
Next I added this account to the Advanced Operators Role Group in Service Manager:
![](/uploads/2015/12/120715_2351_creatingscs5.png)
Adding the account to the Advanced Operators group is more permission than I need for this scenario, but will make me able to use the same account for other work item scenarios in the future.
With the Service Manager Enviroment prepared, I can go to the next step which is the PowerShell Runbook in Azure Automation.

## Create an Azure Automation Runbook for creating SCSM Incidents

I created a new PowerShell Script based Runbook in Azure Automation for Creating Incidents. This Runbook are using a Credential Asset to run Remote PowerShell session commands to my Service Manager Management Server. The Credential Asset is the local Active Directory Account I created in the previous step:
![](/uploads/2015/12/120715_2351_creatingscs6.png)
I also have created a variable for the SCSM Management Server Name to be used in the Runbook.
The PowerShell Runbook can then be created in Azure Automation, using my Automation Assets, and connecting to Service Manager for creating a new Incident as specified:
![](/uploads/2015/12/120715_2351_creatingscs7.png)
The complete PowerShell Runbook is show below:
```powershell
# Setting Generic Incident Title and Description
$incident_title = "Azure Automation Generated Alert"
$incident_desc = "This Incident is generated from an Azure Automation Runbook via Hybrid Worker"
# Getting Assets for SCSM Management Server Name and Credentials
$scsm_mgmtserver = Get-AutomationVariable -Name 'SCSMServerName'
$credential = Get-AutomationPSCredential -Name 'SCSMAASvcAccount'
# Create Remote Session to SCSM Management Server
# (Specified credential must be in Remote Management Users local group and SCSM operator)
$session = New-PSSession -ComputerName $scsm_mgmtserver -Credential $credential
# Import module for Service Manager PowerShell CmdLets
$SMDIR = Invoke-Command -ScriptBlock {(Get-ItemProperty 'hklm:/software/microsoft/System Center/2010/Service Manager/Setup').InstallDirectory} -Session $session
Invoke-Command -ScriptBlock { param($SMDIR) Set-Location -Path $SMDIR } -Args $SMDIR -Session $session
Import-Module ".\Powershell\System.Center.Service.Manager.psd1" -PSSession $session
# Create Incident
Invoke-Command -ScriptBlock { param ($incident_title, $incident_desc)
# Get Incident Class
$IncidentClass = Get-SCSMClass -Name System.WorkItem.Incident
# Get Prefix for Incident IDs
$IncidentPrefix = (Get-SCSMClassInstance -Class (Get-SCSMClass -Name System.WorkItem.Incident.GeneralSetting)).PrefixForId
# Set Incident Properties
$Property = @{Id="$IncidentPrefix{0}"
Title = $incident_title
Description = $incident_desc
Urgency = "System.WorkItem.TroubleTicket.UrgencyEnum.Medium"
Source = "SkillSCSM.IncidentSourceEnum.OMS"
Impact = "System.WorkItem.TroubleTicket.ImpactEnum.Medium"
Status = "IncidentStatusEnum.Active"
```
}
```powershell
# Create the Incident
New-SCSMClassInstance -Class $IncidentClass -Property $Property -PassThru
```
} -Args $incident\_title, $incident\_desc -Session $session
```powershell
Remove-PSSession $session
```
The script should be pretty straightforward to interpret. The most important part is that it would require to be run on a Hybrid Worker Group with Servers that can connect via PowerShell Remote to the specified Service Manager Management Server. The Incident that will be created are using a few variables for incident title and description (these will be updated for contextual data from OMS Alerts in part 2), and some fixed data for Urgency, Impact and Status, along with my custom Source for Operations Management Suite (ref. the Enumeration Value created in the first step).
After publishing this Runbook I'm ready to run it with a Hybrid Worker.

## Testing the PowerShell Runbook with a Hybrid Worker

Now I can run my Azure Automation PowerShell Runbook. I select to run it on my previously defined Hybrid Worker Group.
![](/uploads/2015/12/120715_2351_creatingscs8.png)
The Runbook is successfully completed, and the output is showing the new incident details:
![](/uploads/2015/12/120715_2351_creatingscs9.png)
I can also see the Incident created in Service Manager:
![](/uploads/2015/12/120715_2351_creatingscs10.png)
That concludes this first part of this blog post. Stay tuned for how to create an OMS Alert and trigger this Runbook in part 2!
