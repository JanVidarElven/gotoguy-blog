# GoToGuy Blog (Hugo + Azure Static Web Apps)

This repository is ready for a WordPress-to-Hugo migration with:

- Hugo static site generation
- LoveIt theme
- Markdown-first content
- Azure Static Web Apps hosting
- GitHub Actions CI/CD on every push

## Current defaults

- Production URL: `https://gotoguy.blog/`
- Theme: `LoveIt`
- Post permalink format: `/:year/:month/:day/:slug/`
- Build command: `hugo --minify`
- Build output: `public/`

## Repository layout

- `config.toml`: Hugo site settings and permalinks
- `themes/LoveIt/`: Git submodule for the active Hugo theme
- `content/posts/`: Blog posts in Markdown
- `content/about.md`: Static page example
- `content/speaking.md`: Speaking page backed by Sessionize data
- `data/sessionize/speaking_history.json`: Generated speaking session data
- `static/`: Static assets
- `.github/workflows/deploy-swa.yml`: CI/CD pipeline for SWA
- `.github/workflows/refresh-speaking-history.yml`: Manual refresh of speaking history
- `staticwebapp.config.json`: SWA routing, headers, and legacy redirects

## Local development

1. Install Hugo extended.
2. Run:

   ```bash
   git submodule update --init --recursive
   hugo server -D --disableFastRender
   ```

3. Open `http://localhost:1313`.

## Speaking history refresh

Refresh the speaking page data locally:

```bash
python scripts/fetch_sessionize_speaking_history.py
```

Or run the **Refresh speaking history** workflow in GitHub Actions to update it from your public Sessionize profile.

## Squad setup for blog operations

This repository is initialized for [Squad](https://github.com/bradygaster/squad) and includes a specialized team under [.squad/](C:/_Repos/GitHub-JanVidarElven/gotoguy-blog/.squad):

- `lead`: product and technical coordination
- `frontend`: LoveIt theme, UX, and accessibility
- `platform`: Azure Static Web Apps, GitHub Actions, and backend-facing Azure work
- `analytics`: traffic analytics, telemetry instrumentation, and reporting insights
- `migration`: WordPress conversion, redirects, media, and SEO continuity
- `security`: secrets, permissions, and hardening
- `reviewer`: validation and regression review
- `docs`: runbooks and contributor guidance

### Start using Squad locally

```bash
npx @bradygaster/squad-cli doctor
copilot --agent squad --additional-mcp-config @.mcp.json --yolo
```

Or in VS Code Copilot Chat, select the **Squad** agent directly. The repo includes [settings.json](C:/_Repos/GitHub-JanVidarElven/gotoguy-blog/.vscode/settings.json) to make new chat sessions default to Squad mode.

Then describe the work naturally, for example:

- `Team, plan the remaining WordPress migration tasks.`
- `frontend, improve the homepage and taxonomy navigation.`
- `platform, validate Azure Static Web Apps deployment and custom domain setup.`
- `analytics, set up GA4 and Search Console migration baseline tracking.`
- `migration, review converted posts and generate redirects for old WordPress URLs.`

### GitHub issue flow

- Add the `squad` label to an issue to send it to triage.
- The Squad triage workflow applies a `squad:{member}` label based on the issue content.
- Pushes to [.squad/team.md](C:/_Repos/GitHub-JanVidarElven/gotoguy-blog/.squad/team.md) sync labels automatically.
- Use [.github/ISSUE_TEMPLATE/analytics-instrumentation-and-reporting.md](C:/_Repos/GitHub-JanVidarElven/gotoguy-blog/.github/ISSUE_TEMPLATE/analytics-instrumentation-and-reporting.md) to open structured analytics backlog items for `squad:analytics`.

## Analytics rollout checklist

### Create the GA4 property

1. In Google Analytics, open **Admin** and create a property for GoToGuy Blog.
2. Set the reporting timezone and currency.
3. Under **Data collection and modification**, open **Data streams** and add a Web stream for `https://gotoguy.blog/`.
4. Enable enhanced measurement for page views, scrolls, outbound clicks, and file downloads.
5. Copy the Measurement ID (`G-...`).
6. In the GitHub repository, open **Settings > Secrets and variables > Actions > Variables** and create:
   - Name: `GA4_MEASUREMENT_ID`
   - Value: the `G-...` Measurement ID

The Measurement ID is injected only for pushes to `main`. Pull-request previews and normal local development do not load GA4.

GA4 is also consent-gated: it is not downloaded and does not collect data until the visitor selects **Allow analytics**. The behavior and stored consent value are described on the `/privacy/` page.

### Configure Google Search Console

1. Add a Domain property for `gotoguy.blog` in Google Search Console.
2. Add the provided DNS TXT verification record at the domain apex and retain it after verification.
3. Submit `https://gotoguy.blog/sitemap.xml`.
4. Inspect representative homepage, post, category, and tag URLs.
5. Monitor indexing, canonical selection, Core Web Vitals, clicks, impressions, CTR, and average position.

No Search Console Change of Address request is needed because the domain remains the same.

### Validate analytics

For a deliberate local production-mode test, use a test Measurement ID:

```powershell
$env:HUGO_PARAMS_ANALYTICS_GOOGLE_ID = "G-XXXXXXXXXX"
hugo server --environment production
```

Before consent, confirm no request is made to `googletagmanager.com`. After allowing analytics, validate the tag using Google Tag Assistant and GA4 Realtime or DebugView.

### Migration baseline

Use this sequence during and after cutover:

1. Capture users, sessions, views, engagement rate, and average engagement time.
2. Compare top landing pages before and after cutover.
3. Monitor organic clicks, impressions, CTR, and average position.
4. Monitor 404s and redirect behavior during the first 30 days.

## Azure Static Web Apps setup

1. Create a Static Web App in your Azure subscription.
2. Connect it to this GitHub repository and `main` branch.
3. Add repository secret:
   - `AZURE_STATIC_WEB_APPS_API_TOKEN` (from SWA Deployment Token)
4. Push to `main` to trigger deployment.

### Deploy the Static Web App with Bicep

Infrastructure-as-code files are under [infra/azure-swa/](C:/_Repos/GitHub-JanVidarElven/gotoguy-blog/infra/azure-swa).

1. Update [main.bicepparam](C:/_Repos/GitHub-JanVidarElven/gotoguy-blog/infra/azure-swa/main.bicepparam) with your preferred name/location/tags.
2. Deploy to your target resource group:

```bash
az deployment group create \
  --resource-group <your-resource-group> \
  --parameters infra/azure-swa/main.bicepparam
```

3. Retrieve deployment token and add it as GitHub repository secret `AZURE_STATIC_WEB_APPS_API_TOKEN`:

```bash
az staticwebapp secrets list \
  --name <your-static-web-app-name> \
  --resource-group <your-resource-group> \
  --query "properties.apiKey" \
  --output tsv
```

4. Keep this repo's existing workflow [deploy-swa.yml](C:/_Repos/GitHub-JanVidarElven/gotoguy-blog/.github/workflows/deploy-swa.yml) unchanged: it already deploys the Hugo `public/` folder using that token.

## WordPress migration checklist

1. Export WordPress XML (`Tools > Export`).
2. Copy media from `wp-content/uploads`.
3. Convert posts/pages to Markdown with front matter.
4. Keep slugs aligned to preserve URLs.
5. Add any additional route redirects to `staticwebapp.config.json`.

## Automated WordPress export conversion

### Script (local)

Use `scripts/wp_export_to_hugo.py` to convert a WordPress WXR XML export into Hugo content files.

Example:

```bash
python scripts/wp_export_to_hugo.py \
  --xml migration/wordpress-export.xml \
  --output content \
  --include-pages \
  --overwrite
```

If your media export is a zip archive with year/month folders such as `2024/04/image.png`, extract it directly into `static/uploads/`:

```bash
python scripts/wp_export_to_hugo.py \
  --xml migration/wordpress-export.xml \
  --output content \
  --include-pages \
  --media-zip migration/media-export.zip \
  --media-output static/uploads \
  --overwrite
```

Notes:

- Posts are written under `content/posts/`.
- Pages are written under `content/`.
- `wp-content/uploads` URLs are rewritten to `/uploads/`.
- WordPress heading tags, lists, and inline code are converted into Hugo markdown where possible.
- Media archives are extracted while preserving year/month folder structure.

### GitHub Actions workflow

Use `.github/workflows/wp-export-to-hugo.yml`:

1. Add your WordPress export file to `migration/wordpress-export.xml` (or another repo path).
2. Run the **Convert WordPress Export to Hugo** workflow from GitHub Actions.
3. Optional: let it auto-create a PR with converted content.
4. Review PR output and run final content cleanup.
