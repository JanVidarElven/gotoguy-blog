---
title: "Welcome to the New Home of GoToGuy Blog"
date: 2026-09-01T22:54:00+02:00
draft: false
slug: "welcome-to-the-new-home-of-gotoguy-blog"
tags: ["hugo", "azure", "github-actions", "wordpress", "squad"]
categories: ["meta"]
---

Welcome to the new home of GoToGuy Blog!

For many years this blog lived on WordPress. It gave me a place to share technical articles, scripts, conference experiences, and lessons learned from working with Microsoft cloud, identity, security, automation, and management technologies. WordPress served the blog well, but over time I wanted a platform that was simpler to maintain, easier to automate, and better aligned with the tools I use in my daily work.

The result is the site you are reading now: a static blog built from Markdown, stored in GitHub, and deployed to Azure.

## Why I moved from WordPress

The main goal was to make the blog content portable and keep the publishing workflow close to source control. Instead of writing content into a database-backed content management system, every article is now a Markdown file in a Git repository.

This gives me:

- Version history for every post and configuration change
- Pull requests and reviews for larger updates
- A local preview before publishing
- Automated builds and deployments
- Less infrastructure to operate and patch
- Content that is easy to search, edit, reuse, and migrate again if needed

The public URL remains `https://gotoguy.blog/`, so the new platform changes how the site is built and operated without changing where readers find it.

## How the new blog is built

The site is generated with [Hugo](https://gohugo.io/), a fast static site generator. Hugo turns the Markdown content, templates, configuration, and static files in the repository into the HTML pages that make up the finished site.

The visual design is based on the [LoveIt](https://github.com/dillonzq/LoveIt) theme, with local configuration and template overrides for this blog.

The main technologies are:

- **Hugo** for static site generation
- **Markdown** for posts and pages
- **LoveIt** for the Hugo theme and presentation
- **GitHub** for source control and collaboration
- **GitHub Actions** for continuous integration and deployment
- **Azure Static Web Apps** for hosting, TLS, preview environments, and the custom domain
- **Bicep** for deploying the Azure infrastructure as code

Every push to the main branch starts a GitHub Actions workflow. The workflow installs Hugo, builds and minifies the site, and then deploys the generated output to Azure Static Web Apps. Pull requests can also receive their own preview environments, making it possible to review changes before they reach the production site.

## How the content was migrated

The migration started with a WordPress WXR XML export containing the existing posts, pages, dates, slugs, categories, tags, and article content. A migration script converted the WordPress HTML into Hugo Markdown and generated front matter for each page.

The process included more than simply copying text:

- WordPress headings were converted into Markdown headings
- Code snippets from several generations of WordPress editors were identified and rebuilt as fenced code blocks
- Languages such as PowerShell, Bicep, JSON, Kusto, JavaScript, HTML, HTTP, Bash, and Power Fx were detected for syntax highlighting
- The WordPress media export was unpacked into Hugo's static assets while preserving its year and month folders
- Image references were rewritten from WordPress upload URLs to their new static paths
- Existing dates and slugs were preserved to maintain familiar URLs
- Redirects, feeds, metadata, and SEO continuity were reviewed for the platform cutover

The result is that the existing archive remains available, but the source is now open, readable Markdown rather than content locked inside a WordPress database.

## Working with an AI Squad

Another important part of this migration has been the use of [Squad](https://github.com/bradygaster/squad), created by Brady Gaster. Squad provides a persistent team of specialized AI agents that work with the repository and its project context.

Instead of relying on one general assistant for every task, the project has specialists for:

- Product and technical coordination
- Frontend design, Hugo, and accessibility
- Azure infrastructure and GitHub Actions
- WordPress migration, redirects, and SEO
- Security and secrets hygiene
- Analytics and traffic insights
- Quality review and release readiness
- Documentation and operational runbooks

The team helps plan work, route issues to the right specialist, implement and review changes, and preserve decisions in the repository. The migration still remains human-led: I decide the direction, review the output, and control what is committed and deployed. Squad provides focused assistance and orchestration around those decisions.

## Building the new home through conversation

The migration was also developed interactively with an AI assistant using the Copilot CLI runtime in Visual Studio Code. Rather than beginning with a complete specification, I could describe what I wanted, ask questions, review the result, and then refine the solution step by step.

The assistant helped throughout the project by:

- Discussing the security implications of keeping the blog repository public
- Explaining how to preview and troubleshoot Hugo locally
- Configuring and adapting the LoveIt theme
- Diagnosing a Hugo live-rebuild failure caused by a theme template assumption
- Adding my profile, social links, and Sessionize-powered speaking history
- Planning the WordPress migration and building the conversion workflow
- Investigating differences between old and new WordPress code snippet formats
- Improving heading, image, code fence, and syntax-language conversion
- Configuring sharing options and cleaning up theme output
- Comparing hosting and analytics alternatives
- Adding an analytics specialist to Squad
- Creating the Bicep template for Azure Static Web Apps
- Diagnosing an Azure preflight validation error and validating the corrected deployment
- Helping manage Git history when a large media archive prevented a push
- Running Hugo builds and other validation checks after changes

This conversational approach was especially useful when the migration uncovered unexpected problems. I could provide an error message or point to a page that did not render correctly, and the assistant could inspect the repository, identify the likely cause, implement a focused fix, and verify the result. That made the process iterative and practical rather than a one-time generated migration.

The conversation also became part of the project's working context. Earlier decisions, requirements, errors, and corrections informed later changes, while Squad gave those tasks clearer ownership across migration, platform, frontend, security, analytics, documentation, and review.

## What comes next

Moving the blog is not only about preserving the old content. The new platform creates a foundation for publishing new articles, improving navigation and accessibility, monitoring traffic and search performance, and evolving the site through reviewable changes.

Thank you for following GoToGuy Blog to its new home. The technology underneath has changed, but the purpose remains the same: sharing practical experiences, technical solutions, and lessons learned with the community.
