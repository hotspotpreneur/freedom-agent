#!/usr/bin/env python3
"""
ULTIMATE Liverpool FC News Aggregator
======================================
The most comprehensive Liverpool FC news scraper - designed to beat WalkOn!

Sources: 20+ RSS feeds + web scraping
Coverage: 1st team, managers, coaches, youth, academy, legends, WSL
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

# ============================================================================
# COMPREHENSIVE RSS FEEDS LIST
# ============================================================================

RSS_FEEDS = [
    # Major UK Newspapers
    {"name": "Liverpool Echo", "url": "https://www.liverpoolecho.co.uk/sport/football/?service=rss", "priority": 1},
    {"name": "BBC Sport", "url": "https://feeds.bbci.co.uk/sport/football/rss.xml", "priority": 1},
    {"name": "Sky Sports", "url": "https://www.skysports.com/rss/12040", "priority": 1},
    {"name": "The Guardian", "url": "https://www.theguardian.com/football/liverpool/rss", "priority": 1},
    {"name": "Mirror", "url": "https://www.mirror.co.uk/sport/football/?service=rss", "priority": 2},
    {"name": "Metro", "url": "https://metro.co.uk/sport/football/feed/", "priority": 2},
    
    # Football News Sites
    {"name": "CaughtOffside", "url": "https://www.caughtoffside.com/feed/", "priority": 2},
    {"name": "The4thOfficial", "url": "https://the4thofficial.net/feed/", "priority": 2},
    {"name": "Sport Witness", "url": "https://sportwitness.co.uk/feed/", "priority": 2},
    
    # Fan Sites
    {"name": "This Is Anfield", "url": "https://www.thisisanfield.com/feed/", "priority": 1},
    {"name": "Read Liverpool FC", "url": "https://readliverpoolfc.com/feed/", "priority": 1},
    {"name": "Live4Liverpool", "url": "https://live4liverpool.com/feed/", "priority": 1},
    {"name": "The Anfield Wrap", "url": "https://www.theanfieldwrap.com/feed/", "priority": 2},
    {"name": "Football Insider", "url": "https://www.footballinsider.com/feed/", "priority": 2},
    {"name": "Football FanCast", "url": "https://www.footballfancast.com/feed/", "priority": 3},
    
    # International
    {"name": "90min", "url": "https://www.90min.com/feed", "priority": 2},
    {"name": "Football Transfers", "url": "https://www.footballtransfers.com/en/rss.xml", "priority": 2},
]

# ============================================================================
# COMPREHENSIVE KEYWORD DICTIONARY
# ============================================================================

# All keywords organized by category
KEYWORDS = {
    # Primary
    "primary": {"liverpool", "liverpool fc", "anfield", "the reds", "ynwa"},
    
    # Managers (all-time)
    "managers": {
        # Current
        "andoni iraola", "iraola",
        # Recent
        "jurgen klopp", "klopp", "jurgens",
        # Legends
        "bill shankly", "shankly", "shanklys",
        "bob paisley", "paisley",
        "kenny daglish", "dalglish", "king kenny",
        "rafa benitez", "benitez", "rafa",
        # Others
        "roy evans", "ger houllier", "houllier", "david hodgeson",
    },
    
    # Coaches
    "coaches": {
        "pep lijnders", "lijnders", "assistant manager",
        "pete krawietz", "krawietz",
        "john achterberg", "achterberg",
        "aaron briggs", "briggs",
        "viv anderson", "anderson",
        "coach", "coaching staff", "backroom"
    },
    
    # Current First Team
    "players": {
        # Goalkeepers
        "alisson", "alisson becker", "kelleher", "caimhin kelleher", "marcai",
        # Defenders
        "virgil van dijk", "vvd", "van dijk", "virgil",
        "ibrahim konate", "konate", "ibrahim",
        "joe gomez", "gomez",
        "trent alexander arnold", "trent", "alexander arnold", "taa",
        "andrew robertson", "robertson", "robbo",
        "kostas tsimikas", "tsimikas",
        "jarrel quansah", "quansah", "jarell",
        "conor bradley", "bradley",
        # Midfielders
        "alexis mac allister", "mac allister", "macca", "allister",
        "dominik szoboszlai", "szoboszlai", "dominik",
        "ryan gravenberch", "gravenberch",
        "wataru endo", "endo",
        "stefan bajcetic", "bajcetic",
        "curtis jones", "jones",
        "harvey elliott", "elliott",
        "ben doak", "doak",
        "fabio carvalho", "carvalho",
        "tony gallagher", "gallagher",
        # Forwards
        "darwin nunez", "nunez", "darwin",
        "luis diaz", "diaz", "luchito",
        "diogo jota", "jota",
        "cody gakpo", "gakpo",
        "mohamed salah", "salah", "the egyptian king", "mo salah",
        "victor munoz", "munoz", "victor",
        "giovanni leoni", "leoni",
    },
    
    # Youth & Academy
    "youth": {
        "academy", "youth team", "youth system", "youth academy",
        "melwood", "axa training ground", "kirkby", "axa",
        "u21", "u23", "u18", "under 21", "under 23", "under 18",
        "reserves", "development squad", "academy squad",
        "young reds", "youngsters", "youth player",
        "lewis koumas", "koumas", "jayden danns", "danns",
        "james mcconnell", "mcconnell", "bobby clark", "clark",
        "calvin ramsay", "ramsay", "mateusz musialowski", "musialowski",
    },
    
    # Women's Football
    "wsl": {
        "liverpool women", "liverpool wsl", "liverpool women's",
        "wsl", "women's super league", "fa wsl",
        "natalia ramos", "megan curnow", "cassie white",
        "niamh fahey", "katherine flanagan",
    },
    
    # Legends & Ex-Players (decade by decade)
    "legends": {
        # 60s-70s
        "ian callaghan", "callaghan", "ray clemence", "clemence",
        "kevin keegan", "keegan", "graeme souness", "souness",
        "phil neal", "neal", "alan kennedy", "kennedy",
        "bruce grobbelaar", "grobbelaar", "alan hansen", "hansen",
        # 80s-90s
        "john barnes", "barnes", "peter beardsley", "beardsley",
        "john alder", "alder", "steve staunton", "staunton",
        "ronnie whelan", "whelan", "ray houghton", "houghton",
        "john toshack", "toshack",
        # 2000s
        "steven gerrard", "gerrard", "captain fantastic",
        "jamie carragher", "carragher", "carra",
        "michael owen", "owen",
        "robbie fowler", "fowler", "god",
        "sami hyppia", "hyppia", "djimi traore", "traore",
        "xabi alonso", "alonso",
        "peter crouch", "crouch", "luis garcia", "garcia",
        "emile heskey", "heskey",
        # 2010s
        "fernando torres", "torres", "raheem sterling", "sterling",
        "louis suarez", "suarez", "sturridge", "daniel sturridge",
        "philippe coutinho", "coutinho", "cout",
        "sadio mane", "mane", "roberto firmino", "firmino",
        "jordan henderson", "henderson", "hendo",
        "james milner", "milner", "the vice captain",
        # Recent ex
        "fabinho", "thiago alcantara", "thiago", "nee keita",
    },
    
    # Transfer Keywords
    "transfer": {
        "transfer", "signing", "bid", "offer", "deal",
        "contract", "extension", "renewal", "released",
        "free transfer", "loan move", "permanent deal",
        "fee", "medical", "personal terms", "agreed terms",
        "brokering", "push for", "target", "chasing",
        "bradley barcola", "barcola", "ibrahim mbaye", "mbaye",
        "raul asencio", "asencio", "djed spence", "spence",
        "ezri konsa", "konsa", "alex scott",
    },
    
    # Injury Keywords
    "injury": {
        "injury", "injured", "fitness", "recovery",
        "acl", "knee injury", "hamstring", "ankle injury",
        "groin", "calf strain", "thigh", "back problem",
        "surgery", "rehab", "treatment", "rehabilitation",
        "doubt", "out for", "return date", "comeback",
    },
    
    # Match Keywords
    "match": {
        "premier league", "champions league", "fa cup",
        "league cup", "europa league", "community shield",
        "carabao cup", "matchday", "fixture", "result",
        "score", "won", "lost", "draw", "victory", "defeat",
        "goal", "assist", "hat-trick", "brace", "double",
        "clean sheet", "penalty", "red card", "yellow card",
    },
}

# Flatten all keywords for searching
ALL_KEYWORDS = set()
for category in KEYWORDS.values():
    ALL_KEYWORDS.update(category)

# ============================================================================
# CATEGORIZATION FUNCTIONS
# ============================================================================

def categorize_article(title: str, description: str) -> str:
    """Categorize article based on title and description"""
    text = (title + " " + description).lower()
    
    priority_order = [
        ("transfer", KEYWORDS["transfer"]),
        ("injury", KEYWORDS["injury"]),
        ("match preview", ["preview", "team news", "predictions", "opposition"]),
        ("match result", ["result", "score", "won", "lost", "draw", "victory", "defeat"]),
        ("wsl", KEYWORDS["wsl"]),
        ("youth", KEYWORDS["youth"]),
        ("manager", KEYWORDS["managers"]),
        ("legends", KEYWORDS["legends"]),
    ]
    
    for category_name, keywords in priority_order:
        if any(kw in text for kw in keywords):
            cat_names = {
                "transfer": "Transfer News",
                "injury": "Injury News", 
                "match preview": "Match Preview",
                "match result": "Match Result",
                "wsl": "WSL",
                "youth": "Youth/Academy",
                "manager": "Manager News",
                "legends": "Legends/Ex-Players"
            }
            return cat_names[category_name]
    
    return "General News"

def get_topics(title: str, description: str) -> List[str]:
    """Identify all topics in the article"""
    text = (title + " " + description).lower()
    topics = []
    
    topic_map = [
        ("Manager", KEYWORDS["managers"]),
        ("Coaching Staff", KEYWORDS["coaches"]),
        ("First Team", KEYWORDS["players"]),
        ("Youth/Academy", KEYWORDS["youth"]),
        ("WSL", KEYWORDS["wsl"]),
        ("Legends/Ex-Players", KEYWORDS["legends"]),
    ]
    
    for topic_name, keywords in topic_map:
        if any(kw in text for kw in keywords):
            topics.append(topic_name)
    
    if not topics:
        topics.append("General")
    
    return topics

def is_liverpool_article(title: str, description: str = "", keywords_str: str = "") -> bool:
    """Check if article is Liverpool-related"""
    text = (title + " " + description + " " + keywords_str).lower()
    
    # Must have "liverpool" or multiple keyword matches
    has_liverpool = "liverpool" in text or "anfield" in text
    
    # Count keyword matches
    matches = sum(1 for kw in ALL_KEYWORDS if kw in text)
    
    return has_liverpool or matches >= 2

# ============================================================================
# SCRAPING FUNCTIONS
# ============================================================================

def fetch_url(url: str, referer: str = "") -> Optional[str]:
    """Fetch URL with error handling"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/rss+xml, application/xml, text/html, */*',
                'Accept-Language': 'en-GB,en;q=0.9',
            }
        )
        if referer:
            req.add_header('Referer', referer)
            
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"  ⚠️ Error: {e}")
        return None

def extract_image_from_item(item) -> str:
    """Extract image URL from RSS item"""
    # Try various RSS namespaces
    namespaces = [
        ('media', 'http://search.yahoo.com/mrss/'),
        ('media', 'http://search.yahoo.com/mrss/'),
    ]
    
    for prefix, uri in namespaces:
        # media:content
        elem = item.find(f'.//{{{uri}}}content')
        if elem is not None:
            url = elem.get('url')
            if url:
                return url
        
        # media:thumbnail
        elem = item.find(f'.//{{{uri}}}thumbnail')
        if elem is not None:
            url = elem.get('url')
            if url:
                return url
    
    # Try enclosure
    enclosure = item.find('enclosure')
    if enclosure is not None:
        url = enclosure.get('url')
        if url:
            enc_type = enclosure.get('type', '')
            if 'image' in enc_type.lower() or 'jpg' in enc_type.lower() or 'png' in enc_type.lower():
                return url
    
    return ""

def parse_rss_item(item, source: str) -> Optional[Dict]:
    """Parse a single RSS item"""
    # Extract basic info
    title = html.unescape(item.findtext('title', '').strip())
    link = item.findtext('link', '').strip()
    description = html.unescape(item.findtext('description', '').strip())
    pub_date = item.findtext('pubDate', '')
    
    # Get keywords if available
    keywords_elem = item.find('.//{http://search.yahoo.com/mrss/}keywords')
    keywords_str = keywords_elem.text if keywords_elem is not None else ""
    
    # Get image
    image_url = extract_image_from_item(item)
    
    # Filter for Liverpool content
    if not is_liverpool_article(title, description, keywords_str):
        return None
    
    # Categorize
    category = categorize_article(title, description)
    topics = get_topics(title, description)
    
    # Clean description
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
        'scraped_at': datetime.now().isoformat()
    }

def parse_rss_feed(content: str, source_name: str) -> List[Dict]:
    """Parse RSS feed and return Liverpool articles"""
    articles = []
    
    try:
        root = ET.fromstring(content)
        for item in root.findall('.//item'):
            article = parse_rss_item(item, source_name)
            if article:
                articles.append(article)
    except ET.ParseError as e:
        print(f"  ⚠️ XML parse error: {e}")
    except Exception as e:
        print(f"  ⚠️ Error: {e}")
    
    return articles

# ============================================================================
# MAIN SCRAPER
# ============================================================================

def scrape_all_sources() -> Dict:
    """Main function to scrape all sources"""
    all_articles = []
    sources_used = []
    sources_failed = []
    
    print("=" * 70)
    print("🏆 ULTIMATE LIVERPOOL FC NEWS AGGREGATOR 🏆")
    print("=" * 70)
    print(f"Scraping {len(RSS_FEEDS)} sources...\n")
    
    for feed in RSS_FEEDS:
        print(f"📰 {feed['name']}...", end=" ")
        content = fetch_url(feed['url'])
        
        if content:
            articles = parse_rss_feed(content, feed['name'])
            if articles:
                print(f"✅ {len(articles)} articles")
                all_articles.extend(articles)
                sources_used.append(feed['name'])
            else:
                print("⚠️ No Liverpool articles")
        else:
            print("❌ Failed to fetch")
            sources_failed.append(feed['name'])
        
        time.sleep(0.3)  # Rate limiting
    
    # Remove duplicates
    seen = set()
    unique_articles = []
    for article in all_articles:
        key = article['title'][:60].lower()
        if key not in seen:
            seen.add(key)
            unique_articles.append(article)
    
    # Sort by category priority
    category_priority = {
        "Transfer News": 1,
        "Breaking": 2,
        "Injury News": 3,
        "Match Preview": 4,
        "Match Result": 5,
        "Manager News": 6,
        "WSL": 7,
        "Youth/Academy": 8,
        "Legends/Ex-Players": 9,
        "General News": 10
    }
    
    unique_articles.sort(key=lambda x: category_priority.get(x['category'], 99))
    
    # Build summary
    summary = {}
    for article in unique_articles:
        cat = article['category']
        summary[cat] = summary.get(cat, 0) + 1
    
    # Build output
    output = {
        "metadata": {
            "last_updated": datetime.now().isoformat(),
            "total_sources": len(RSS_FEEDS),
            "successful_sources": len(sources_used),
            "sources_used": sources_used,
            "sources_failed": sources_failed[:10],  # Limit failed list
        },
        "summary": summary,
        "total_articles": len(unique_articles),
        "articles": unique_articles[:150]  # Keep latest 150
    }
    
    return output

def save_output(data: Dict, filename: str = "liverpool-news.json"):
    """Save to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Saved to {filename}")

def main():
    """Main entry point"""
    data = scrape_all_sources()
    save_output(data)
    
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"Total articles: {data['total_articles']}")
    print(f"Sources scraped: {data['metadata']['successful_sources']}/{data['metadata']['total_sources']}")
    print(f"\n📂 By Category:")
    for cat, count in data['summary'].items():
        print(f"  • {cat}: {count}")
    
    print(f"\n📰 Sources Used:")
    for src in data['metadata']['sources_used'][:10]:
        print(f"  - {src}")
    
    print("\n✅ Done! Your ultimate Liverpool news aggregator is ready!")

if __name__ == "__main__":
    main()