---
title: "Blog Series – Redesigning an Operations Manager Service Level and Distributed Application because of empty Service Level Tracking Report"
date: 2013-10-21T22:37:30Z
draft: false
slug: "blog-series-redesigning-an-operations-manager-service-level-and-distributed-application-because-of-empty-service-level-tracking-report"
categories:
  - "Operations Manager"
---

This blog series consists of several blog posts, where I have redesigned an Operations Manager infrastructure with many Distributed Applications (DA) and Service Level Objectives (SLO). Some Distributed Applications contains other DAs, and the SLOs have these DAs as target as well as the top level DA, the "IT" Distributed Application.

A major part of this redesign have been going from a single unsealed Management Pack (MP) containing all the DAs, SLOs, Components and Overrides, to a design where I have been using several sealed Management Packs for the Distributed Applications, and using unsealed Management Packs for the Overrides and customizations.

This has been quite a bit of work, and the major reason for undertaking this work was this problem: "The Service Level Tracking Summary Report in System Center Operations Manager 2007 may be empty if TODAY is not selected for the TO date", as described in the KB <http://support.microsoft.com/kb/2567404>.

The reasons for why the Service Level Tracking Summary Report could be empty is well explained in the KB article, and this problem exist not only for Operations Manager 2007, but also for Operations Manager 2012 and 2012 SP1.

The possible resolutions are:

1. Seal MPs where you store SLOs.
2. Store SLOs separately (in separate MPs).
3. Increase the number of versions of the unsealed MP DW will preserve.

I found that increasing the number of MP versions in the DW would not be a satisfactory solution, and might not even be enough depending on how often the unsealed Management Pack have been updated. Moreover, if you have ALL the DAs, SLOs, Components and more in 1 big MP, you tend to get frequent updates over time as the infrastructure components you monitor are changing and you need to update the DAs and its components.

As for storing SLOs separately, you will not be able to do that if the SLOs are targeting DAs that are in an unsealed Management Pack, as the SLOs will forced to be saved in the same unsealed Management Pack as its targets.

So, at first hand it seemed I was left with the first resolution, to sealing my MP that not only consisted of the SLOs, but also all the Distributed Applications and its components.

Following this first introductory blog post, are the following blog articles:

- Part 1 – Sealing a Management Pack with Distributed Applications, components and references to other Management Packs
- Part 2 – Importing a Sealed MP with instance specific overrides fails
- Part 3 – How to Seal a Management Pack with Window Service monitors
- Part 4 – When Sealing a MP with Distributed Applications containing other DAs, they end up being Not Monitored
- Part 5 – Wrapping it up, sealing Management Packs with Distributed Applications containing other DAs, and sealing the SLOs targeting them

The links will be updated as soon as I have worked my way through the blog articles and published them. I hope this will be helpful for others, as I have learned a lot myself working through these.
