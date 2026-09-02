# Jetpack Stats historical baseline

This folder preserves a point-in-time snapshot of WordPress Jetpack Stats
before the blog moved to Hugo/Azure Static Web Apps with Umami and
Google Analytics. Jetpack Stats only exposes aggregated pageview/referrer
counts (not raw per-visit events), and there is no supported bulk export
or import path into GA4 or Umami. This baseline exists so the historical
traffic picture is not lost even though it cannot be technically migrated.

See the related decision record:
[.squad/decisions/inbox/analytics-add-umami-cloud-as-primary-analytics-keep-ga4-cons.md](/.squad/decisions/inbox/analytics-add-umami-cloud-as-primary-analytics-keep-ga4-cons.md)

## Naming convention

```
jetpack-stats-<view>-<date-captured>.png
```

- `<view>`: what the screenshot shows, e.g. `alltime`, `top-posts`,
  `yearly-summary`, `referrers`, `countries`.
- `<date-captured>`: the date (`YYYY-MM-DD`) the screenshot was taken,
  not the date range shown in the screenshot itself.

Examples:

- `jetpack-stats-alltime-2026-09-02.png`
- `jetpack-stats-top-posts-2026-09-02.png`
- `jetpack-stats-yearly-summary-2026-09-02.png`
- `jetpack-stats-referrers-2026-09-02.png`

Use PNG for all screenshots (avoids compression artifacts on dashboard
text/numbers).

## Captured snapshots

Fill in a row per screenshot added to this folder, so the numbers are
searchable without opening every image.

| File | View | Date range shown | Key numbers | Notes |
|------|------|-------------------|-------------|-------|
| _(add rows here)_ | | | | |

### Example row

| File | View | Date range shown | Key numbers | Notes |
|------|------|-------------------|-------------|-------|
| `jetpack-stats-alltime-2026-09-02.png` | All-time views | 2015-01-01 to 2026-09-02 | 128,430 total views | Captured just before WordPress decommission |
