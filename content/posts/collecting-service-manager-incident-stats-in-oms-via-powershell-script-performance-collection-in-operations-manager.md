---
title: "Collecting Service Manager Incident Stats in OMS via PowerShell Script Performance Collection in Operations Manager"
date: 2016-02-19T01:18:36Z
draft: false
slug: "collecting-service-manager-incident-stats-in-oms-via-powershell-script-performance-collection-in-operations-manager"
tags:
  - "Azure"
  - "Log Insights"
  - "Operations Management Suite"
categories:
  - "Operations Manager"
  - "Operations Managment Suite"
  - "PowerShell"
  - "Service Manager"
---

I have been thinking about bringing in some key Service Manager statistics to Microsoft Operations Management Suite. The best way to do that now is to use the NRT Performance Data Collection in OMS and PowerShell Script rule in my Operations Manager Management Group that I have connected to OMS. The key solution to make this happen are the "Sample Management Pack - Wizard to Create PowerShell script Collection Rules" described in this blog article <http://blogs.msdn.com/b/wei_out_there_with_system_center/archive/2015/09/29/oms-collecting-nrt-performance-data-from-an-opsmgr-powershell-script-collection-rule-created-from-a-wizard.aspx>.
With this solution I can practically get any data I want into OMS via SCOM and PowerShell Script, so I will start my solution for bringing in Service Manager Stats by defining some PowerShell commands to get the values I want. For that I will use the SMLets PowerShell Module for Service Manager.
For this blog article, I will focus on Incident Stats from SCSM. In a later article I will get in some more SCSM data to OMS.

## Getting Ready

I have to do some preparations first. This includes:

1. Importing the "Sample Management Pack – Wizard to Create PowerShell script Collection Rules"
   1. This can be downloaded from Technet Gallery at <https://gallery.technet.microsoft.com/Sample-Management-Pack-e48040f7>
2. Install the SMLets for SCSM PowerShell Module (at the chosen Target server for the PowerShell Script Rule).
   1. I chose to install it from the PowerShell Gallery at <https://www.powershellgallery.com/packages/SMLets>
   2. If you are running Windows Server 2012 R2, which I am, follow the instructions here to support the PowerShellGet module, <https://www.powershellgallery.com/GettingStarted?section=Get%20Started>.
3. Choose Target for where to run the SCSM commands from
   1. Regarding the SMLets and where to install, I decided to use the SCOM Root Management Server Emulator. This server will then run the SCSM commands against the Service Manager Management Server.
4. Choose account for Run As Profile
   1. I also needed to think about the run as account the SCSM commands will run under. As we will see later the PowerShell Script Rules will be set up with a Default Run As Profile.
   2. The Default Run As Profile for the RMS Emulator will be the Management Server Action Account, if I had chosen another Rule Target the Default Run As Profile would be the Local System Account.
   3. Alternatively, I could have created a custom Run As Profile with a SCSM user account that have permissions to read the required data from SCSM, and configured the PowerShell Script rules to use that.
   4. I decided to go with the Management Server Action Account, and make sure that this account is mapped to a Role in SCSM with access to the work items I want to query against, any Operator Role will do but you could chose to scope and restrict more if needed:![](/uploads/2016/02/021916_0106_collectings1.png)

At this point I'm ready for the next step, which is to create some PowerShell commands for the Script Rule in SCOM.

## Creating the PowerShell Command Script for getting SCSM data

First I needed to think about what kind of Incident data I wanted to get from SCSM. I decided to get the following values:

- Active Incidents
- Pending Incidents
- Resolved Incidents
- Closed Incidents
- Incidents Opened Last Day
- Incidents Opened Last Hour

These values will be retrieved by the Get-SCSMIncident cmdlet in SMLets, using different criteria. The complete script is shown below:
```powershell
# Debug file
$debuglog = $env:TEMP+"\powershell_perf_collect_debug.log"
```
Date | Out-File $debuglog
"Who Am I: " | Out-File $debuglog -Append
whoami | Out-File $debuglog -Append
```powershell
$ErrorActionPreference = "Stop"
```
Try {
```powershell
Import-Module "C:\Program Files\WindowsPowerShell\Modules\SMLets"
$API = new-object -comObject "MOM.ScriptAPI"
$scsmserver = "MY-SCSM-MANAGEMENTSERVER-HERE"
$beforetime = $(Get-Date).AddHours(-1)
$beforedate = $(Get-Date).AddDays(-1)
$PropertyBags=@()
$activeincidents = 0
$activeincidents = @(Get-SCSMIncident -ComputerName $scsmserver -Status 'Active').Count
$PropertyBag = $API.CreatePropertyBag()
$PropertyBag.AddValue("Instance", "Active Incidents")
$PropertyBag.AddValue("Value", [UInt32]$activeincidents)
$PropertyBags += $PropertyBag
```
"Active Incidents: " | Out-File $debuglog -Append
```powershell
$activeincidents | Out-File $debuglog -Append
$pendingincidents = 0
$pendingincidents = @(Get-SCSMIncident -ComputerName $scsmserver -Status 'Pending').Count
$PropertyBag = $API.CreatePropertyBag()
$PropertyBag.AddValue("Instance", "Pending Incidents")
$PropertyBag.AddValue("Value", [UInt32]$pendingincidents)
$PropertyBags += $PropertyBag
```
"Pending Incidents: " | Out-File $debuglog -Append
```powershell
$pendingincidents | Out-File $debuglog -Append
$resolvedincidents = 0
$resolvedincidents = @(Get-SCSMIncident -ComputerName $scsmserver -Status 'Resolved').Count
$PropertyBag = $API.CreatePropertyBag()
$PropertyBag.AddValue("Instance", "Resolved Incidents")
$PropertyBag.AddValue("Value", [UInt32]$resolvedincidents)
$PropertyBags += $PropertyBag
```
"Resolved Incidents: " | Out-File $debuglog -Append
```powershell
$resolvedincidents | Out-File $debuglog -Append
$closedincidents = 0
$closedincidents = @(Get-SCSMIncident -ComputerName $scsmserver -Status 'Closed').Count
$PropertyBag = $API.CreatePropertyBag()
$PropertyBag.AddValue("Instance", "Closed Incidents")
$PropertyBag.AddValue("Value", [UInt32]$closedincidents)
$PropertyBags += $PropertyBag
```
"Closed Incidents: " | Out-File $debuglog -Append
```powershell
$closedincidents | Out-File $debuglog -Append
$incidentsopenedlasthour = 0
$incidentsopenedlasthour = @(Get-SCSMIncident -CreatedAfter $beforetime -ComputerName $scsmserver).Count
$PropertyBag = $API.CreatePropertyBag()
$PropertyBag.AddValue("Instance", "Incidents Opened Last Hour")
$PropertyBag.AddValue("Value", [UInt32]$incidentsopenedlasthour)
$PropertyBags += $PropertyBag
```
"Incidents Opened Last Hour: " | Out-File $debuglog -Append
```powershell
$incidentsopenedlasthour | Out-File $debuglog -Append
$incidentsopenedlastday = 0
$incidentsopenedlastday = @(Get-SCSMIncident -CreatedAfter $beforedate -ComputerName $scsmserver).Count
$PropertyBag = $API.CreatePropertyBag()
$PropertyBag.AddValue("Instance", "Incidents Opened Last Day")
$PropertyBag.AddValue("Value", [UInt32]$incidentsopenedlastday)
$PropertyBags += $PropertyBag
```
"Incidents Opened Last Day: " | Out-File $debuglog -Append
```powershell
$incidentsopenedlastday | Out-File $debuglog -Append
$PropertyBags
```
} Catch {
"Error Catched: " | Out-File $debuglog -Append
```powershell
$($_.Exception.GetType().FullName) | Out-File $debuglog -Append
$($_.Exception.Message) | Out-File $debuglog -Append
```
}
Some comments about the script. I usually like to include some debug logging in the script when I develop the solution. This way I can keep track of what happens underway in the script or get some exceptions if the script command fails. Be aware though that doing $ErrorActionPreference=Stop will end the script if any errors, so it might be an idea to remove the debug logging when confirmed that everything works.
In the next part I'm ready to create the PowerShell Script Rule.

## Creating the PowerShell Script Rule

In the Operations Console, under Authoring, create a new PowerShell Script Rule as shown below:

1. Select the PowerShell Script (Performance – OMS Bound) Rule:![](/uploads/2016/02/021916_0106_collectings2.png)I have created a custom destination management pack for this script.
2. Specifying a Rule name and Rule Category: Performance Collection. As mentioned earlier in this article the Rule target will be the Root Management Server Emulator:![](/uploads/2016/02/021916_0106_collectings3.png)
3. Selecting to run the script every 30 minutes, and at which time the interval will start from:![](/uploads/2016/02/021916_0106_collectings4.png)
4. Selecting a name for the script file and timeout, and entering the complete script as shown earlier:![](/uploads/2016/02/021916_0106_collectings5.png)
5. For the Performance Mapping information, the Object name must be in the <\\FQDN\YourObjectName> format. For FQDN I used the Target variable for PrincipalName, and for the Object Name ServiceManagerIncidentStats, and adding the "\\" at the start and "\" between: \\$Target/Host/Property[Type="MicrosoftWindowsLibrary7585010!Microsoft.Windows.Computer"]/PrincipalName$\ServiceMgrIncidentStats I specified the Counter name as "Service Manager Incident Stats", and the Instance and Value are specified as $Data/Property(@Name='Instance')$ and $Data/Property(@Name=Value)$. These reflect the PropertyBag instance and value created in the PowerShell script:![](/uploads/2016/02/021916_0106_collectings6.png)
6. After finishing the Create Rule Wizard, two new rules are created, which you can find by scoping to the Root Management Server Emulator I chose as target. Both Rules must be enabled, as they are not enabled by default:![](/uploads/2016/02/021916_0106_collectings7.png)
7. Looking into the Properties of the rules, we can make edits to the PowerShell script, and verify that the Run as profile is the Default. This is where I would change the profile if I wanted to create my own custom profile and run as account for it.![](/uploads/2016/02/021916_0106_collectings8.png)

At this point we are finished configuring the SCOM side, and can wait for some hours to see that data are actually coming into my OMS workspace.

## Looking at Service Manager Performance Data in OMS

After a while I will start seeing Performance Data coming into OMS with the specified Object and Counter Name, and for the different instances and values.
In Log Search, I can specify Type=Perf ObjectName=ServiceMgrIncidentStats, and I will find the Results and Metrics for the specified time frame.
![](/uploads/2016/02/021916_0106_collectings9.png)
I can now look at Service Manager stats as performance data, showing different scenarios like how many active, pending, resolved and closed incidents there are over a time period. I can also look at how many incidents are created by each hour or by each day.
Finally, I can also create saved searches and alerts that creates for example alerts when the number of incidents for any counters are over a set value.
Thanks for reading, and look for more blog posts on OMS and getting SCSM data via NRT Perfomance Collection in the future ;)
