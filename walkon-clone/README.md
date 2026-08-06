# WalkOn Clone - Liverpool FC News Aggregator

A self-hosted alternative to Newsfinity-powered Liverpool FC news aggregation.

## ⚽ Comprehensive Coverage

This scraper captures news about:
- **1st Team** - Current players, manager, coaching staff
- **Managers** - Bill Shankly, Bob Paisley, Kenny Dalglish, Rafa Benítez, Jürgen Klopp, Andoni Iraola
- **Coaches** - Pep Lijnders, Pete Krawietz, John Achterberg, etc.
- **AXA Training Ground** - Academy and training news
- **Youth Teams** - U21, U23, U18, Academy
- **Legends & Ex-Players** - From the 60s to modern day
- **WSL** - Liverpool Women

## Features

- ✅ **Multi-source scraping** - Liverpool Echo, Sky Sports, BBC Sport
- ✅ **Auto-categorization** - Transfer, Injury, Match Preview, WSL, Youth, Legends
- ✅ **Topic detection** - Identifies if article is about managers, players, youth, etc.
- ✅ **No Monthly Fees** - Runs on your own server
- ✅ **JSON output** - Easy to integrate with any frontend

## Quick Start

### 1. Run the Scraper

```bash
python3 comprehensive-scraper.py
```

This creates `liverpool-news.json` with all the latest articles.

### 2. View the Frontend

Open `index.html` in a browser (use a local server to avoid CORS):

```bash
# Using Python
python3 -m http.server 8000

# Then open http://localhost:8000
```

## Sources

The scraper pulls from:
- **Liverpool Echo** - Primary local coverage
- **Sky Sports** - Transfer news & match coverage
- **BBC Sport** - General football news

## Keyword Categories

The scraper searches for:

| Category | Examples |
|----------|----------|
| Managers | Iraola, Klopp, Shankly, Paisley, Dalglish, Benítez |
| Players | Van Dijk, Salah, Trent, Robertson, Mac Allister, etc. |
| Youth | U21, U23, U18, Academy, Melwood, Kirkby |
| Legends | Gerrard, Carragher, Owen, Fowler, Barnes, etc. |
| Women's | WSL, Liverpool Women, Natalia Ramos |

## Automation

Set up a cron job to run the scraper every 15 minutes:

```bash
# Edit crontab
crontab -e

# Add this line
*/15 * * * * cd /path/to/walkon-clone && python3 comprehensive-scraper.py >> scraper.log 2>&1
```

## File Structure

```
walkon-clone/
├── index.html              # Main frontend
├── comprehensive-scraper.py # Full-featured scraper
├── liverpool-news.json     # Generated news data
├── scraper.py              # Simple scraper (legacy)
└── README.md               # This file
```

## TODO / Coming Soon

- [ ] Add more RSS sources (Metro, Mirror, Daily Star)
- [ ] Add Google News / Bing News API integration
- [ ] Search functionality
- [ ] Fixtures & Results section
- [ ] Player profiles database
- [ ] Historical news archive

## Tech Stack

- **Scraper**: Python 3 (no external dependencies)
- **Frontend**: Pure HTML/CSS/JS
- **Storage**: JSON file (easily upgradeable to SQLite)

## License

MIT - Do whatever you want with it!