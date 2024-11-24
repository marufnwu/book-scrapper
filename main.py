from scrapers.flipkart import FlipkartScraper
from uploader import ItemUploader

def main():
    platform_scrapers = {
        "flipkart": FlipkartScraper(),
    }

    platform = input(
        "Enter the platform to scrape (flipkart/amazon): ").strip().lower()
    url = input("Enter the URL to scrape: ").strip()

    if platform in platform_scrapers:
        scraper = platform_scrapers[platform]
        links = scraper.scrapeLinks(url)
        
        for link in links:
            item = scraper.scrape(link)
            uploader = ItemUploader()
            uploader.upload([item])
    else:
        print("Platform not supported.")


if __name__ == "__main__":
    main()
