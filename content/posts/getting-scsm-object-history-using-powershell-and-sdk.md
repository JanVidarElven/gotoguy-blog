---
title: "Getting SCSM Object History using PowerShell and SDK"
date: 2016-01-27T19:56:54Z
draft: false
slug: "getting-scsm-object-history-using-powershell-and-sdk"
categories:
  - "PowerShell"
  - "Service Manager"
---

Some objects in the Service Manager CMDB, does not have the History tab. For example for Active Directory Users:
[![image](/uploads/2016/01/image_thumb13.png "image")](/uploads/2016/01/image13.png)
This makes it more difficult to keep track of changes made by either the AD Connector or Relationship Changes.
Some years ago this blog post from Technet showed how you could access object history programmatically using the SDK and a Console Application: [http://blogs.technet.com/b/servicemanager/archive/2011/09/16/accessing-object-history-programmatically-using-the-sdk.aspx](http://blogs.technet.com/b/servicemanager/archive/2011/09/16/accessing-object-history-programmatically-using-the-sdk.aspx "http://blogs.technet.com/b/servicemanager/archive/2011/09/16/accessing-object-history-programmatically-using-the-sdk.aspx")
I thought I could accomplish the same using PowerShell and the SDK instead, so I wrote the following script based on the mentioned blog article:

```powershell
# Import module for Service Manager PowerShell CmdLets
$SMDIR    = (Get-ItemProperty 'hklm:/software/microsoft/System Center/2010/Service Manager/Setup').InstallDirectory
Set-Location -Path $SMDIR
If (!(Get-Module –Name “System.Center.Service.Manager”)) { Import-Module ".\Powershell\System.Center.Service.Manager.psd1" }

# Connect to Management Server
$EMG = New-Object Microsoft.EnterpriseManagement.EnterpriseManagementGroup "localhost"

# Specify Object Class
# In this example AD User
$aduserclass = Get-SCSMClass -DisplayName "Active Directory User"

# Get Instance of Class
$aduser = Get-SCSMClassInstance -Class $aduserclass | Where {$_.UserName -eq 'myusername'}

# Get History of Object Changes
$listhistory = $emg.EntityObjects.GetObjectHistoryTransactions($aduser)

# Loop History and Output to Console
ForEach ($emoht in $listhistory) {

    Write-Host "*************************************************************" -ForegroundColor Cyan
    Write-Host $emoht.DateOccurred `t $emoht.ConnectorDisplayName `t $emoht.UserName -ForegroundColor Cyan
    Write-Host "*************************************************************" -ForegroundColor Cyan

    ForEach ($emoh in $emoht.ObjectHistory) {

        If ($emoh.Values.ClassHistory.Count -gt 0) {
        
            Write-Host "*************************" -ForegroundColor Yellow
            Write-Host "Property Value Changes"  -ForegroundColor Yellow
            Write-Host "*************************"  -ForegroundColor Yellow

            ForEach ($emoch in $emoh.Values.ClassHistory) {
                ForEach ($propertyChange in $emoch.PropertyChanges) {
                    $propertyChange.GetEnumerator() | % {
                        Write-Host $emoch.ChangeType `t $_.Key `t $_.Value.First `t $_.Value.Second -ForegroundColor Yellow
                    }
                }
            }

        }
        
        If ($emoh.Values.RelationshipHistory.Count -gt 0) {

            Write-Host "*************************" -ForegroundColor Green
            Write-Host "Relationship Changes" -ForegroundColor Green
            Write-Host "*************************" -ForegroundColor Green

            ForEach ($emorh in $emoh.Values.RelationshipHistory) {

                $mpr = $emg.EntityTypes.GetRelationshipClass($emorh.ManagementPackRelationshipTypeId)
                Write-Host $mpr.DisplayName `t $emorh.ChangeType `t (Get-SCSMClassInstance -Id $emorh.SourceObjectId).DisplayName `t (Get-SCSMClassInstance -Id $emorh.TargetObjectId).DisplayName -ForegroundColor Green
            
            }

        }

    }

}
```


Running the script outputs the source of the changes, and any Property or Relationship changes, as shown in the below sample image:
[![image](/uploads/2016/01/image_thumb14.png "image")](/uploads/2016/01/image14.png)
