#!/usr/bin/env python3
"""
Liverpool News Scraper
Scrapes news from various RSS feeds and aggregates them into a JSON file
"""

import json
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from typing import List, Dict
import os

# RSS Feed Sources
RSS_FEEDS = [
    {
        "name": "Liverpool Echo",
        "url": "https://www.liverpoolecho.co.uk/sport/football/?service=rss",
        "filter_keywords": ["Liverpool FC", "Liverpool"]
    },
    {
        "name": "BBC Sport Liverpool",
        "url": "https://push.api.bbc.co.uk/v2/sport/teams/football/liverpool",
        "filter_keywords": ["Liverpool"]
    },
]

def fetch_rss_feed(url: str) -> str:
    """Fetch RSS feed content"""
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def parse_liverpool_echo(xml_content: str) -> List[Dict]:
    """Parse Liverpool Echo RSS feed"""
    articles = []
    
    try:
        root = ET.fromstring(xml_content)
        for item in root.findall('.//item'):
            title = item.findtext('title', '')
            link = item.findtext('link', '')
            description = item.findtext('description', '')
            pub_date = item.findtext('pubDate', '')
            
            # Get image
            media_content = item.find('.//{http://search.yahoo.com/mrss/}content')
            media_thumbnail = item.find('.//{http://search.yahoo.com/mrss/}thumbnail')
            
            image_url = ''
            if media_content is not None:
                image_url = media_content.get('url', '')
            elif media_thumbnail is not None:
                image_url = media_thumbnail.get('url', '')
            
            # Get keywords
            keywords = item.findtext('.//{http://search.yahoo.com/mrss/}keywords', '')
            
            # Only include Liverpool-related articles
            if 'Liverpool' in title or 'Liverpool' in keywords:
                articles.append({
                    'title': title.strip(),
                    'link': link,
                    'description': description.strip() if description else '',
                    'image': image_url,
                    'source': 'Liverpool Echo',
                    'pub_date': pub_date,
                    'keywords': keywords,
                    'category': categorize_article(title, keywords)
                })
    except Exception as e:
        print(f"Error parsing XML: {e}")
    
    return articles

def categorize_article(title: str, keywords: str) -> str:
    """Categorize article based on title and keywords"""
    title_lower = title.lower()
    keywords_lower = keywords.lower() if keywords else ''
    
    if any(word in title_lower for word in ['transfer', 'sign', 'signing', 'deal', 'contract']):
        return 'Transfer News'
    elif any(word in title_lower for word in ['injury', 'injured', 'recovery', 'fitness', 'ACL']):
        return 'Injury News'
    elif any(word in title_lower for word in ['preview', 'match preview', 'preview of', 'coming up']):
        return 'Match Preview'
    elif any(word in title_lower for word in ['women', 'WSL', 'female']):
        return 'WSL'
    elif any(word in title_lower for word in ['result', 'score', 'won', 'lost', 'draw', 'victory']):
        return 'Match Result'
    elif any(word in title_lower for word in ['breaking', 'breaking news', 'exclusive']):
        return 'Breaking'
    else:
        return 'General News'

def calculate_time_bucket(pub_date: str) -> str:
    """Calculate time bucket for article freshness"""
    # This is simplified - in production, you'd parse the actual date
    return 'recent'

def aggregate_news() -> Dict:
    """Main function to aggregate all news"""
    all_articles = []
    
    print("Fetching Liverpool Echo feed...")
    echo_content = fetch_rss_feed(RSS_FEEDS[0]['url'])
    if echo_content:
        echo_articles = parse_liverpool_echo(echo_content)
        all_articles.extend(echo_articles)
        print(f"  Found {len(echo_articles)} Liverpool articles")
    
    # Build final JSON structure
    aggregated = {
        "last_updated": datetime.now().isoformat(),
        "total_articles": len(all_articles),
        "articles": all_articles
    }
    
    return aggregated

def save_to_json(data: Dict, filename: str = "news-data.json"):
    """Save aggregated news to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(data['articles'])} articles to {filename}")

if __name__ == "__main__":
    print("=" * 50)
    print("Liverpool News Aggregator")
    print("=" * 50)
    
    news_data = aggregate_news()
    save_to_json(news_data)
    
    print("\nDone! Sample articles:")
    for article in news_data['articles'][:3]:
        print(f"  - {article['title'][:60]}...")