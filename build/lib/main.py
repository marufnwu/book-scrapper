import argparse
from enum import Enum
import json

from config.config import CONFIG
from scrapers.flipkart import FlipkartScraper

class LinkType(Enum):
    PRODUCT = 1
    CATEGORY = 2
    
    
platform_scrapers = {
        "flipkart": FlipkartScraper(),
        "amazon":FlipkartScraper(),
    }

def scrape_and_upload(platform, link_type, url):
    if platform not in platform_scrapers:
        raise ValueError(f"Unsupported platform: {platform}")

    scraper = platform_scrapers[platform]
    
    items = []

    if link_type == LinkType.CATEGORY:
        links = scraper.scrapeLinks(url)
        for link in links:
            item = scraper.scrape(link)
            items.append(item)
    elif link_type == LinkType.PRODUCT:
        item = scraper.scrape(url)
        items.append(item)
    else:
        raise ValueError(f"Invalid link type: {link_type}")
    
    return items

def main():
    link_type_help = "Type of link to scrape: " + ", ".join(
        f"{lt.value} for {lt.name}" for lt in LinkType
    )
    
    parser = argparse.ArgumentParser(
        description="Scrape and upload items from e-commerce platforms."
    )
    # Dynamically set choices for platforms
    parser.add_argument(
        "-p", "--platform",
        type=str,
        required=True,
        choices=platform_scrapers.keys(),
        help=f"Platform to scrape (e.g., {', '.join(platform_scrapers.keys())})."
    )
    # Dynamically set choices for link types
    parser.add_argument(
        "-t", "--link-type",
        type=int,
        required=True,
        choices=[lt.value for lt in LinkType],
        help=link_type_help
    )
    parser.add_argument(
        "-u", "--url",
        type=str,
        required=True,
        help="URL to scrape."
    )
    

    parser.add_argument(
        "-d", "--debug",
        type=str,
        choices=["True", "False"],
        help=f"Override DEBUG value (default: {CONFIG['DEBUG']})."
    )

    args = parser.parse_args()
    
   # Override the global DEBUG configuration
    if args.debug is not None:
        CONFIG["DEBUG"] = args.debug == "True"
    
    try:
        link_type = LinkType(args.link_type)
        result = scrape_and_upload(args.platform, link_type, args.url)
        items_dict = [item.to_dict() for item in result]

        print(json.dumps(items_dict))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
