---
title: "Shut Down Azure Servers for Earth Hour – 2015 Edition"
date: 2015-03-28T19:40:19Z
draft: false
slug: "shut-down-azure-servers-for-earth-hour-2015-edition"
tags:
  - "Azure"
  - "SQL Server"
categories:
  - "Automation"
  - "PowerShell"
---

One year ago, I published a blog article for shutting down, and later restart again, Azure Servers for one hour duration during Earth Hour 2014: <https://systemcenterpoint.wordpress.com/2014/03/28/earth-hour-how-to-shut-down-and-restart-your-windows-azure-services-with-automation/>.
In that article, I used three different Automation technologies to accomplish that:

- Scheduled PowerShell script
- System Center 2012 R2 Orchestrator
- Service Management Automation in Windows Azure Pack

Today is Earth Hour 2015 ([www.earthhour.org](http://www.earthhour.org)). While the Automation technologies referred still can be used for shutting down and restarting Azure Servers, I thought I should create an updated blog article using Azure Automation that has been launched during the last year.
This new example are built on the following:

1. An Azure SQL Database with a table for specifying which Cloud Services and VM Names that should be shut down during Earth Hour
2. An Azure Automation Runbook which connects to the Azure SQL Database, reads the Servers specified and shuts them down one by one (or later starts them up one by one).
3. Two Schedules, one that triggers when the Earth Hour starts and one that triggers when Earth Hour begins, and calls the Runbook.

Creating a Azure SQL Database or a SQL Server is outside the scope of this article, but the table I have created is defined like this:
CREATE TABLE dbo.EarthHourServices 
( 
    ID int NOT NULL, 
    CloudService varchar(50) NULL, 
    VMName varchar(50) NULL, 
    StayProvisioned bit NULL, 
 CONSTRAINT PK\_ID PRIMARY KEY (ID) 
) 
GO 
The StayProvisioned is a boolean data value where I can specify if VM's should only be stopped, or stopped and deallocated.
This table is then filled with values for the servers I want to stop.
The Azure Automation Runbook I want to create have some requirements:

1. I need to create a PowerShell Credential Asset for the SQL Server username and password
2. I need to be able to Connect to my Azure Subscription. Previously I have been using the Connect-Azure solution (<https://gallery.technet.microsoft.com/scriptcenter/Connect-to-an-Azure-f27a81bb>) for connecting to my specified Azure Subscription. This is still working and I'm using this method in this blog post, but now depreciated and you should use this guide instead: <http://azure.microsoft.com/blog/2014/08/27/azure-automation-authenticating-to-azure-using-azure-active-directory/>.

This is the Runbook I have created:

```powershell
workflow EarthHour_StartStopAzureServices
{
    param
    (
        # Fully-qualified name of the Azure DB server 
        [parameter(Mandatory=$true)] 
        [string] $SqlServerName,
        # Credentials for $SqlServerName stored as an Azure Automation credential asset
        [parameter(Mandatory=$true)] 
        [PSCredential] $SqlCredential,
        # Action, either Start or Stop for the specified Azure Services 
        [parameter(Mandatory=$true)] 
        [string] $Action
    )

    # Specify Azure Subscription Name
    $subName = 'My Azure Subscription'
    # Connect to Azure Subscription
    Connect-Azure `
        -AzureConnectionName $subName
    Select-AzureSubscription `
        -SubscriptionName $subName 

    inlinescript
    {

        # Setup credentials   
        $ServerName = $Using:SqlServerName
        $UserId = $Using:SqlCredential.UserName
        $Password = ($Using:SqlCredential).GetNetworkCredential().Password
        
        # Create connection to DB
        $Database = "SkillAutomationRepository"
        $DatabaseConnection = New-Object System.Data.SqlClient.SqlConnection
        $DatabaseConnection.ConnectionString = "Server = $ServerName; Database = $Database; User ID = $UserId; Password = $Password;"
        $DatabaseConnection.Open();

        # Get Table
        $DatabaseCommand = New-Object System.Data.SqlClient.SqlCommand
        $DatabaseCommand.Connection = $DatabaseConnection
        $DatabaseCommand.CommandText = "SELECT ID, CloudService, VMName, StayProvisioned FROM EarthHourServices"
        $DbResult = $DatabaseCommand.ExecuteReader()

        # Check if records are returned from SQL database table and loop through result set
        If ($DbResult.HasRows)
        {
            While($DbResult.Read())
            {
                # Get values from table
                $CloudService = $DbResult[1]
                $VMname = $DbResult[2]
                [bool]$StayProvisioned = $DbResult[3] 
 
                 # Check if we are starting or stopping the specified services
                If ($Using:Action -eq "Stop") {

                    Write-Output "Stopping: CloudService: $CloudService, VM Name: $VMname, Stay Provisioned: $StayProvisioned"
                
                    $vm = Get-AzureVM -ServiceName $CloudService -Name $VMname
                    
                    If ($vm.InstanceStatus -eq 'ReadyRole') {
                        If ($StayProvisioned -eq $true) {
                            Stop-AzureVM -ServiceName $vm.ServiceName -Name $vm.Name -StayProvisioned
                        }
                        Else {
                            Stop-AzureVM -ServiceName $vm.ServiceName -Name $vm.Name -Force
                        }
                    }
                                       
                }
                ElseIf ($Using:Action -eq "Start") {

                    Write-Output "Starting: CloudService: $CloudService, VM Name: $VMname, Stay Provisioned: $StayProvisioned"

                    $vm = Get-AzureVM -ServiceName $CloudService -Name $VMname
                    
                    If ($vm.InstanceStatus -eq 'StoppedDeallocated' -Or $vm.InstanceStatus -eq 'StoppedVM') {
                        Start-AzureVM -ServiceName $vm.ServiceName -Name $vm.Name    
                    }
                     
                }
 
            }
        }

        # Close connection to DB
        $DatabaseConnection.Close() 
    }    

}
```

And this is my schedules which will run the Runbook when Earth Hour Begins and Ends. The Scedules specify the parameters I need to connect to Azure SQL and the Action for either Stop VM's or Start VM's.
![](/uploads/2015/03/032815_1934_shutdownazu1.png)
Good luck with automating your Azure Servers and remember to turn off the lights as well J!
