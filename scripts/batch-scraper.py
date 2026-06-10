#!/usr/bin/env python3
"""
Batch Lead Scraper - North West UK Plumbers
Covers: Merseyside, Greater Manchester, Cheshire, Lancashire
"""

import csv
import re
from datetime import datetime
from pathlib import Path

# Comprehensive North West UK Areas
AREAS = {
    # Merseyside
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
    
    # Greater Manchester
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
    "Oldham": "Greater Manchester",
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
    
    # Cheshire
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
    
    # Lancashire
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

# Trusted UK Trade Directories
DIRECTORIES = [
    {
        "name": "trustatrader",
        "base_url": "https://www.trustatrader.com/plumbers-in-",
        "url_format": "https://www.trustatrader.com/plumbers-in-{town}",
    },
    {
        "name": "checkatrade", 
        "base_url": "https://www.checkatrade.com/plumbers-in/",
        "url_format": "https://www.checkatrade.com/plumbers-in/{town}",
    },
    {
        "name": "mybuilder",
        "base_url": "https://www.mybuilder.com/trades/plumbers",
        "url_format": "https://www.mybuilder.com/trades/plumbers?location={town}",
    },
]

OUTPUT_DIR = Path("memory/leads")
TODAY = datetime.now().strftime("%Y-%m-%d")

def generate_urls():
    """Generate URLs for all areas"""
    urls = []
    for town, county in AREAS.items():
        for directory in DIRECTORIES:
            url = directory["url_format"].format(
                town=town.lower().replace(" ", "-").replace("&", "and")
            )
            urls.append({
                "town": town,
                "county": county,
                "directory": directory["name"],
                "url": url
            })
    return urls

def extract_phone_numbers(text):
    """Extract UK phone numbers from text"""
    phones = []
    # UK mobile: 07xxx xxxxxx
    mobiles = re.findall(r'07[\d\s]{9,11}', text.replace("-", " "))
    for m in mobiles:
        clean = re.sub(r'\s+', '', m)
        if len(clean) == 11:
            phones.append(("mobile", clean))
    
    # UK landline: 01xxx, 02xxx, 03xxx
    landlines = re.findall(r'0[\d\s]{9,11}', text.replace("-", " "))
    for l in landlines:
        clean = re.sub(r'\s+', '', l)
        if len(clean) == 11 and not clean.startswith('07'):
            phones.append(("landline", clean))
    
    return phones

def save_leads(leads, filename_prefix="plumbers"):
    """Save leads to CSV"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    filename = f"{TODAY}-{filename_prefix}-northwest-uk.csv"
    output_path = OUTPUT_DIR / filename
    
    fieldnames = ['business_name', 'category', 'phone', 'mobile_phone', 
                  'email', 'website', 'city', 'county', 'source', 'scraped_date']
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(leads)
    
    return output_path, len(leads)

def main():
    print("=" * 60)
    print("Batch Lead Scraper - North West UK Plumbers")
    print("=" * 60)
    print(f"\nTotal areas to scrape: {len(AREAS)}")
    print(f"Directories: {len(DIRECTORIES)}")
    print(f"Total URLs: {len(AREAS) * len(DIRECTORIES)}")
    
    # Generate URLs
    urls = generate_urls()
    
    print(f"\nAreas by county:")
    by_county = {}
    for town, county in AREAS.items():
        by_county[county] = by_county.get(county, 0) + 1
    for county, count in sorted(by_county.items()):
        print(f"  {county}: {count} towns")
    
    print("\n" + "=" * 60)
    print("NEXT STEP: Use browser to scrape these URLs")
    print("=" * 60)
    
    # Save the URL list for reference
    url_file = OUTPUT_DIR / f"{TODAY}-scrape-urls.csv"
    with open(url_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['town', 'county', 'directory', 'url'])
        writer.writeheader()
        writer.writerows(urls)
    
    print(f"\nURL list saved to: {url_file}")
    print("\nTop 20 URLs to scrape:")
    for u in urls[:20]:
        print(f"  {u['town']} ({u['county']}) - {u['directory']}")
    print("  ...")
    
    return urls

if __name__ == "__main__":
    urls = main()