---
title: "Creating SCSM Incidents from OMS Alerts using Azure Automation – Part 2"
date: 2015-12-08T16:58:17Z
draft: false
slug: "creating-scsm-incidents-from-oms-alerts-using-azure-automation-part-2"
tags:
  - "Azure"
  - "Operations Management Suite"
categories:
  - "Automation"
  - "Operations Managment Suite"
  - "PowerShell"
  - "Service Manager"
---

This is the second part of a 2-part blog article that will show how you can create a new Service Manager Incident from an Azure Automation Runbook using a Hybrid Worker Group, and with OMS Alerts search for a condition and generate an alert which triggers this Azure Automation Runbook for creating an Incident in Service Manager via a Webhook and some contextual data for the Alert.

- [Part 1: Create an Azure Automation Runbook that connects to and generates an Incident in Service Manager via a Hybrid Worker](https://systemcenterpoint.wordpress.com/2015/12/08/creating-scsm-incidents-from-oms-alerts-using-azure-automation-part-1/)
- Part 2: Create an OMS Alert that searches for a specified log event and triggers the Azure Automation Runbook with some contextual data for the Incident

In Part 1 of the blog I prepared my Service Manager environment, and created Azure Automation Runbook and Assets to run via Hybrid Worker for generating incidents in Service Manager. In this second part of the blog I will configure my Operations Management Suite environment for OMS Alerting and Alert Remediation, and create an OMS Alert that will trigger this PowerShell Runbook.

## Configuring OMS Alerting and Remediation

If you haven't already for your OMS Workspace, you will need to enable the OMS Alerting and Alert Remediation under Settings and Preview Features. This is shown in the picture below:
![](/uploads/2015/12/120815_1649_creatingscs1.png)

## Creating the OMS Alert

The next step is to create the OMS Alert. To do this I will need to do a Log Search with the criteria I want. For my example in this article, I will use an EventLog Search where I have previously added Azure AD Application Proxy Connector Event Log to OMS, and where I also have created a custom field for events where "The Connector was unable to connect to the service due to networking issues".
The result of this Log Search is shown below, where I have 7 results in the last 7 days:
![](/uploads/2015/12/120815_1649_creatingscs2.png)
When I enabled OMS Alerting and Remediation under Settings, I can now see that I have a new Alert button at the bottom of the screen. I click on that to create my new OMS Alert.
I give the OMS Alert a descriptive name, using my current search query, and checking every 15 minutes for this alert. I can also specify a threshold over a specified time windows, in this case I want the Alert to trigger if there are more than 0 occurrences. If I want to I can also send an email notification to specified recipient(s).
![](/uploads/2015/12/120815_1649_creatingscs3.png)
Since I want to generate a SCSM Incident when this OMS Alert triggers, I select to Enable Remediation and select my Create-SCSMIncident Runbook.
![](/uploads/2015/12/120815_1649_creatingscs4.png)
After saving the OMS Alert I get a successful confirmation, and a link to where I can see my configured Alerts:
![](/uploads/2015/12/120815_1649_creatingscs5.png)
While in Preview I can only create up to 10 Alerts, and I can also remove them but not edit existing for now:
![](/uploads/2015/12/120815_1649_creatingscs6.png)
That is all I need to configure in Operations Management Suite to get the OMS Alert to trigger. Now I need to go back to the Azure Portal and configure some changes for my PowerShell Runbook!

## Configuring Azure Automation PowerShell Runbook for Webhook and Hybrid Worker Group

In the Azure Portal and under my Automation Account and the PowerShell Runbook I created for Create-SCSMIncident (see Part 1), there will now automatically be created a Webhook for OMS Alert Remediation. This Webhook has a expiry date of one year ahead of creation.
![](/uploads/2015/12/120815_1649_creatingscs7.png)
I now need to specify the Parameters for the Webhook, so that it runs on my Hybrid Worker group:
![](/uploads/2015/12/120815_1649_creatingscs8.png)
After I have specified the Hybrid Worker group, any OMS Alerts will now trigger this Runbook and run on my local environment, and in this case create the SCSM incident as specified in the PowerShell Runbook. But, I also want to have some contextual data in the Incident, so I need to look at the Webhook data in the next step.

## Configuring and using Webhook for contextual data in Runbook

Whenever the OMS Alert triggers the remediation Azure Automation Runbook via the Webhook, event information will be submitted from OMS to the Runbook via WebhookData input parameter.
An example of this is shown in the image below, where the WebhookData Input Parameter contains event information formatted as JSON (JavaScript Object Notation):
![](/uploads/2015/12/120815_1649_creatingscs9.png)
So, I need to configure my PowerShell Runbook to process this WebhookData, and to use that information when creating the Incident.
Let's first take a look at the WebhookData. If I copy the input from above to for example Visual Studio Code, I can see clearer that the WebhookData consists of a WebhookName, RequestBody and RequestHeader. The values I'm looking for are in the RequestBody and SearchResults:
![](/uploads/2015/12/120815_1649_creatingscs10.png)
I update my PowerShell Runbook so that I can process the WebhookData, and get the WebhookName, WebhookHeaders and WebhookBody. When I have the WebhookBody, I can get the SearchResults and by using ConvertFrom-JSON loop trough the value array to get the fields I'm looking for like this:
![](/uploads/2015/12/120815_1649_creatingscs11.png)
In this case I want the Source, EventID and RenderedDescription, which also corresponds to the values from the Alert in OMS, as shown below. I then use these values for the Incident Title and Description in the PowerShell Runbook.
![](/uploads/2015/12/120815_1649_creatingscs12.png)
The complete Azure Automation PowerShell Runbook is shown below:
param (
[object]$WebhookData
)
if ($WebhookData -ne $null) { 
```powershell
# Get Webhook Data
$WebhookName = $WebhookData.WebhookName
$WebhookHeaders = $WebhookData.RequestHeader
$WebhookBody = $WebhookData.RequestBody
# Writing Webhook Data to verbose output
Write-Verbose "Webhook name: '$WebhookName'"
Write-Verbose "Webhook header:"
Write-Verbose $WebhookHeaders
Write-Verbose "Webhook body:"
Write-Verbose $WebhookBody
# Searching Webhook Data for Value Results
$SearchResults = (ConvertFrom-JSON $WebhookBody).SearchResults
$SearchResultsValue = $SearchResults.value
```
Foreach ($item in $SearchResultsValue)
{
```powershell
# Getting Alert Source, EventID and RenderedDescription
$AlertSource = $item.Source
Write-Verbose "Alert Name: '$AlertSource'"
$AlertEventId = $item.EventID
Write-Verbose "Alert EventID: '$AlertEventId'"
$AlertDescription = $item.RenderedDescription
Write-Verbose "Alert Description: '$AlertDescription'"
```
}
```powershell
# Setting Incident Title and Description based on OMS Alert
$incident_title = "OMS Alert: " + $AlertSource
$incident_desc = $AlertDescription
```
}
else
{
```powershell
# Setting Generic Incident Title and Description
$incident_title = "Azure Automation Generated Alert"
$incident_desc = "This Incident is generated from an Azure Automation Runbook via Hybrid Worker"
```
}
```powershell
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
After publishing the updated Runbook I'm ready for the OMS Alert to trigger.

## When the OMS Alert triggers

The next time this OMS Alert triggers, I can verify that the Runbook is started and an Incident is created. Since I also wanted an email notification, I also received that:
![](/uploads/2015/12/120815_1649_creatingscs13.png)
In Operations Management Suite, I search for any OMS Alerts generated by using the query "Type=Alert SourceSystem=OMS":
![](/uploads/2015/12/120815_1649_creatingscs14.png)
In Azure Automation, I can see that the Runbook has launched a job:
![](/uploads/2015/12/120815_1649_creatingscs15.png)
And most importantly, I can see that the Incident is created in Service Manager with the info I specified:
![](/uploads/2015/12/120815_1649_creatingscs16.png)
That concludes this two-part blog article on how to create SCSM Incidents from OMS Alerts. OMS Automation rocks!
