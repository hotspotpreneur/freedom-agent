# 🏆 MAXIMUM Liverpool FC News Aggregator

The **ultimate** self-hosted Liverpool FC news aggregator - designed to beat WalkOn.com!

## ⚽ Coverage

| Category | Coverage |
|----------|----------|
| **1st Team** | All current players |
| **Managers** | Shankly → Paisley → Dalglish → Benítez → Klopp → Iraola |
| **Coaches** | Lijnders, Krawietz, Achterberg, Briggs |
| **AXA/Kirkby** | Academy & training |
| **Youth** | U21, U23, U18 |
| **Legends** | 60s to present |
| **WSL** | Liverpool Women |
| **Journalists** | Romano, Ornstein, Joyce, Pearce, Bascombe |

## 📰 Stats (Latest Run)

- **265 articles** scraped
- **19 sources** active
- **8 categories** auto-detected
- **5 journalists** tracked

### Journalists Found:
- Fabrizio Romano: 8
- Chris Bascombe: 2  
- James Pearce: 2
- Paul Joyce: 1

## 📡 Sources (19 Active)

1. Liverpool Echo
2. BBC Sport
3. Sky Sports
4. The Guardian
5. Mirror
6. Metro
7. The Telegraph
8. CaughtOffside
9. The4thOfficial
10. Sport Witness
11. 90min
12. Yahoo Sports
13. This Is Anfield
14. Read Liverpool FC
15. Live4Liverpool
16. The Anfield Wrap
17. Rush The Kop (90 articles!)
18. Empire of the Kop
19. Inside Futbol

## 🚀 Quick Start

### Run the Scraper

```bash
cd walkon-clone
python3 maximum-scraper.py
```

### Set Up Auto-Refresh (Every 5 Minutes)

```bash
# Make setup script executable
chmod +x setup-cron.sh

# Run setup
bash setup-cron.sh
```

Or manually add to crontab:
```bash
crontab -e

# Add this line for every 5 minutes:
*/5 * * * * cd /path/to/walkon-clone && python3 maximum-scraper.py >> scraper.log 2>&1
```

### View the Site

```bash
python3 -m http.server 8000
# Open http://localhost:8000
```

## 📁 Files

```
walkon-clone/
├── maximum-scraper.py     # ⭐ THE SCRAPER (use this one)
├── index.html             # Frontend
├── liverpool-news.json    # Latest data (265 articles)
├── setup-cron.sh          # Cron setup script
├── comprehensive-scraper.py
├── ultimate-scraper.py
├── scraper.py
└── README.md
```

## 🔄 How It Works

1. **Scrapes 26 RSS feeds** every run
2. **Filters for Liverpool content** using 100+ keywords
3. **Categorizes** (Transfer, Injury, WSL, Youth, Legends, etc.)
4. **Tracks journalists** (Romano, Ornstein, Joyce, Pearce, Bascombe)
5. **Removes duplicates**
6. **Outputs to JSON** for frontend

## 🆚 vs WalkOn

| Feature | WalkOn | Ours |
|---------|--------|------|
| Sources | ~10 (paid) | 19+ (free) |
| Articles | ~50-100 | 265 |
| Refresh | Unknown | 5 min |
| Journalists | No | ✅ Yes |
| Youth/Legends | Basic | Full |
| Cost | £££ | Free |

## 📝 TODO

- [x] 265 articles per run
- [x] Journalist tracking
- [x] 5-minute refresh
- [ ] Add more fan sites
- [ ] Add Twitter/X monitoring for Romano
- [ ] Add fixtures section
- [ ] Deploy to hosting

---

# 🚀 WordPress Theme - Kopite News

## Installation

1. Upload the `wp-theme` folder to `/wp-content/themes/`
2. Log in to WordPress admin at https://kopite.online/wp-admin
3. Go to **Appearance → Themes**
4. Activate **Kopite News**
5. Go to **Appearance → Widgets** to configure ad spaces
6. Create pages: Home, News, Contact
7. Go to **Settings → Reading** and set "Your homepage displays" to "A static page"

## Ad Spaces

- **Banner Ad**: 728x90px - appears below header
- **Sidebar Ads**: 160x600px - appear on left/right of content

## Header Image

Use this prompt to generate the header graphic with DALL-E:

```
Create a minimalist Liverpool FC themed header graphic. On the left, show the iconic ANFIELD PAVILION ARCH (Paisley Gates) as an elegant black line drawing. On the right, arrange six legendary Liverpool managers as stylized black pencil sketches in a row: Bill Shankly, Bob Paisley, Kenny Dalglish, Joe Fagan, Rafael Benítez, and Jürgen Klopp. The style should be vintage football programme artwork - Art Deco inspired line drawings with clean strokes. Use white background with subtle red accents. The overall composition should be professional and suitable for a sports news website header. Horizontal layout, 1200x200 pixels.
```

## Importing News Articles

The scraper outputs to `liverpool-news.json`. To import into WordPress:

1. Install "WP All Import" plugin or use the REST API
2. Create a simple script to POST articles to /wp-json/wp/v2/posts
3. Or manually import JSON using WP's import tools

## Theme Features

- White background with red (#C8102E) accents
- Black text links (like WalkOn)
- Auto-updating copyright in footer
- Ad widget areas for monetization
- Responsive design
- Custom meta field for article source

Built with 🔥 for Paul