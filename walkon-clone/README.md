# WalkOn Clone - Liverpool News Aggregator

A self-hosted alternative to Newsfinity-powered Liverpool FC news aggregation.

## Features

- **Live News Aggregation** - Pulls from RSS feeds (Liverpool Echo, etc.)
- **Auto-categorization** - Tags articles as Transfer News, Injury News, Match Previews, WSL
- **Time-based Sections** - Shows articles by age (30min, 1hr, 2hr)
- **Clean Design** - Mobile-responsive, similar to original WalkOn
- **No Monthly Fees** - Runs on your own server

## Quick Start

### Option 1: Static (No Backend)

1. Copy `index.html` to any web server
2. Manually update the JSON data in the `<script>` section
3. Deploy!

### Option 2: Python Scraper

```bash
# Install dependencies (if needed)
pip install requests feedparser

# Run the scraper
python3 scraper.py

# This creates news-data.json with latest articles
```

Then update `index.html` to load `news-data.json` instead of hardcoded data.

## RSS Feed Sources

- **Liverpool Echo**: `https://www.liverpoolecho.co.uk/sport/football/?service=rss`
- **Sky Sports (search results)**: Various team-specific feeds

## Adding More Sources

Edit `scraper.py` and add to `RSS_FEEDS`:

```python
{
    "name": "Your Source",
    "url": "https://example.com/rss.xml",
    "filter_keywords": ["Liverpool"]
}
```

## Automation (Cron Job)

Run the scraper every 15 minutes:

```bash
# Edit crontab
crontab -e

# Add this line
*/15 * * * * /usr/bin/python3 /path/to/walkon-clone/scraper.py
```

## File Structure

```
walkon-clone/
├── index.html      # Main frontend
├── scraper.py      # Python RSS scraper
├── news-data.json  # Generated news data
└── README.md       # This file
```

## Tech Stack

- **Frontend**: Pure HTML/CSS/JS (no framework needed)
- **Backend**: Python for scraping
- **Storage**: JSON file (easily upgradeable to SQLite/PostgreSQL)

## TODO

- [ ] Add more RSS sources (BBC, Sky Sports filtered)
- [ ] Create a simple Node.js server for auto-updates
- [ ] Add search functionality
- [ ] Add "Most Popular" tracking (requires DB)
- [ ] Add fixtures/results section

## License

MIT - Do whatever you want with it!