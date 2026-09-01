---
title: "How to use PowerShell script for setting Azure AD Password Reset Writeback On-premises Permissions"
date: 2017-02-09T14:42:21Z
draft: false
slug: "how-to-use-powershell-script-for-setting-azure-ad-password-reset-writeback-on-premises-permissions"
tags:
  - "Azure AD Premium"
categories:
  - "Automation"
  - "Enterprise Mobility + Security"
  - "PowerShell"
---

When you configure the Azure AD Premium Self Service Password Reset solution on your Azure AD tenant and then the Azure AD Connect Password Writeback feature, you will need to add permissions in your local Active Directory that permits the Azure AD Connect account to actually change and reset passwords for your users  , as detailed here: https://docs.microsoft.com/en-us/azure/active-directory/active-directory-passwords-getting-started#step-4-set-up-the-appropriate-active-directory-permissions.
I wrote this PowerShell script that helps you configure this correctly in your domain/forest. Some notes:

- You can use it in a single-domain, single-forest domain, or in a multi-domain forest, just remember to specify a Domain Controller for the wanted domain, and for the domain the Azure AD Connect account is in.
- You have to find the Azure AD Connect Synchronization account, it would be MSOL\_xxxx.. if you have used Express settings, or a dedicated account. Look at current configuration for details.
- You can specify an OU for your users, and if inheritance is enabled all subordinate users and OUs will inherit the permissions. If not, please run the script once for each OU you want the permissions to be applied for.

Here is the script:
https://gist.github.com/skillriver/32fb55b024767bfb5c65260714b1259a
Hope the script will be helpful!
