import argparse
from enum import Enum

from config.config import CONFIG
from scrapers.flipkart import FlipkartScraper
from Utils import Response
class LinkType(Enum):
    PRODUCT = 1
    CATEGORY = 2
    
    
platform_scrapers = {
        "flipkart": FlipkartScraper(),
        "amazon":FlipkartScraper(),
    }

def scrape_and_upload(platform, link_type, url)->Response:
    if platform not in platform_scrapers:
        return Response(
            error=True,
            message=f"Unsupported platform: {platform}"
        )

    scraper = platform_scrapers[platform]
    
    items = []

    if link_type == LinkType.CATEGORY:
        links = scraper.scrapeLinks(url)
        for link in links:
            item = scraper.scrape(link)
            if item:
                items.append(item)
    elif link_type == LinkType.PRODUCT:
        item = scraper.scrape(url)
        if item:
            items.append(item)
    else:
        return Response(
            error=True,
            message=f"Invalid link type: {link_type}"
        )
    
    return Response(
        data=items,
        message="Success"
    )

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
        print(result.json().strip())
    except Exception as e:
        print(Response(
            error=True,
            message=e.__str__()
        ))

if __name__ == "__main__":
    main()
