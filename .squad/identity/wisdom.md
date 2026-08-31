---
last_updated: 2026-08-31T07:40:58.328Z
---

# Team Wisdom

Reusable patterns and heuristics learned through work. NOT transcripts — each entry is a distilled, actionable insight.

## Patterns

<!-- Append entries below. Format: **Pattern:** description. **Context:** when it applies. -->

**Pattern:** Treat WordPress migration as repeatable batches: export content, convert to Markdown, review output, import media, then validate redirects. **Context:** one-time migration and any future re-imports.

**Pattern:** Pin Hugo and theme versions deliberately and verify compatibility before changing either. **Context:** LoveIt and Hugo version mismatches can break local preview and CI quickly.

**Pattern:** Keep generated migration artifacts and raw WordPress exports out of git unless intentionally sanitized. **Context:** public blog repo hygiene and secret/content leak prevention.

**Pattern:** Route Azure Static Web Apps, GitHub Actions, and deployment-token work through the platform and security agents together. **Context:** infrastructure changes that touch both delivery and risk.
