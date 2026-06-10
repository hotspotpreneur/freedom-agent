#!/usr/bin/env python3
"""
Auto Lead Scraper - Uses web_fetch to extract plumber data
Covers all Northwest UK areas
"""

import csv
import re
import time
from datetime import datetime
from pathlib import Path
from multiprocessing import Pool, cpu_count
from functools import partial

AREAS = {
    # Merseyside (16)
    "Liverpool": "Merseyside",
    "Birkenhead": "Merseyside",
    "Southport": "Merseyside",
    "Bootle": "Merseyside",
    "St Helens": "Merseyside",
    "Wallasey": "Merseyside",
    "Bebington": "Merseyside",
    "Crosby": "Merseyside",
    "Formby": "Merseyside",
    "Huyton": "Merseyside",
    "Kirkby": "Merseyside",
    "Litherland": "Merseyside",
    "Moreton": "Merseyside",
    "Prescot": "Merseyside",
    "Rainhill": "Merseyside",
    "Whiston": "Merseyside",
    
    # Greater Manchester (47)
    "Manchester": "Greater Manchester",
    "Bolton": "Greater Manchester",
    "Bury": "Greater Manchester",
    "Oldham": "Greater Manchester",
    "Rochdale": "Greater Manchester",
    "Salford": "Greater Manchester",
    "Stockport": "Greater Manchester",
    "Wigan": "Greater Manchester",
    "Altrincham": "Greater Manchester",
    "Ashton-under-Lyne": "Greater Manchester",
    "Atherton": "Greater Manchester",
    "Audenshaw": "Greater Manchester",
    "Blackrod": "Greater Manchester",
    "Bramhall": "Greater Manchester",
    "Bredbury": "Greater Manchester",
    "Chadderton": "Greater Manchester",
    "Cheadle": "Greater Manchester",
    "Cheadle Hulme": "Greater Manchester",
    "Denton": "Greater Manchester",
    "Dukinfield": "Greater Manchester",
    "Eccles": "Greater Manchester",
    "Failsworth": "Greater Manchester",
    "Farnworth": "Greater Manchester",
    "Golborne": "Greater Manchester",
    "Hale": "Greater Manchester",
    "Hazel Grove": "Greater Manchester",
    "Hindley": "Greater Manchester",
    "Horwich": "Greater Manchester",
    "Hyde": "Greater Manchester",
    "Irlam": "Greater Manchester",
    "Leigh": "Greater Manchester",
    "Levenshulme": "Greater Manchester",
    "Littleborough": "Greater Manchester",
    "Middleton": "Greater Manchester",
    "Mossley": "Greater Manchester",
    "Newton-le-Willows": "Greater Manchester",
    "Prestwich": "Greater Manchester",
    "Radcliffe": "Greater Manchester",
    "Royton": "Greater Manchester",
    "Sale": "Greater Manchester",
    "Stretford": "Greater Manchester",
    "Swinton": "Greater Manchester",
    "Tyldesley": "Greater Manchester",
    "Urmston": "Greater Manchester",
    "Walkden": "Greater Manchester",
    "Westhoughton": "Greater Manchester",
    "Whitefield": "Greater Manchester",
    
    # Cheshire (28)
    "Chester": "Cheshire",
    "Warrington": "Cheshire",
    "Crewe": "Cheshire",
    "Nantwich": "Cheshire",
    "Macclesfield": "Cheshire",
    "Wilmslow": "Cheshire",
    "Alderley Edge": "Cheshire",
    "Bollington": "Cheshire",
    "Congleton": "Cheshire",
    "Disley": "Cheshire",
    "Ellesmere Port": "Cheshire",
    "Frodsham": "Cheshire",
    "Knutsford": "Cheshire",
    "Lymm": "Cheshire",
    "Middlewich": "Cheshire",
    "Mobberley": "Cheshire",
    "Neston": "Cheshire",
    "Northwich": "Cheshire",
    "Padgate": "Cheshire",
    "Penketh": "Cheshire",
    "Prestbury": "Cheshire",
    "Runcorn": "Cheshire",
    "Sandbach": "Cheshire",
    "Tarporley": "Cheshire",
    "Tattenhall": "Cheshire",
    "Widnes": "Cheshire",
    "Winsford": "Cheshire",
    "Wirral": "Cheshire",
    
    # Lancashire (49)
    "Preston": "Lancashire",
    "Blackburn": "Lancashire",
    "Blackpool": "Lancashire",
    "Burnley": "Lancashire",
    "Lancaster": "Lancashire",
    "Accrington": "Lancashire",
    "Bamber Bridge": "Lancashire",
    "Barnoldswick": "Lancashire",
    "Barrowford": "Lancashire",
    "Burscough": "Lancashire",
    "Chorley": "Lancashire",
    "Clayton": "Lancashire",
    "Clitheroe": "Lancashire",
    "Colne": "Lancashire",
    "Coppull": "Lancashire",
    "Croston": "Lancashire",
    "Darwen": "Lancashire",
    "Earby": "Lancashire",
    "Eccleston": "Lancashire",
    "Fleetwood": "Lancashire",
    "Garstang": "Lancashire",
    "Great Harwood": "Lancashire",
    "Haslingden": "Lancashire",
    "Hesketh Bank": "Lancashire",
    "Heskin": "Lancashire",
    "Kirkby Lonsdale": "Lancashire",
    "Leyland": "Lancashire",
    "Longridge": "Lancashire",
    "Lytham": "Lancashire",
    "Morecambe": "Lancashire",
    "Nelson": "Lancashire",
    "Newchurch": "Lancashire",
    "New Longton": "Lancashire",
    "Ormskirk": "Lancashire",
    "Oswaldtwistle": "Lancashire",
    "Padiham": "Lancashire",
    "Parbold": "Lancashire",
    "Penwortham": "Lancashire",
    "Poulton-le-Fylde": "Lancashire",
    "Preesall": "Lancashire",
    "Rawtenstall": "Lancashire",
    "Ribchester": "Lancashire",
    "Rishton": "Lancashire",
    "Rufford": "Lancashire",
    "Thornton": "Lancashire",
    "Upholland": "Lancashire",
    "Whalley": "Lancashire",
    "Wrea Green": "Lancashire",
    "Wrightington": "Lancashire",
}

OUTPUT_DIR = Path("memory/leads")
TODAY = datetime.now().strftime("%Y-%m-%d")

def parse_plumber_listing(text, town, county):
    """Extract plumber data from TrustATrader page content"""
    leads = []
    seen_phones = set()
    
    # Pattern: ### [Business Name](/traders/...)
    # Then: [Phone Number](tel:07xxx)
    
    # Split into trader blocks
    blocks = text.split("### [")
    
    for block in blocks[1:]:  # Skip first empty block
        try:
            # Extract business name (between [ and ](/traders/)
            name_match = re.search(r'^([^\]]+)\]\(/traders/', block)
            if not name_match:
                continue
            business_name = name_match.group(1).strip()
            
            # Extract phone number (tel:07xxx or similar)
            phone_match = re.search(r'tel:(\d+)', block)
            if not phone_match:
                continue
            phone = phone_match.group(1)
            
            # Skip if we've seen this phone
            if phone in seen_phones:
                continue
            seen_phones.add(phone)
            
            # Determine if mobile (starts with 07)
            if phone.startswith('07'):
                mobile_phone = phone
                phone = ""
            else:
                mobile_phone = ""
                phone = phone
            
            leads.append({
                'business_name': business_name,
                'category': 'plumbers',
                'phone': phone,
                'mobile_phone': mobile_phone,
                'email': '',
                'website': '',
                'city': town,
                'county': county,
                'source': 'trustatrader',
                'scraped_date': TODAY
            })
        except Exception as e:
            continue
    
    return leads

def generate_url(town):
    """Generate TrustATrader URL for a town"""
    slug = town.lower().replace(" ", "-").replace("&", "and")
    return f"https://www.trustatrader.com/plumbers-in-{slug}"

def main():
    print("=" * 60)
    print("Auto Lead Scraper - North West UK Plumbers")
    print("=" * 60)
    print(f"\nTotal areas to scrape: {len(AREAS)}")
    print("\nThis script generates the URLs and parsing logic.")
    print("Use web_fetch in batch to get the actual data.")
    
    # Show distribution
    by_county = {}
    for town, county in AREAS.items():
        by_county[county] = by_county.get(county, 0) + 1
    
    print("\nAreas by county:")
    for county, count in sorted(by_county.items()):
        print(f"  {county}: {count} towns")
    
    # Generate all URLs
    urls = []
    for town, county in AREAS.items():
        urls.append({
            'town': town,
            'county': county,
            'url': generate_url(town)
        })
    
    # Save URL list
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    url_file = OUTPUT_DIR / f"{TODAY}-trustatrader-urls.csv"
    with open(url_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['town', 'county', 'url'])
        writer.writeheader()
        writer.writerows(urls)
    
    print(f"\nURL list saved to: {url_file}")
    print("\nSample URLs (first 10):")
    for u in urls[:10]:
        print(f"  {u['town']} ({u['county']}): {u['url']}")
    
    return urls

if __name__ == "__main__":
    urls = main()