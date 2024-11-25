from ast import Raise
from enum import Enum
from scrapers.flipkart import FlipkartScraper
from scrapers.scraper import BaseScraper
from uploader import ItemUploader


class LinkType(Enum):
    PRODUCT = 1
    CATEGORY = 2

def main():
    platform_scrapers = {
        "flipkart": FlipkartScraper(),
    }

    platform = input(
        "Enter the platform to scrape (flipkart/amazon): ").strip().lower()
    
    link_type_input = input("Enter link type (1 for PRODUCT, 2 for CATEGORY): ").strip()
    
    try:
        # Convert user input to the corresponding enum value
        link_type = LinkType(int(link_type_input))
    except ValueError:
        print("Link type is not valid.")
        return
    
    
    url = input("Enter the URL to scrape: ").strip()
    
    if not url:
        raise ValueError("URL not set")

    if platform in platform_scrapers:
        scraper = platform_scrapers[platform]
        links = scraper.scrapeLinks(url)
        
        for link in links:
            item = scraper.scrape(link)
            uploader = ItemUploader()
            uploader.upload([item])
    else:
        print("Platform not supported.")
        
def getHtml(scraper:BaseScraper):
            


if __name__ == "__main__":
    main()
