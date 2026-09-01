# Work Routing

How to decide who handles what.

## Routing Table

| Work Type | Route To | Examples |
|-----------|----------|----------|
| Architecture, scope, backlog shaping | Lead | epics, trade-offs, sequencing, acceptance criteria |
| LoveIt theme, layouts, UX, accessibility | Frontend | menus, homepage, styling, taxonomy pages, responsive fixes |
| Azure hosting, GitHub Actions, deployment plumbing | Platform | SWA config, workflows, custom domains, Azure resources |
| Analytics instrumentation and reporting | Analytics | GA4 events, Search Console coverage, privacy analytics, dashboards |
| One-time WordPress migration and SEO preservation | Migration | WXR conversion, uploads, redirects, permalink mapping |
| Security posture and secrets hygiene | Security | repo hardening, Action secrets, headers, threat review |
| Regression, quality, release readiness | Reviewer | build validation, broken links, redirect checks, content QA |
| Runbooks, contributor docs, migration docs | Docs | operating procedures, setup docs, editorial workflow |

## Issue Routing

| Label | Action | Who |
|-------|--------|-----|
| `squad` | Triage: analyze issue, assign `squad:{member}` label | Lead |
| `squad:{name}` | Pick up issue and complete the work | Named member |

### How Issue Assignment Works

1. When a GitHub issue gets the `squad` label, the **Lead** triages it — analyzing content, assigning the right `squad:{member}` label, and commenting with triage notes.
2. When a `squad:{member}` label is applied, that member picks up the issue in their next session.
3. Members can reassign by removing their label and adding another member's label.
4. The `squad` label is the "inbox" — untriaged issues waiting for Lead review.

## Rules

1. **Eager by default** — spawn all agents who could usefully start work, including anticipatory downstream work.
2. **Scribe always runs** after substantial work, always as `mode: "background"`. Never blocks.
3. **Quick facts → coordinator answers directly.** Don't spawn an agent for "what port does the server run on?"
4. **When two agents could handle it**, pick the one whose domain is the primary concern.
5. **"Team, ..." → fan-out.** Spawn all relevant agents in parallel as `mode: "background"`.
6. **Anticipate downstream work.** If a feature is being built, spawn the tester to write test cases from requirements simultaneously.
7. **Issue-labeled work** — when a `squad:{member}` label is applied to an issue, route to that member. The Lead handles all `squad` (base label) triage.

## Work Type → Agent

| Work Type | Primary | Secondary |
|-----------|---------|----------|
| architecture | lead | docs |
| design | frontend | lead |
| frontend | frontend | reviewer |
| theme | frontend | reviewer |
| accessibility | frontend | reviewer |
| azure-platform | platform | security |
| deployment | platform | reviewer |
| github-actions | platform | security |
| analytics | analytics | docs |
| telemetry | analytics | platform |
| traffic-insights | analytics | docs |
| migration | migration | docs |
| redirects | migration | reviewer |
| seo | migration | frontend |
| security | security | lead |
| review | reviewer | security |
| documentation | docs | lead |
