---
title: "Displaying Azure Automation Runbook Stats in OMS via Performance Collection and Operations Manager"
date: 2016-03-04T12:39:16Z
draft: false
slug: "displaying-azure-automation-runbook-stats-in-oms-via-performance-collection-and-operations-manager"
tags:
  - "Azure"
  - "Operations Management Suite"
categories:
  - "Automation"
  - "Log Analytics"
  - "Operational Insights"
  - "Operations Manager"
  - "Operations Managment Suite"
  - "PowerShell"
---

Wouldn't it be **great** to get some more information about your Azure Automation Runbooks in the Operations Management Suite Portal? That's a rhetorical question, of course the answer will be yes!
While Azure Automation is a part of the suite of components in OMS, today you only get the following information from the Azure Automation blade:
![](/uploads/2016/03/030416_1227_displayinga1.png)
The blade shows the number of runbooks and jobs from the one Automation Account you have configured. You can only configure one Automation Account at a time, and for getting more details you are directed to the Azure Portal.
![](/uploads/2016/03/030416_1227_displayinga2.png)
I wanted to use my OMS-connected Operations Manager Management Group, and use a PowerShell script rule to get some more statistics for Azure Automation and display that in OMS Log Analytics as Performance Data. I will do this using the "Sample Management Pack – Wizard to Create PowerShell script Collection Rules" described in this blog article <http://blogs.msdn.com/b/wei_out_there_with_system_center/archive/2015/09/29/oms-collecting-nrt-performance-data-from-an-opsmgr-powershell-script-collection-rule-created-from-a-wizard.aspx>.
I will use the AzureRM PowerShell Module for the PowerShell commands that will connect to my Azure subscription and get the Azure Automation Runbooks data.

## Getting Ready

Before I can create the PowerShell script rule for gettting the Azure Automation data, I have to do some preparations first. This includes:

1. Importing the "Sample Management Pack – Wizard to Create PowerShell script Collection Rules" to my Operations Manager environment.
   1. This can be downloaded from Technet Gallery at <https://gallery.technet.microsoft.com/Sample-Management-Pack-e48040f7>.
2. Install the AzureRM PowerShell Module (at the chosen Target server for the PowerShell Script Rule).
   1. I chose to install it from the PowerShell Gallery using the instructions here: <https://azure.microsoft.com/en-us/documentation/articles/powershell-install-configure/>
   2. If you are running Windows Server 2012 R2, which I am, follow the instructions here to support the PowerShellGet module, <https://www.powershellgallery.com/GettingStarted?section=Get%20Started>.
3. Choose Target for where to run the AzureRM commands from
   1. Regarding the AzureRM and where to install, I decided to use the SCOM Root Management Server Emulator. This server will then run the AzureRM commands against my Azure Subscription.
4. Choose account for Run As Profile
   1. I also needed to think about the run as account the AzureRM commands will run under. As we will see later the PowerShell Script Rules will be set up with a Default Run As Profile.
   2. The Default Run As Profile for the RMS Emulator will be the Management Server Action Account, if I had chosen another Rule Target the Default Run As Profile would be the Local System Account.
   3. Alternatively, I could have created a custom Run As Profile with a user account that have permissions to execute the AzureRM cmdlets and connect to and read the required data from the Azure subscription, and configure the PowerShell Script rules to use that.
   4. I decided to go with the Management Server Action Account, in my case SKILL\scom\_msaa. This account will execute the AzureRM PowerShell cmdlets, so I need to make sure that I can login to my Azure subscription using that account.
5. Next, I started PowerShell ISE with "Run as different user", specifying my scom\_msaa account. I run the commands below, as I wanted to save the password for the user I'm going to connect to the Azure subscription and get the Automation data. I also did a test import-module of the AzureRM modules I will need in the main script.![](/uploads/2016/03/030416_1227_displayinga3.png)

The commands above are here in full:
```powershell
# Prepare to save encrypted password

# Verify that logged on as scom_msaa
```
whoami
```powershell
# Get the password
$securepassword = Read-Host -AsSecureString -Prompt "Enter Azure AD account password:"
# Filepath for encrypted password file
$filepath = "C:\users\scom_msaa\AppData\encryptedazureadpassword.txt"
# Save password encrypted to file
```
ConvertFrom-SecureString -SecureString $securepassword | Out-File -FilePath $filepath
```powershell
Import-Module 'C:\Program Files\WindowsPowerShell\Modules\AzureRM'
Import-Module 'C:\Program Files\WindowsPowerShell\Modules\AzureRM.Profile'
Import-Module 'C:\Program Files\WindowsPowerShell\Modules\AzureRM.Automation'
```
At this point I'm ready for the next step, which is to create some PowerShell commands for the Script Rule in SCOM.

## Creating the PowerShell Command Script for getting Azure Automation data

First I needed to think about what kind of Azure Automation and Runbook data I wanted to get from my Azure Subscription. I decided to get the following values:

- Job Count Last Day
- Job Count Last Month
- Job Count This Month
- Job Minutes This Month
- Runbooks in New State
- Runbooks in Published State
- Runbooks in Edit State
- PowerShell Workflow Runbooks
- Graphical Runbooks
- PowerShell Script Runbooks

I wanted to have the statistics for Runbooks Jobs to see the activity of the Runbooks. As I'm running the Free plan of Azure Automation, I'm restricted to 500 minutes a month, so it makes sense to count the accumulated job minutes for the month as well.
In addition to this I want some statistics for the number of Runbooks in the environment, separated on New, Published and Edit Runbooks, and the Runbook type separated on Workflow, Graphical and PowerShell Script.
![](/uploads/2016/03/030416_1227_displayinga4.png)
The PowerShell Script Rule for getting these data will be using the AzureRM PowerShell Module, and specifically the cmdlets in AzureRM.Profile and AzureRM.Automation:
![](/uploads/2016/03/030416_1227_displayinga5.png)
To log in and authenticate to Azure, I will use the encrypted password saved earlier, and create a Credential object for the login:
![](/uploads/2016/03/030416_1227_displayinga6.png)
Initializing the script with date filters and setting default values for variables. I decided to create the script so that I can get data from all the Resource Groups I have Automation Accounts in. This way, If I have multiple Automation Accounts, I can get statistics combined for each of them:
![](/uploads/2016/03/030416_1227_displayinga7.png)
Then, looping through each Resource Group, running the different commands to get the variable data. Since I potentially will loop through multiple Resource Groups and Automation Accounts, the variables will be using += to add to the previous loop value:
![](/uploads/2016/03/030416_1227_displayinga8.png)
After setting each variable and exiting the loop, the $PropertyBag can be filled with the values for the different counters:
![](/uploads/2016/03/030416_1227_displayinga9.png)
The complete script is shown below for how to get those Azure Automation data via SCOM and PowerShell Script Rule to to OMS:
```powershell
# Debug file
$debuglog = $env:TEMP+"\powershell_perf_collect_AA_stats_debug.log"
```
Date | Out-File $debuglog
"Who Am I: " | Out-File $debuglog -Append
whoami | Out-File $debuglog -Append
```powershell
$ErrorActionPreference = "Stop"
```
Try {
If (!(Get-Module –Name "AzureRM")) { Import-Module 'C:\Program Files\WindowsPowerShell\Modules\AzureRM' }
If (!(Get-Module –Name "AzureRM.Profile")) { Import-Module 'C:\Program Files\WindowsPowerShell\Modules\AzureRM.Profile' }
If (!(Get-Module –Name "AzureRM.Automation")) { Import-Module 'C:\Program Files\WindowsPowerShell\Modules\AzureRM.Automation' }
```powershell
# Get Cred for ARM
$filepath = "C:\users\scom_msaa\AppData\encryptedazureadpassword.txt"
$userName = "myAzureADAdminAccount"
$securePassword = ConvertTo-SecureString (Get-Content -Path $FilePath)
$cred = New-Object -TypeName System.Management.Automation.PSCredential ($username, $securePassword)
# Log in and sett active subscription
```
Login-AzureRmAccount -Credential $cred
```powershell
$subscriptionid = "mysubscriptionID"
Set-AzureRmContext -SubscriptionId $subscriptionid
$API = new-object -comObject "MOM.ScriptAPI"
$aftertime = $(Get-Date).AddHours(-1)
$afterdate_lastday = $(Get-Date).AddDays(-1)
$afterdate_lastmonth = $(Get-Date).AddDays(-30)
$afterdate_thismonth = $(Get-Date).AddDays(-($(Get-Date).Day)+1)
$AutomationRGs = @("MyResourceGroupName1","MyResourceGroupName2")
$PropertyBags=@()
$newrunbooks = 0
$publishedrunbooks = 0
$editrunbooks = 0
$scriptrunbooks = 0
$graphrunbooks = 0
$powershellrunbooks = 0
$jobcountlastday = 0
$jobcountlastmonth = 0
$jobcountthismonth = 0
$jobminutesthismonth = 0
```
ForEach ($AutomationRG in $AutomationRGs) {
```powershell
$rmautomationacct = Get-AzureRmAutomationAccount -ResourceGroupName $AutomationRG
$newrunbooks += (Get-AzureRmAutomationRunbook -AutomationAccountName $rmautomationacct.AutomationAccountName -ResourceGroupName $AutomationRG `
```
| Where {$\_.State -eq "New"}).Count
```powershell
$publishedrunbooks += (Get-AzureRmAutomationRunbook -AutomationAccountName $rmautomationacct.AutomationAccountName -ResourceGroupName $AutomationRG `
```
| Where {$\_.State -eq "Published"}).Count
```powershell
$editrunbooks += (Get-AzureRmAutomationRunbook -AutomationAccountName $rmautomationacct.AutomationAccountName -ResourceGroupName $AutomationRG `
```
| Where {$\_.State -eq "Edit"}).Count
```powershell
$scriptrunbooks += (Get-AzureRmAutomationRunbook -AutomationAccountName $rmautomationacct.AutomationAccountName -ResourceGroupName $AutomationRG `
```
| Where {$\_.RunbookType -eq "Script"}).Count
```powershell
$graphrunbooks += (Get-AzureRmAutomationRunbook -AutomationAccountName $rmautomationacct.AutomationAccountName -ResourceGroupName $AutomationRG `
```
| Where {$\_.RunbookType -eq "Graph"}).Count
```powershell
$powershellrunbooks += (Get-AzureRmAutomationRunbook -AutomationAccountName $rmautomationacct.AutomationAccountName -ResourceGroupName $AutomationRG `
```
| Where {$\_.RunbookType -eq "PowerShell"}).Count
```powershell
$jobcountlastday += (Get-AzureRmAutomationJob -AutomationAccountName $rmautomationacct.AutomationAccountName -ResourceGroupName $AutomationRG `
```
-StartTime $afterdate\_lastday).Count
```powershell
$jobcountlastmonth += (Get-AzureRmAutomationJob -AutomationAccountName $rmautomationacct.AutomationAccountName -ResourceGroupName $AutomationRG `
```
-StartTime $afterdate\_lastmonth).Count
```powershell
$jobcountthismonth += (Get-AzureRmAutomationJob -AutomationAccountName $rmautomationacct.AutomationAccountName -ResourceGroupName $AutomationRG `
```
-StartTime $afterdate\_thismonth.ToLongDateString()).Count
```powershell
$jobsthismonth = Get-AzureRmAutomationJob -AutomationAccountName $rmautomationacct.AutomationAccountName -ResourceGroupName $AutomationRG `
```
-StartTime $afterdate\_thismonth.ToLongDateString() | Select-Object RunbookName, StartTime, EndTime, CreationTime, LastModifiedTime, @{Name='RunningTime';Expression={[TimeSpan]::Parse($\_.EndTime - $\_.StartTime).TotalMinutes}}, @{Name='Month';Expression={($\_.EndTime).Month}}
```powershell
$jobminutesthismonth += [int][Math]::Ceiling(($jobsthismonth | Measure-Object -Property RunningTime -Sum).Sum)
```
}
```powershell
$PropertyBag = $API.CreatePropertyBag()
$PropertyBag.AddValue("Instance", "Job Count Last Day")
$PropertyBag.AddValue("Value", [UInt32]$jobcountlastday)
$PropertyBags += $PropertyBag
```
"Job Count Last Day: " | Out-File $debuglog -Append
```powershell
$jobcountlastday | Out-File $debuglog -Append
$PropertyBag = $API.CreatePropertyBag()
$PropertyBag.AddValue("Instance", "Job Count Last Month")
$PropertyBag.AddValue("Value", [UInt32]$jobcountlastmonth)
$PropertyBags += $PropertyBag
```
"Job Count Last Month: " | Out-File $debuglog -Append
```powershell
$jobcountlastmonth | Out-File $debuglog -Append
$PropertyBag = $API.CreatePropertyBag()
$PropertyBag.AddValue("Instance", "Job Count This Month")
$PropertyBag.AddValue("Value", [UInt32]$jobcountthismonth)
$PropertyBags += $PropertyBag
```
"Job Count This Month: " | Out-File $debuglog -Append
```powershell
$jobcountthismonth | Out-File $debuglog -Append
$PropertyBag = $API.CreatePropertyBag()
$PropertyBag.AddValue("Instance", "Job Minutes This Month")
$PropertyBag.AddValue("Value", [UInt32]$jobminutesthismonth)
$PropertyBags += $PropertyBag
```
"Job Minutes This Month: " | Out-File $debuglog -Append
```powershell
$jobminutesthismonth | Out-File $debuglog -Append
$PropertyBag = $API.CreatePropertyBag()
$PropertyBag.AddValue("Instance", "Runbooks in New State")
$PropertyBag.AddValue("Value", [UInt32]$newrunbooks)
$PropertyBags += $PropertyBag
```
"Runbooks in New State: " | Out-File $debuglog -Append
```powershell
$newrunbooks | Out-File $debuglog -Append
$PropertyBag = $API.CreatePropertyBag()
$PropertyBag.AddValue("Instance", "Runbooks in Published State")
$PropertyBag.AddValue("Value", [UInt32]$publishedrunbooks)
$PropertyBags += $PropertyBag
```
"Runbooks in Published State: " | Out-File $debuglog -Append
```powershell
$publishedrunbooks | Out-File $debuglog -Append
$PropertyBag = $API.CreatePropertyBag()
$PropertyBag.AddValue("Instance", "Runbooks in Edit State")
$PropertyBag.AddValue("Value", [UInt32]$editrunbooks)
$PropertyBags += $PropertyBag
```
"Runbooks in Edit State: " | Out-File $debuglog -Append
```powershell
$editrunbooks | Out-File $debuglog -Append
$PropertyBag = $API.CreatePropertyBag()
$PropertyBag.AddValue("Instance", "PowerShell Workflow Runbooks")
$PropertyBag.AddValue("Value", [UInt32]$scriptrunbooks)
$PropertyBags += $PropertyBag
```
"PowerShell Workflow Runbooks: " | Out-File $debuglog -Append
```powershell
$scriptrunbooks | Out-File $debuglog -Append
$PropertyBag = $API.CreatePropertyBag()
$PropertyBag.AddValue("Instance", "Graphical Runbooks")
$PropertyBag.AddValue("Value", [UInt32]$graphrunbooks)
$PropertyBags += $PropertyBag
```
"Graphical Runbooks: " | Out-File $debuglog -Append
```powershell
$graphrunbooks | Out-File $debuglog -Append
$PropertyBag = $API.CreatePropertyBag()
$PropertyBag.AddValue("Instance", "PowerShell Script Runbooks")
$PropertyBag.AddValue("Value", [UInt32]$powershellrunbooks)
$PropertyBags += $PropertyBag
```
"PowerShell Script Runbooks: " | Out-File $debuglog -Append
```powershell
$powershellrunbooks | Out-File $debuglog -Append
$PropertyBags
```
} Catch {
"Error Catched: " | Out-File $debuglog -Append
```powershell
$($_.Exception.GetType().FullName) | Out-File $debuglog -Append
$($_.Exception.Message) | Out-File $debuglog -Append
```
}
PS! I have included debugging and logging in the script, be aware though that doing $ErrorActionPreference=Stop will end the script if any errors, for example with logging, so it might be an idea to remove the debug logging when confirmed that everything works.
In the next part I'm ready to create the PowerShell Script Rule.

## Creating the PowerShell Script Rule

In the Operations Console, under Authoring, create a new PowerShell Script Rule as shown below:

1. Select the PowerShell Script (Performance – OMS Bound) Rule:![](/uploads/2016/03/030416_1227_displayinga10.png)I have created a custom destination management pack for this script.
2. Specifying a Rule name and Rule Category: Performance Collection. As mentioned earlier in this article the Rule target will be the Root Management Server Emulator:![](/uploads/2016/03/030416_1227_displayinga11.png)
3. Selecting to run the script every 30 minutes, and at which time the interval will start from:![](/uploads/2016/03/030416_1227_displayinga12.png)
4. Selecting a name for the script file and timeout, and entering the complete script as shown earlier:![](/uploads/2016/03/030416_1227_displayinga13.png)
5. For the Performance Mapping information, the Object name must be in the \\FQDN\YourObjectName format. For FQDN I used the Target variable for PrincipalName, and for the Object Name AzureAutomationRunbookStats, and adding the "\\" at the start and "\" between: \\$Target/Host/Property[Type="MicrosoftWindowsLibrary7585010!Microsoft.Windows.Computer"]/PrincipalName$\AzureAutomationRunbookStatsI specified the Counter name as "Azure Automation Runbook Stats", and the Instance and Value are specified as $Data/Property(@Name='Instance')$ and $Data/Property(@Name=Value)$. These reflect the PropertyBag instance and value created in the PowerShell script:![](/uploads/2016/03/030416_1227_displayinga14.png)
6. After finishing the Create Rule Wizard, two new rules are created, which you can find by scoping to the Root Management Server Emulator I chose as target. Both Rules must be enabled, as they are not enabled by default:![](/uploads/2016/03/030416_1227_displayinga15.png)

At this point we are finished configuring the SCOM side, and can wait for some hours to see that data are actually coming into my OMS workspace.

## Looking at Azure Automation Runbook Stats Performance Data in OMS

After a while I will start seeing Performance Data coming into OMS with the specified Object and Counter Name, and for the different instances and values.
![](/uploads/2016/03/030416_1227_displayinga16.png)
In Log Search, I can specify Type=Perf ObjectName=AzureAutomationRunbookStats, and I will find the Results and Metrics for the specified time frame.
In the example above I'm highlighting the Job Minutes This Month counter, which will steadily increase for each month, and as we can see the highest value was 107 minutes, after when the month changed to March we were back at 0 minutes. After a while when the number of job minutes increases it will be interesting to follow whether this counter will go close to 500 minutes.
This way, I can now look at Azure Automation Runbook stats as performance data, showing different scenarios like how many jobs and runbook job minutes there are over a time period. I can also look at how what type of runbooks I have and what state they are in.
I can also create saved searches and alerts for my search criteria.

## Creating OMS Alerts for Azure Automation Runbook Counters

There is one specific scenario for Alerts I'm interested in, and that is when I'm approaching my monthly limit on 500 job minutes.
"Job Minutes This Month" is a counter that will get the sum of all job minutes for all runbook jobs across all automation accounts. In the classic Azure portal, you will have a usage overview like this:
![](/uploads/2016/03/030416_1227_displayinga17.png)
With OMS I would get this information over a time period like this:
![](/uploads/2016/03/030416_1227_displayinga18.png)
The search query for Job Minutes This Month as I have defined it via the PowerShell Script Rule in OMS is:
**Type=Perf ObjectName=AzureAutomationRunbookStats InstanceName="Job Minutes This Month"**
This would give me all results for the defined time period, but to generate an alert I would want to look at the most recent results, for example for the last hour. In addition, I want to filter the results for my alert when the number of job minutes are over the threshold of 450 which means I'm getting close to the limit of 500 free minutes per month. My query for this would be:
**Type=Perf ObjectName=AzureAutomationRunbookStats InstanceName="Job Minutes This Month" AND TimeGenerated>NOW-1HOUR AND CounterValue > 450**
Now, in my test environment, this will give med 0 results, because I'm currently at 37 minutes:
![](/uploads/2016/03/030416_1227_displayinga19.png)
Let's say, for sake of testing an Alert, I add criteria to include 37 minutes as well, like this:
![](/uploads/2016/03/030416_1227_displayinga20.png)
This time I have 2 results. Let's create an alert for this, press the ALERT button:
![](/uploads/2016/03/030416_1227_displayinga21.png)
For the alert I give it a name and base it on the search query. I want to check every 60 minutes, and generate alert when the number of results is greater than 1 so that I make sure the passing of the threshold is consistent and not just temporary.
![](/uploads/2016/03/030416_1227_displayinga22.png)
For actions I want an email notification, so I type in a Subject and my recipients.
![](/uploads/2016/03/030416_1227_displayinga23.png)
I Save the alert rule, and verify that it was successfully created.
![](/uploads/2016/03/030416_1227_displayinga24.png)
Soon I get my first alert on email:
![](/uploads/2016/03/030416_1227_displayinga25.png)
Now, that it works, I can remove the Alert and create a new one without the OR CounterValue=37, this I leave to you ;)
With that, this blog post is concluded. Thanks for reading, I hope this post on how to get more insights on your Azure Automation Runbook Stats in OMS and getting data via NRT Perfomance Collection has been useful ;)
