# 🕯️ Focus Ledger Widgets

Custom embeddable widgets for my Notion Focus Ledger page. Hosted on GitHub Pages for clean, banner-free embedding.

## Widgets

| Widget | File | Description |
|--------|------|-------------|
| 🕯️ Banner | `banner.html` | Animated header with candle glow, floating particles, live date/time |
| 📊 Stats Dashboard | `stats.html` | Focus analytics with bar charts, donut chart, heatmap, streak tracker |
| 💬 Quote | `quote.html` | Rotating focus/productivity quotes with click-to-refresh |
| ⏱️ Focus Timer | `timer.html` | Pomodoro-style timer with 25/45/90 min modes and session tracking |

## How to Embed in Notion

1. Enable GitHub Pages (Settings → Pages → Deploy from branch → `main` → Save)
2. Your widgets will be live at: `https://<username>.github.io/focus-ledger-widgets/<widget>.html`
3. In Notion, type `/embed` and paste the widget URL
4. Resize the embed block to fit your layout

## Recommended Embed Sizes

- **Banner**: Full width, ~200px tall
- **Stats Dashboard**: Full width, ~380px tall
- **Quote**: Full width, ~140px tall
- **Focus Timer**: Half width or full width, ~140px tall

## Customization

All widgets use a warm/cozy color palette (#1a1410 dark bg, #c9956b gold accent). Edit the CSS variables to match your style.

### Connecting Real Data (Stats Dashboard)

The stats widget currently shows demo data. To connect it to your Notion database:

1. Use [ChartBase](https://notion2charts.com) (free) to create charts from your Deep Work Ledger database
2. Or use the Notion API to fetch data and update the `demoData` object in `stats.html`
