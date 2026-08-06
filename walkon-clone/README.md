# 🏆 Ultimate Liverpool FC News Aggregator

A **self-hosted, fully-featured** Liverpool FC news aggregator - designed to beat WalkOn.com!

## ⚽ Comprehensive Coverage

| Category | Coverage |
|----------|----------|
| **1st Team** | All current players, coaching staff |
| **Managers** | Shankly, Paisley, Dalglish, Benítez, Klopp, Iraola |
| **Coaches** | Lijnders, Krawietz, Achterberg, Briggs |
| **AXA/Kirkby** | Academy & training ground news |
| **Youth Teams** | U21, U23, U18, reserves |
| **Legends** | From 60s (Callaghan, Clemence) to modern (Gerrard, Owen, Salah) |
| **WSL** | Liverpool Women |

## 📰 Sources (14 Active)

The scraper pulls from these sources:

- **Liverpool Echo** - Primary local coverage
- **BBC Sport** - Official BBC football news
- **Sky Sports** - Transfer & match coverage  
- **The Guardian** - Quality journalism
- **Mirror** - Tabloid football coverage
- **Metro** - Quick-fire football news
- **CaughtOffside** - Transfer rumors & news
- **The4thOfficial** - Transfer news
- **Sport Witness** - Transfer updates
- **This Is Anfield** - Top fan site
- **Read Liverpool FC** - Independent coverage
- **Live4Liverpool** - Fan site
- **The Anfield Wrap** - Podcast & content
- **90min** - Football features

## 📊 Current Stats

- **176 articles** scraped per run
- **14 sources** active
- **8 categories** auto-detected

### Categories:
- Transfer News (112)
- General News (29)
- Match Result (10)
- Injury News (9)
- Legends/Ex-Players (8)
- Manager News (5)
- Youth/Academy (2)
- WSL (1)

## 🚀 Quick Start

### 1. Run the Scraper

```bash
cd walkon-clone
python3 ultimate-scraper.py
```

This creates `liverpool-news.json` with all the latest articles.

### 2. View the Frontend

Open `index.html` in a browser (use a local server to avoid CORS):

```bash
# Using Python
python3 -m http.server 8000

# Then open http://localhost:8000
```

## ⚙️ Automation

Set up a cron job to run every 15 minutes:

```bash
# Edit crontab
crontab -e

# Add this line
*/15 * * * * cd /path/to/walkon-clone && python3 ultimate-scraper.py >> scraper.log 2>&1
```

Or set up a systemd timer for more reliability.

## 📁 File Structure

```
walkon-clone/
├── index.html              # Beautiful responsive frontend
├── ultimate-scraper.py     # The ultimate scraper (THIS IS THE ONE)
├── comprehensive-scraper.py # Legacy scraper
├── liverpool-news.json     # Generated news data (176 articles!)
├── scraper.py              # Simple scraper (legacy)
└── README.md               # This file
```

## 🔧 Adding More Sources

Edit `ultimate-scraper.py` and add to `RSS_FEEDS`:

```python
{"name": "Site Name", "url": "https://example.com/rss.xml", "priority": 2},
```

Priority: 1 = Essential, 2 = Important, 3 = Nice to have

## 🎯 Features

- ✅ Multi-source RSS aggregation (14 sources)
- ✅ Auto-categorization (Transfer, Injury, WSL, Youth, Legends, etc.)
- ✅ Topic detection (Managers, Players, Youth, etc.)
- ✅ Duplicate removal
- ✅ Category-based sorting
- ✅ JSON output for easy integration
- ✅ No dependencies (pure Python standard library)
- ✅ Rate limiting to be nice to servers
- ✅ Error handling for failed sources

## 🆚 vs WalkOn.com

| Feature | WalkOn | Our Aggregator |
|---------|--------|----------------|
| Sources | Newsfinity (paid) | 14+ free RSS feeds |
| Categories | Limited | 8 categories |
| Youth/Academy | Basic | Full coverage |
| Legends | Basic | Full historical |
| WSL | Yes | Yes |
| Cost | Monthly fee | Free! |
| Customizable | No | Full control |

## 📝 TODO

- [ ] Add web scraping for sites without RSS
- [ ] Add Google Alerts / News API
- [ ] Create simple admin panel
- [ ] Add search functionality
- [ ] Add fixtures & results
- [ ] Player database
- [ ] Historical archive
- [ ] Auto-deploy to hosting

## 📜 License

MIT - Do whatever you want with it!

---

Built with 🔥 by Your Freedom Agent