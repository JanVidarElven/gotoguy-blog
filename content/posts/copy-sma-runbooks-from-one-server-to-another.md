---
title: "Copy SMA Runbooks from one Server to another"
date: 2015-03-06T13:52:31Z
draft: false
slug: "copy-sma-runbooks-from-one-server-to-another"
tags:
  - "Azure"
categories:
  - "Automation"
  - "PowerShell"
  - "SMA"
  - "WAP"
---

Recently I decided to scrap my old Windows Azure Pack environment and create a new environment for Windows Azure Pack partly based in Microsoft Azure. As a part of this reconfiguration I have set up a new SMA server, and wanted to copy my existing SMA runbooks from the old Server to the new Server.
This little script did the trick for me, hope it can be useful for others as well.

```powershell
# Specify old and new SMA servers
$OldSMAServer = "myOldSMAServer"
$NewSMAServer = "myNewSMAServer"

# Define export directory
$exportdir = 'C:\_Source\SMARunbookExport\'

# Get which SMA runbooks I want to export, filtered by my choice of tags
$sourcerunbooks = Get-SmaRunbook -WebServiceEndpoint https://$OldSMAServer | Where { $_.Tags -iin ('Azure','Email','Azure,EarthHour','EarthHour,Azure')}

# Loop through and export definition to file, on for each runbook
foreach ($rb in $sourcerunbooks) {
    $exportrunbook = Get-SmaRunbookDefinition -Type Draft -WebServiceEndpoint https://$OldSMAServer -name $rb.RunbookName
    $exporttofile = $exportdir + $rb.RunbookName + '.txt'
    $exportrunbook.Content | Out-File $exporttofile
}

# Then loop through and import to new SMA server, keeping my tags
foreach ($rb in $sourcerunbooks) {
    $importfromfile = $exportdir + $rb.RunbookName + '.txt'
    Import-SmaRunbook -Path $importfromfile -WebServiceEndpoint https://$NewSMAServer -Tags $rb.Tags
}

# Check my new SMA server for existence of the imported SMA runbooks
Get-SmaRunbook -WebServiceEndpoint https://$NewSMAServer |  FT RunbookName, Tags
```
