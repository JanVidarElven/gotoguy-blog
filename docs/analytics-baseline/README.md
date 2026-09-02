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
| `jetpack-stats-alltime-2026-08-31.png` | All-time views | 2013-09-01 to 2026-09-01 | 573,488 total views | Captured just before WordPress decommission |
| `jetpack-stats-alltime-2026-08-31.png` | All-time visitors | 2013-09-01 to 2026-09-01 | 427,829 total visitors | Captured just before WordPress decommission |
| `jetpack-stats-countries-2026-08-31.png` | Countries | 2013-09-01 to 2026-09-01 | 144,032 United States views, 56,872 United Kingdom views, 48,004 India views | Captured just before WordPress decommission |
| `jetpack-stats-top-posts-2026-08-31.png` | Top posts | 2013-09-01 to 2026-09-01 | 'Working with Azure AD extension attributes using PowerShell' 53,128 views | Captured just before WordPress decommission |
| `jetpack-stats-year-by-year-2026-08-31.png` | Year by Year 2013 | 2013-09-01 to 2013-12-31 | 37 views | Captured just before WordPress decommission |
| `jetpack-stats-year-by-year-2026-08-31.png` | Year by Year 2014 | 2014-01-01 to 2014-12-31 | 2,711 views | Captured just before WordPress decommission |
| `jetpack-stats-year-by-year-2026-08-31.png` | Year by Year 2015 | 2015-01-01 to 2015-12-31 | 10,097 views | Captured just before WordPress decommission |
| `jetpack-stats-year-by-year-2026-08-31.png` | Year by Year 2016 | 2016-01-01 to 2016-12-31 | 14,466 views | Captured just before WordPress decommission |
| `jetpack-stats-year-by-year-2026-08-31.png` | Year by Year 2017 | 2017-01-01 to 2017-12-31 | 46,608 views | Captured just before WordPress decommission |
| `jetpack-stats-year-by-year-2026-08-31.png` | Year by Year 2018 | 2018-01-01 to 2018-12-31 | 52,177 views | Captured just before WordPress decommission |
| `jetpack-stats-year-by-year-2026-08-31.png` | Year by Year 2019 | 2019-01-01 to 2019-12-31 | 56,423 views | Captured just before WordPress decommission |
| `jetpack-stats-year-by-year-2026-08-31.png` | Year by Year 2020 | 2020-01-01 to 2020-12-31 | 78,993 views | Captured just before WordPress decommission |
| `jetpack-stats-year-by-year-2026-08-31.png` | Year by Year 2021 | 2021-01-01 to 2021-12-31 | 93,429 views | Captured just before WordPress decommission |
| `jetpack-stats-year-by-year-2026-08-31.png` | Year by Year 2022 | 2022-01-01 to 2022-12-31 | 81,488 views | Captured just before WordPress decommission |
| `jetpack-stats-year-by-year-2026-08-31.png` | Year by Year 2023 | 2023-01-01 to 2023-12-31 | 69,844 views | Captured just before WordPress decommission |
| `jetpack-stats-year-by-year-2026-08-31.png` | Year by Year 2024 | 2024-01-01 to 2024-12-31 | 42,035 views | Captured just before WordPress decommission |
| `jetpack-stats-year-by-year-2026-08-31.png` | Year by Year 2025 | 2025-01-01 to 2025-12-31 | 16,522 views | Captured just before WordPress decommission |
| `jetpack-stats-year-by-year-2026-08-31.png` | Year by Year 2026 | 2026-01-01 to 2026-09-01 | 8,655 views | Captured just before WordPress decommission |

### Example row

| File | View | Date range shown | Key numbers | Notes |
|------|------|-------------------|-------------|-------|
| `jetpack-stats-alltime-2026-09-02.png` | All-time views | 2015-01-01 to 2026-09-02 | 128,430 total views | Captured just before WordPress decommission |
