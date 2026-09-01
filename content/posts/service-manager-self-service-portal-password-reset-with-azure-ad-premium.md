---
title: "Service Manager Self Service Portal - Password Reset with Azure AD Premium"
date: 2015-06-29T14:09:55Z
draft: false
slug: "service-manager-self-service-portal-password-reset-with-azure-ad-premium"
tags:
  - "Azure"
  - "Azure AD Application Proxy"
  - "Azure AD Premium"
  - "Cireson"
  - "Self-Service Portal"
categories:
  - "Service Manager"
---

One challenge with using a Self Service Portal for Service Manager is that the user must have a valid Active Directory user name and password to be able to log on to the Self Service portal. So what do you do if have forgotten your password or the password has expired?
Previously in Service Manager, we have addressed this by having another user request a password reset on your behalf, that user being either a Service Desk analysts or a Super User allowed to create that password reset request.
The optimal solution would be to enable the user to reset their own password. This blog article will show how you can use Azure AD Premium to accomplish just that!

## Some requirements

First of all, this solution will have some requirements:

- You must have Azure AD with Directory Integration enabled for your on-premises Active Directory
- You must have configured password write-back to on-premises Active Directory![](/uploads/2015/06/062915_1406_servicemana1.png)
  ![](/uploads/2015/06/062915_1406_servicemana2.png)
- You must configure a user password reset policy in Azure AD, and users must at least have one authentication method defined:![](/uploads/2015/06/062915_1406_servicemana3.png)
- You must have either configured federated (SSO with ADFS) users or users with password synchronization in the directory integration set up
- Each user, and any administrator setting this up, needs to have an Azure AD Premium license. Azure AD Premium is either licensed directly or part of the Enterprise Mobility Suite (EMS)

## Some recommendations

In addition to the requirements above, I have some recommendations as well:

- Use the Azure AD Application Proxy to publish the Self Service Portal with Azure AD Pre-Authentication and Windows Integrated Authentication. This way the password reset request can be seamlessly integrated with the application URL the user are trying to access.
- For details on how to publish the Self Service Portal with Azure AD App Proxy, see my previous blog articles on this <https://systemcenterpoint.wordpress.com/2015/03/26/publish-the-cireson-self-service-portal-with-azure-ad-application-proxy/> and <https://systemcenterpoint.wordpress.com/2015/06/10/using-a-custom-domain-name-for-an-application-published-with-with-azure-ad-application-proxy/>.

## How this works

With all these requirements in place, this is how it works when a user tries to access the Self Service Portal and wants to reset the password.
In my environment, I am using the Self Service Portal from Cireson, but this should work for the built-in Service Manager Portal as well.

1. First, I go to my application URL, <https://selfservice.skill.no>. Since I have published this with Azure AD App Proxy, I must sign in with my hybrid Azure AD identity. I am presented with my customized Azure AD sign in page:![](/uploads/2015/06/062915_1406_servicemana4.png)
2. Since I have forgotten my password or maybe my password has expired, I select the link for "Can't access your account" under the Sign in button. This will bring me to the reset password page where I can specify my user identity and write the captcha code:![](/uploads/2015/06/062915_1406_servicemana5.png)
3. Next I select one of my defined authentication methods, in this example I will receive a text message to my mobile phone:![](/uploads/2015/06/062915_1406_servicemana6.png)
4. I receive the SMS verification code and type it in:![](/uploads/2015/06/062915_1406_servicemana7.png)
5. Next after successfully verifying my SMS code, I can specify my new password:![](/uploads/2015/06/062915_1406_servicemana8.png)
6. And my password has been reset:![](/uploads/2015/06/062915_1406_servicemana9.png)
7. Since my user are a federated user I will now be redirected back to the ADFS on-premises and my customized sign-in page there:![](/uploads/2015/06/062915_1406_servicemana10.png)
   ![](/uploads/2015/06/062915_1406_servicemana11.png)
8. After logging in, I'm redirected directly to the published Self Service Portal:![](/uploads/2015/06/062915_1406_servicemana12.png)

## Conclusion

By using the powers of Azure AD Premium and directory integration with my local Active Directory, I can as an end-user reset my passwords, and directly access my published Self Service Portal for Service Manager in this case.
PS! For those that are not in Azure AD yet, Cireson will soon deliver their own password reset solution in the Identity Management Stream. I'll come back to that later.
