#!/usr/bin/env python3
"""
Comprehensive Liverpool FC News Scraper
=========================================
Covers: 1st team, manager, coaches, AXA, youth teams (U21, U23, U18), 
academy, legends, ex-players (60s to modern day)

Managers: Shankly, Paisley, Dalglish, Benítez, Klopp, Iraola
"""

import json
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from typing import List, Dict, Set
import time
import re

# ============================================================================
# RSS FEEDS - Multiple sources for comprehensive coverage
# ============================================================================

RSS_FEEDS = [
    # Primary sources
    {
        "name": "Liverpool Echo",
        "url": "https://www.liverpoolecho.co.uk/sport/football/?service=rss",
        "priority": 1
    },
    {
        "name": "Sky Sports",
        "url": "https://www.skysports.com/rss/12040",
        "priority": 2
    },
    {
        "name": "BBC Sport",
        "url": "https://feeds.bbci.co.uk/sport/football/rss.xml",
        "priority": 1
    },
]

# ============================================================================
# COMPREHENSIVE KEYWORD LIST - All terms to search for
# ============================================================================

# Primary keywords (always include)
PRIMARY_KEYWORDS = {
    "liverpool", "liverpool fc", "liverpool football club", 
    "anfield", "the reds"
}

# Manager keywords
MANAGER_KEYWORDS = {
    # Current
    "andoni iraola", "iraola",
    # Recent past
    "jurgen klopp", "klopp", 
    # Legends & historical
    "bill shankly", "shankly", 
    "bob paisley", "paisley",
    "kenny daglish", "dalglish", "king kenny",
    "rafa benitez", "benitez", "rafa",
    "roy evans", "roy evans",
    "ger houllier", "houllier",
    "graham burns", "burns",
    "pete fitzwater", "fitzwater",
    "tom bush", "bush",
}

# Coach keywords
COACH_KEYWORDS = {
    "pep lijnders", "lijnders", "assistant manager",
    "pete krawietz", "krawietz", 
    "john achterberg", "achterberg", "goalkeeping coach",
    "viv anderson", "anderson",
    "aaron briggs", "briggs", "set piece coach",
    "coach", "coaching staff", "backroom team"
}

# First team players (current)
FIRST_TEAM_CURRENT = {
    # Goalkeepers
    "alisson", "alisson becker", "kelleher", "caimhin kelleher",
    "mario rana", "marcai", "simon",
    # Defenders
    "virgil van dijk", "vvd", "van dijk",
    "ibrahim konate", "konate",
    "joe gomez", "gomez",
    "trent alexander arnold", "trent", "alexander arnold",
    "andrew robertson", "robertson", "robbo",
    "kostas tsimikas", "tsimikas",
    "jarrel quansah", "quansah",
    "conor bradley", "bradley",
    "jarell quansah", "quansah",
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
}

# Youth team keywords
YOUTH_KEYWORDS = {
    # Academy/Youth terms
    "academy", "youth team", "youth system", "youth academy",
    "melwood", "axa training ground", "kirkby academy",
    # Specific youth teams
    "under 21", "u21", "liverpool u21", "liverpool under 21",
    "under 23", "u23", "liverpool u23", "liverpool under 23",
    "under 18", "u18", "liverpool u18", "liverpool under 18",
    "reserves", "development squad", "academy squad",
    "young reds", "youngsters",
    # Youth players
    "lewis koumas", "koumas",
    "jayden danns", "danns",
    "james mcconnell", "mcconnell",
    "bobby clark", "clark",
    "tremy alvaro", "alvaro",
    "calvin ramsay", "ramsay",
    "fabio centrone", "centrone",
    "mateusz musialowski", "musialowski",
    "stefan orcic", "orcic",
}

# Women's/WSL keywords
WOMENS_KEYWORDS = {
    "liverpool women", "liverpool wsl", "liverpool women's",
    "wsl", "women's super league", "fa wsl",
    "natalia ramos", "natalia",
    "megan curnow", "curnow",
    "cassie white", "white",
    "niamh fahey", "fahey",
    "katherine flanagan", "flanagan",
    "natasha harde", "harde",
}

# Legend & ex-player keywords (60s to modern)
LEGEND_KEYWORDS = {
    # 60s-70s legends
    "ian callaghan", "callaghan",
    "ray clemence", "clemence",
    "kevin keegan", "keegan",
    "graeme souness", "souness",
    "phil neal", "neal",
    "alan kennedy", "kennedy",
    "bruce grobbelaar", "grobbelaar",
    "alan hansen", "hansen",
    "mike marsh", "marsh",
    # 80s-90s
    "john barnes", "barnes",
    "peter beardsley", "beardsley",
    "john alder", "alder",
    "steve staunton", "staunton",
    "ronnie whelan", "whelan",
    "ray houghton", "houghton",
    "john toshack", "toshack",
    # 2000s
    "steven gerrard", "gerrard",
    "jamie carragher", "carragher",
    "michael owen", "owen",
    "robbie fowler", "fowler",
    "sami hyppia", "hyppia",
    "djimi traore", "traore",
    "xabi alonso", "alonso",
    "peter crouch", "crouch",
    "luis garcia", "garcia",
    "steven gerrard", "gerrard",
    "emile heskey", "heskey",
    # 2010s
    "fernando torres", "torres",
    "sergio aguero", "aguero",  # Not liverpool but relevant for rivalry
    "raheem sterling", "sterling",
    "louis suarez", "suarez",
    "sturridge", "daniel sturridge",
    "philippe coutinho", "coutinho",
    "mohamed salah", "salah",
    "sadio mane", "mane",
    "roberto firmino", "firmino",
    "jordan henderson", "henderson",
    "james milner", "milner",
    "virgil van dijk", "van dijk",
    "alvaro morata", "morata",  # Not liverpool but rumored
    # Recent ex-players
    "jordan henderson", "henderson",
    "fabinho", "fabinho de lima",
    "thiago alcantara", "thiago",
    "nee be careful", "careful",
    "gareth bale", "bale",  # Not liverpool but rumored
    "naby keita", "keita",
    "dimitri payet", "payet",
}

# Transfer keywords
TRANSFER_KEYWORDS = {
    "transfer", "signing", "bid", "offer", "deal",
    "contract", "extension", "renewal", "released",
    "free transfer", "loan", "permanent", "fee",
    "medical", "personal terms", "agreed",
    # Targets/Rumors
    "bradley barcola", "barcola",
    "ibrahim mbaye", "mbaye",
    "raul asencio", "asencio",
    "djed spence", "spence",
    "ezri konsa", "konsa",
    "alex scott", "scott",
    "marc rocca", "rocca",
}

# Injury keywords
INJURY_KEYWORDS = {
    "injury", "injured", "fitness", "recovery",
    "acl", "knee", "hamstring", "ankle",
    "groin", "calf", "thigh", "back",
    "surgery", "rehab", "treatment",
    "doubt", "out", "return", "comeback",
    "giovanni leoni", "leoni injury",
}

# Match keywords
MATCH_KEYWORDS = {
    "match", "game", "fixture", "result", "score",
    "premier league", "champions league", "fa cup",
    "league cup", "europa league", "community shield",
    "win", "lose", "draw", "victory", "defeat",
    "goal", "assist", "hat-trick", "brace",
    "clean sheet", "penalty", "red card", "yellow card",
    "VAR", "offside", "foul",
}

# Combine all keywords
ALL_KEYWORDS = (
    PRIMARY_KEYWORDS | MANAGER_KEYWORDS | COACH_KEYWORDS | 
    FIRST_TEAM_CURRENT | YOUTH_KEYWORDS | WOMENS_KEYWORDS |
    LEGEND_KEYWORDS | TRANSFER_KEYWORDS | INJURY_KEYWORDS | MATCH_KEYWORDS
)

# ============================================================================
# CATEGORY MAPPING
# ============================================================================

def categorize_article(title: str, description: str) -> str:
    """Categorize article based on content"""
    text = (title + " " + description).lower()
    
    if any(kw in text for kw in TRANSFER_KEYWORDS):
        return "Transfer News"
    elif any(kw in text for kw in INJURY_KEYWORDS):
        return "Injury News"
    elif any(kw in text for kw in ["preview", "coming up", "team news", "predictions"]):
        return "Match Preview"
    elif any(kw in text for kw in ["result", "score", "won", "lost", "draw", "victory"]):
        return "Match Result"
    elif any(kw in text for kw in WOMENS_KEYWORDS):
        return "WSL"
    elif any(kw in text for kw in YOUTH_KEYWORDS):
        return "Youth/Academy"
    elif any(kw in text for kw in MANAGER_KEYWORDS):
        return "Manager News"
    elif any(kw in text for kw in LEGEND_KEYWORDS):
        return "Legends/Ex-Players"
    else:
        return "General News"

def get_article_topic(title: str, description: str) -> List[str]:
    """Identify all topics covered in article"""
    text = (title + " " + description).lower()
    topics = []
    
    if any(kw in text for kw in MANAGER_KEYWORDS):
        topics.append("Manager")
    if any(kw in text for kw in COACH_KEYWORDS):
        topics.append("Coaching Staff")
    if any(kw in text for kw in FIRST_TEAM_CURRENT):
        topics.append("First Team")
    if any(kw in text for kw in YOUTH_KEYWORDS):
        topics.append("Youth/Academy")
    if any(kw in text for kw in WOMENS_KEYWORDS):
        topics.append("Women/WSL")
    if any(kw in text for kw in LEGEND_KEYWORDS):
        topics.append("Legends/Ex-Players")
    if any(kw in text for kw in TRANSFER_KEYWORDS):
        topics.append("Transfers")
    if any(kw in text for kw in INJURY_KEYWORDS):
        topics.append("Injury News")
        
    if not topics:
        topics.append("General")
    
    return topics

# ============================================================================
# SCRAPING FUNCTIONS
# ============================================================================

def fetch_url(url: str) -> str:
    """Fetch URL content with error handling"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def is_liverpool_article(title: str, description: str = "", keywords: str = "") -> bool:
    """Check if article is Liverpool-related"""
    text = (title + " " + description + " " + keywords).lower()
    
    # Must contain "liverpool" OR multiple relevant keywords
    has_primary = "liverpool" in text or "anfield" in text
    
    # Count matching keywords
    matches = sum(1 for kw in ALL_KEYWORDS if kw in text)
    
    return has_primary or matches >= 2

def parse_rss_item(item, source_name: str) -> Dict:
    """Parse a single RSS item"""
    title = item.findtext('title', '').strip()
    link = item.findtext('link', '').strip()
    description = item.findtext('description', '').strip()
    pub_date = item.findtext('pubDate', '')
    
    # Get image from various RSS formats
    image_url = ""
    
    # Media namespace
    media_content = item.find('.//{http://search.yahoo.com/mrss/}content')
    media_thumbnail = item.find('.//{http://search.yahoo.com/mrss/}thumbnail')
    media_keywords = item.findtext('.//{http://search.yahoo.com/mrss/}keywords', '')
    
    if media_content is not None:
        image_url = media_content.get('url', '')
    elif media_thumbnail is not None:
        image_url = media_thumbnail.get('url', '')
    
    # Check enclosure
    enclosure = item.find('enclosure')
    if enclosure is not None and not image_url:
        image_url = enclosure.get('url', '')
    
    # Skip if not Liverpool-related
    if not is_liverpool_article(title, description, media_keywords):
        return None
    
    category = categorize_article(title, description)
    topics = get_article_topic(title, description)
    
    return {
        'title': title,
        'link': link,
        'description': description[:200] + "..." if len(description) > 200 else description,
        'image': image_url,
        'source': source_name,
        'pub_date': pub_date,
        'category': category,
        'topics': topics,
        'keywords_found': media_keywords
    }

def parse_sky_sports(content: str, source_name: str) -> List[Dict]:
    """Parse Sky Sports RSS feed"""
    articles = []
    try:
        root = ET.fromstring(content)
        for item in root.findall('.//item'):
            result = parse_rss_item(item, source_name)
            if result:
                articles.append(result)
    except Exception as e:
        print(f"Error parsing Sky Sports: {e}")
    return articles

def parse_bbc_rss(content: str, source_name: str) -> List[Dict]:
    """Parse BBC RSS feed"""
    articles = []
    try:
        root = ET.fromstring(content)
        for item in root.findall('.//item'):
            title = item.findtext('title', '').strip()
            if 'liverpool' in title.lower():
                result = parse_rss_item(item, source_name)
                if result:
                    articles.append(result)
    except Exception as e:
        print(f"Error parsing BBC: {e}")
    return articles

def parse_generic_rss(content: str, source_name: str) -> List[Dict]:
    """Parse generic RSS feed"""
    articles = []
    try:
        root = ET.fromstring(content)
        for item in root.findall('.//item'):
            result = parse_rss_item(item, source_name)
            if result:
                articles.append(result)
    except Exception as e:
        print(f"Error parsing {source_name}: {e}")
    return articles

# ============================================================================
# MAIN SCRAPER
# ============================================================================

def scrape_all_sources() -> Dict:
    """Main function to scrape all sources"""
    all_articles = []
    sources_scraped = []
    
    print("=" * 60)
    print("LIVERPOOL FC NEWS SCRAPER")
    print("Comprehensive coverage: 1st team, Youth, Legends, WSL")
    print("=" * 60)
    
    for feed in RSS_FEEDS:
        print(f"\n📰 Scraping {feed['name']}...")
        content = fetch_url(feed['url'])
        
        if not content:
            print(f"  ⚠️ Failed to fetch")
            continue
        
        articles = []
        if feed['name'] == 'Sky Sports':
            articles = parse_sky_sports(content, feed['name'])
        elif feed['name'] == 'BBC Sport':
            articles = parse_bbc_rss(content, feed['name'])
        else:
            articles = parse_generic_rss(content, feed['name'])
        
        print(f"  ✅ Found {len(articles)} Liverpool articles")
        all_articles.extend(articles)
        sources_scraped.append(feed['name'])
        
        # Rate limiting
        time.sleep(0.5)
    
    # Remove duplicates based on title
    seen = set()
    unique_articles = []
    for article in all_articles:
        title_key = article['title'].lower()[:50]
        if title_key not in seen:
            seen.add(title_key)
            unique_articles.append(article)
    
    # Sort by category
    category_order = {
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
    
    unique_articles.sort(key=lambda x: category_order.get(x['category'], 99))
    
    # Build output
    output = {
        "last_updated": datetime.now().isoformat(),
        "sources": sources_scraped,
        "total_articles": len(unique_articles),
        "articles": unique_articles[:100]  # Keep latest 100
    }
    
    # Summary stats
    categories = {}
    for article in unique_articles:
        cat = article['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    output['summary'] = categories
    
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
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total articles: {data['total_articles']}")
    print(f"Sources: {', '.join(data['sources'])}")
    print("\nBy category:")
    for cat, count in data.get('summary', {}).items():
        print(f"  • {cat}: {count}")
    
    print("\n✅ Done!")

if __name__ == "__main__":
    main()