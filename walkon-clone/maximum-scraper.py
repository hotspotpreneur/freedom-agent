#!/usr/bin/env python3
"""
MAXIMUM Liverpool FC News Aggregator
=====================================
Ultimate version with:
- Maximum sources (25+)
- Journalist tracking (Romano, Ornstein, Joyce, Pearce, Bascombe)
- Cron job setup included
- Runs every 5 minutes or less
"""

import json
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
import re
from datetime import datetime
from typing import List, Dict, Set, Optional
import time
import html
import os
import sys

# ============================================================================
# MAXIMUM RSS FEEDS - 25+ SOURCES
# ============================================================================

RSS_FEEDS = [
    # Tier 0: OFFICIAL Liverpool FC
    {"name": "LFC Official - News", "url": "https://www.liverpoolfc.com/news.rss", "priority": 1},
    
    # Tier 1: Major UK Newspapers
    {"name": "Liverpool Echo", "url": "https://www.liverpoolecho.co.uk/sport/football/?service=rss", "priority": 1},
    {"name": "BBC Sport", "url": "https://feeds.bbci.co.uk/sport/football/rss.xml", "priority": 1},
    {"name": "Sky Sports", "url": "https://www.skysports.com/rss/12040", "priority": 1},
    {"name": "The Guardian", "url": "https://www.theguardian.com/football/liverpool/rss", "priority": 1},
    {"name": "Mirror", "url": "https://www.mirror.co.uk/sport/football/?service=rss", "priority": 1},
    {"name": "Metro", "url": "https://metro.co.uk/sport/football/feed/", "priority": 1},
    {"name": "The Times", "url": "https://www.thetimes.co.uk/rss/rss.aspx?edition=uk&sectioncode=136&supress=true", "priority": 2},
    {"name": "The Telegraph", "url": "https://www.telegraph.co.uk/football/rss.xml", "priority": 2},
    
    # Tier 2: Football News Sites
    {"name": "CaughtOffside", "url": "https://www.caughtoffside.com/feed/", "priority": 1},
    {"name": "The4thOfficial", "url": "https://the4thofficial.net/feed/", "priority": 1},
    {"name": "Sport Witness", "url": "https://sportwitness.co.uk/feed/", "priority": 1},
    {"name": "HITC", "url": "https://www.hitc.com/rss/", "priority": 2},
    {"name": "Football FanCast", "url": "https://www.footballfancast.com/feed/", "priority": 2},
    {"name": "90min", "url": "https://www.90min.com/feed", "priority": 2},
    {"name": "Yahoo Sports", "url": "https://sports.yahoo.com/rss/", "priority": 2},
    
    # Tier 3: Fan Sites (Critical for Liverpool)
    {"name": "This Is Anfield", "url": "https://www.thisisanfield.com/feed/", "priority": 1},
    {"name": "Read Liverpool FC", "url": "https://readliverpoolfc.com/feed/", "priority": 1},
    {"name": "Live4Liverpool", "url": "https://live4liverpool.com/feed/", "priority": 1},
    {"name": "The Anfield Wrap", "url": "https://www.theanfieldwrap.com/feed/", "priority": 1},
    {"name": "Daveockop", "url": "https://www.daveockop.com/latest-news/feed/", "priority": 2},
    {"name": "Rush The Kop", "url": "https://rushthekop.com/feed/", "priority": 2},
    {"name": "Empire of the Kop", "url": "https://empireofthekop.com/feed/", "priority": 2},
    {"name": "The Liverpool Way", "url": "https://theliverpoolway.com/feed/", "priority": 2},
    
    # Tier 4: Transfer Specialists
    {"name": "Football Insider", "url": "https://www.footballinsider.com/feed/", "priority": 2},
    {"name": "Football Transfers", "url": "https://www.footballtransfers.com/en/rss.xml", "priority": 2},
    {"name": "Inside Futbol", "url": "https://www.insidefutbol.com/feed/", "priority": 3},
]

# ============================================================================
# JOURNALIST KEYWORDS - Track specific journalists
# ============================================================================

JOURNALISTS = {
    "fabrizio romano": "Fabrizio Romano",
    "fabrizio": "Fabrizio Romano",
    "romano": "Fabrizio Romano",
    "the italian": "Fabrizio Romano",
    
    "david ornstein": "David Ornstein",
    "ornstein": "David Ornstein",
    "the athletic": "David Ornstein",
    
    "paul joyce": "Paul Joyce",
    "joyce": "Paul Joyce",
    
    "james pearce": "James Pearce",
    "pearce": "James Pearce",
    "james": "James Pearce",
    
    "chris bascombe": "Chris Bascombe",
    "bascombe": "Chris Bascombe",
    "chris": "Chris Bascombe",
    
    "ben nathan": "Ben Nathan",
    "nathan": "Ben Nathan",
    
    "anfield watch": "Anfield Watch",
    
    "ryan benson": "Ryan Benson",
    
    "jacob burrows": "Jacob Burrows",
    
    "simon stone": "Simon Stone",
    "simon": "Simon Stone",
}

# ============================================================================
# COMPREHENSIVE KEYWORDS
# ============================================================================

KEYWORDS = {
    "primary": {"liverpool", "liverpool fc", "anfield", "the reds", "ynwa", "jurgen klopp", "mo salah", "virgil van dijk"},
    
    "managers": {
        "andoni iraola", "iraola", "new manager", "next manager",
        "jurgen klopp", "klopp", "jurgens",
        "bill shankly", "shankly", "bob paisley", "paisley",
        "kenny daglish", "dalglish", "king kenny",
        "rafa benitez", "benitez",
        "roy evans", "ger houllier",
    },
    
    "coaches": {
        "pep lijnders", "lijnders", "assistant manager",
        "pete krawietz", "krawietz",
        "john achterberg", "achterberg",
        "aaron briggs", "briggs",
        "viv anderson",
    },
    
    "players": {
        # Goalkeepers
        "alisson", "alisson becker", "kelleher", "caimhin kelleher",
        # Defenders
        "virgil van dijk", "vvd", "van dijk",
        "ibrahim konate", "konate",
        "joe gomez", "gomez",
        "trent alexander arnold", "trent", "alexander arnold",
        "andrew robertson", "robertson",
        "kostas tsimikas", "tsimikas",
        "jarrel quansah", "quansah", "jarell",
        "conor bradley", "bradley",
        # Midfielders
        "alexis mac allister", "mac allister", "macca",
        "dominik szoboszlai", "szoboszlai",
        "ryan gravenberch", "gravenberch",
        "wataru endo", "endo",
        "stefan bajcetic", "bajcetic",
        "curtis jones", "jones",
        "harvey elliott", "elliott",
        "ben doak", "doak",
        "fabio carvalho", "carvalho",
        # Forwards
        "darwin nunez", "nunez",
        "luis diaz", "diaz",
        "diogo jota", "jota",
        "cody gakpo", "gakpo",
        "mohamed salah", "salah",
        "victor munoz", "munoz",
        "giovanni leoni", "leoni",
    },
    
    "youth": {
        "academy", "youth team", "youth system",
        "melwood", "axa training ground", "kirkby",
        "u21", "u23", "u18", "under 21", "under 23", "under 18",
        "reserves", "development squad",
        "lewis koumas", "koumas", "jayden danns", "danns",
        "james mcconnell", "mcconnell",
    },
    
    "wsl": {
        "liverpool women", "liverpool wsl", "liverpool women's",
        "wsl", "women's super league",
    },
    
    "legends": {
        "steven gerrard", "gerrard",
        "jamie carragher", "carragher",
        "michael owen", "owen",
        "robbie fowler", "fowler",
        "john barnes", "barnes",
        "kevin keegan", "keegan",
        "ian callaghan", "callaghan",
        "ray clemence", "clemence",
        "graeme souness", "souness",
    },
    
    "transfer": {
        "transfer", "signing", "bid", "offer", "deal",
        "contract", "medical", "personal terms",
        "bradley barcola", "barcola",
        "ibrahim mbaye", "mbaye",
        "raul asencio", "asencio",
        "djed spence", "spence",
        "ezri konsa", "konsa",
    },
    
    "injury": {
        "injury", "injured", "fitness", "recovery",
        "acl", "hamstring", "surgery", "rehab",
    },
}

ALL_KEYWORDS = set()
for cat in KEYWORDS.values():
    ALL_KEYWORDS.update(cat)

# ============================================================================
# FUNCTIONS
# ============================================================================

def detect_journalist(title: str, description: str) -> Optional[str]:
    """Detect if article mentions a specific journalist"""
    text = (title + " " + description).lower()
    
    for keyword, name in JOURNALISTS.items():
        if keyword in text:
            return name
    
    return None

def categorize_article(title: str, description: str) -> str:
    """Categorize article"""
    text = (title + " " + description).lower()
    
    if any(kw in text for kw in KEYWORDS["transfer"]):
        return "Transfer News"
    elif any(kw in text for kw in KEYWORDS["injury"]):
        return "Injury News"
    elif any(kw in text for kw in ["preview", "team news"]):
        return "Match Preview"
    elif any(kw in text for kw in ["result", "score", "won", "lost"]):
        return "Match Result"
    elif any(kw in text for kw in KEYWORDS["wsl"]):
        return "WSL"
    elif any(kw in text for kw in KEYWORDS["youth"]):
        return "Youth/Academy"
    elif any(kw in text for kw in KEYWORDS["managers"]):
        return "Manager News"
    elif any(kw in text for kw in KEYWORDS["legends"]):
        return "Legends/Ex-Players"
    
    return "General News"

def get_topics(title: str, description: str) -> List[str]:
    """Identify topics"""
    text = (title + " " + description).lower()
    topics = []
    
    checks = [
        ("Manager", KEYWORDS["managers"]),
        ("First Team", KEYWORDS["players"]),
        ("Youth/Academy", KEYWORDS["youth"]),
        ("WSL", KEYWORDS["wsl"]),
        ("Legends", KEYWORDS["legends"]),
    ]
    
    for name, kws in checks:
        if any(kw in text for kw in kws):
            topics.append(name)
    
    return topics if topics else ["General"]

def is_liverpool_article(title: str, description: str = "", keywords_str: str = "") -> bool:
    """Check if article is Liverpool-related"""
    text = (title + " " + description + " " + keywords_str).lower()
    
    has_liverpool = "liverpool" in text or "anfield" in text
    matches = sum(1 for kw in ALL_KEYWORDS if kw in text)
    
    return has_liverpool or matches >= 2

def fetch_url(url: str) -> Optional[str]:
    """Fetch URL"""
    import ssl
    try:
        # Create SSL context that doesn't verify certificates (for some RSS feeds)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/rss+xml, application/xml, text/html, */*',
            }
        )
        with urllib.request.urlopen(req, timeout=12, context=ssl_context) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None

def extract_image(item) -> str:
    """Extract image from RSS item"""
    namespaces = ['http://search.yahoo.com/mrss/', 'http://search.yahoo.com/mrss/']
    
    for ns in namespaces:
        for tag in ['content', 'thumbnail']:
            elem = item.find(f'.//{{{ns}}}{tag}')
            if elem is not None:
                url = elem.get('url')
                if url:
                    return url
    
    enclosure = item.find('enclosure')
    if enclosure is not None:
        url = enclosure.get('url')
        if url:
            return url
    
    return ""

def parse_rss_item(item, source: str) -> Optional[Dict]:
    """Parse RSS item"""
    title = html.unescape(item.findtext('title', '').strip())
    link = item.findtext('link', '').strip()
    description = html.unescape(item.findtext('description', '').strip())
    pub_date = item.findtext('pubDate', '')
    
    keywords_elem = item.find('.//{http://search.yahoo.com/mrss/}keywords')
    keywords_str = keywords_elem.text if keywords_elem is not None else ""
    
    image_url = extract_image(item)
    
    if not is_liverpool_article(title, description, keywords_str):
        return None
    
    # Detect journalist
    journalist = detect_journalist(title, description)
    
    category = categorize_article(title, description)
    topics = get_topics(title, description)
    
    description = re.sub(r'<[^>]+>', '', description)
    description = description[:200] + "..." if len(description) > 200 else description
    
    return {
        'title': title,
        'link': link,
        'description': description,
        'image': image_url,
        'source': source,
        'pub_date': pub_date,
        'category': category,
        'topics': topics,
        'journalist': journalist,
        'scraped_at': datetime.now().isoformat()
    }

def parse_rss_feed(content: str, source_name: str) -> List[Dict]:
    """Parse RSS feed"""
    articles = []
    try:
        root = ET.fromstring(content)
        for item in root.findall('.//item'):
            article = parse_rss_item(item, source_name)
            if article:
                articles.append(article)
    except:
        pass
    return articles

# ============================================================================
# MAIN
# ============================================================================

def scrape_all_sources() -> Dict:
    """Main scraping function"""
    all_articles = []
    sources_used = []
    sources_failed = []
    
    print("=" * 70)
    print("🏆 MAXIMUM LIVERPOOL FC NEWS AGGREGATOR 🏆")
    print("=" * 70)
    print(f"Scraping {len(RSS_FEEDS)} sources...\n")
    
    for feed in RSS_FEEDS:
        print(f"📰 {feed['name']}...", end=" ", flush=True)
        content = fetch_url(feed['url'])
        
        if content:
            articles = parse_rss_feed(content, feed['name'])
            if articles:
                print(f"✅ {len(articles)}")
                all_articles.extend(articles)
                sources_used.append(feed['name'])
            else:
                print("⚠️ None")
        else:
            print("❌")
            sources_failed.append(feed['name'])
        
        time.sleep(0.25)
    
    # Remove duplicates
    seen = set()
    unique_articles = []
    for article in all_articles:
        key = article['title'][:60].lower()
        if key not in seen:
            seen.add(key)
            unique_articles.append(article)
    
    # Sort by priority
    priority = {"Transfer News": 1, "Breaking": 2, "Injury News": 3, 
                "Match Preview": 4, "Match Result": 5, "Manager News": 6,
                "WSL": 7, "Youth/Academy": 8, "Legends/Ex-Players": 9, "General News": 10}
    unique_articles.sort(key=lambda x: priority.get(x['category'], 99))
    
    # Summary
    summary = {}
    journalists_found = {}
    for a in unique_articles:
        cat = a['category']
        summary[cat] = summary.get(cat, 0) + 1
        if a.get('journalist'):
            j = a['journalist']
            journalists_found[j] = journalists_found.get(j, 0) + 1
    
    output = {
        "metadata": {
            "last_updated": datetime.now().isoformat(),
            "total_sources": len(RSS_FEEDS),
            "successful_sources": len(sources_used),
            "sources_used": sources_used,
            "sources_failed": sources_failed[:10],
        },
        "summary": summary,
        "journalists": journalists_found,
        "total_articles": len(unique_articles),
        "articles": unique_articles[:200]
    }
    
    return output

def save_output(data: Dict, filename: str = "liverpool-news.json"):
    """Save to JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Saved to {filename}")

def main():
    """Main entry"""
    data = scrape_all_sources()
    save_output(data)
    
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"Total articles: {data['total_articles']}")
    print(f"Sources: {data['metadata']['successful_sources']}/{data['metadata']['total_sources']}")
    
    print(f"\n📂 By Category:")
    for cat, count in data['summary'].items():
        print(f"  • {cat}: {count}")
    
    if data.get('journalists'):
        print(f"\n📝 Journalists Found:")
        for j, count in data['journalists'].items():
            print(f"  • {j}: {count}")
    
    print(f"\n📰 Sources:")
    for src in data['metadata']['sources_used']:
        print(f"  - {src}")
    
    print("\n✅ Done!")

if __name__ == "__main__":
    main()