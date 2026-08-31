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

## Azure Static Web Apps setup

1. Create a Static Web App in your Azure subscription.
2. Connect it to this GitHub repository and `main` branch.
3. Add repository secret:
   - `AZURE_STATIC_WEB_APPS_API_TOKEN` (from SWA Deployment Token)
4. Push to `main` to trigger deployment.

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

Notes:

- Posts are written under `content/posts/`.
- Pages are written under `content/`.
- `wp-content/uploads` URLs are rewritten to `/uploads/`.
- After conversion, copy media files to `static/uploads/`.

### GitHub Actions workflow

Use `.github/workflows/wp-export-to-hugo.yml`:

1. Add your WordPress export file to `migration/wordpress-export.xml` (or another repo path).
2. Run the **Convert WordPress Export to Hugo** workflow from GitHub Actions.
3. Optional: let it auto-create a PR with converted content.
4. Review PR output and run final content cleanup.
