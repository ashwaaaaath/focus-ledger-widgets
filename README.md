# 🕯️ Focus Ledger Widgets

Custom embeddable widgets for my Notion Focus Ledger page. Hosted on GitHub Pages — clean, no banners.

## Widgets

| Widget | File | Description |
|--------|------|-------------|
| 🕯️ Banner | `banner.html` | Animated header with candle glow, floating particles, live date/time |
| 📊 Stats Dashboard | `stats.html` | Live focus analytics synced from Notion every 30 min |
| 💬 Quote | `quote.html` | Rotating focus/productivity quotes with click-to-refresh |
| ⏱️ Focus Timer | `timer.html` | Pomodoro-style timer with 25/45/90 min modes and session tracking |

## Setup: Connect Stats to Notion

The stats dashboard pulls live data from your Deep Work Ledger via GitHub Actions.

### One-time setup:

1. Go to this repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `NOTION_API_KEY`
4. Value: Your Notion integration API key (starts with `ntn_` or `secret_`)
5. Make sure the integration has access to the Focus Ledger page in Notion (Settings → Connections → Add your integration)
6. Go to the **Actions** tab and manually run the "Sync Notion Data" workflow to test

The workflow runs every 30 minutes and updates `data.json`, which the stats widget reads.

## How to Embed in Notion

1. In Notion, type `/embed` and press Enter
2. Paste the widget URL (e.g. `https://ashwaaaaath.github.io/focus-ledger-widgets/banner.html`)
3. Click **Embed link**
4. Resize the embed block to fit

## Customization

Edit any `.html` file, push to `main`, and GitHub Pages auto-deploys. Notion embeds update on refresh.
