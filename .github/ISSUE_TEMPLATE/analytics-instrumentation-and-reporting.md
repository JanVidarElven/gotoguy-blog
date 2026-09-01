---
name: Analytics instrumentation and reporting
about: Plan, implement, and verify blog analytics for migration and ongoing operations
title: "analytics: "
labels: ["squad", "squad:analytics", "go:needs-research"]
assignees: []
---

## Goal

Describe what decision this analytics work should support (for example: validating migration traffic parity, measuring post engagement, or tracking newsletter conversions).

## Scope

- [ ] GA4 setup/update
- [ ] Google Search Console setup/update
- [ ] Privacy-friendly analytics decision (Plausible/Umami/none)
- [ ] Hugo instrumentation changes
- [ ] Dashboard/reporting changes
- [ ] QA and verification

## Implementation checklist

### GA4
- [ ] Confirm property and data stream IDs
- [ ] Add/validate tracking script in Hugo layout
- [ ] Define required events (for example: outbound link click, newsletter click, contact action)
- [ ] Validate events in GA4 Realtime and DebugView

### Search Console
- [ ] Verify domain or URL-prefix property
- [ ] Submit sitemap URL (`/sitemap.xml`)
- [ ] Confirm indexing coverage and no critical crawl errors
- [ ] Capture baseline metrics (clicks, impressions, CTR, average position)

### Privacy-friendly analytics (optional)
- [ ] Decide platform (Plausible, Umami, or skip)
- [ ] Add script/config if enabled
- [ ] Confirm pageview collection and referrer tracking
- [ ] Document retention/privacy settings

### Migration KPI baseline (first 30 days)
- [ ] Define baseline period and compare window
- [ ] Track top landing pages before/after cutover
- [ ] Track 404 rate and redirect hit trends
- [ ] Track organic traffic trend vs WordPress baseline

## Validation checklist

- [ ] `hugo --minify` succeeds
- [ ] `hugo server -D --disableFastRender` renders pages without analytics layout errors
- [ ] Tracking appears on production pages after deployment
- [ ] At least one test event per required type is captured
- [ ] Notes/screenshots added to issue

## Deliverables

- [ ] PR with instrumentation/config changes
- [ ] Short runbook update for analytics maintenance
- [ ] Initial dashboard/report link(s)

## Notes for triage

Expected owner: `squad:analytics`  
Secondary reviewers when needed: `squad:platform` (deployment), `squad:security` (privacy/security review), `squad:docs` (runbook updates)
