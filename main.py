from scrapers.flipkart import FlipkartScraper


def main():
    platform_scrapers = {
        "flipkart": FlipkartScraper(),
    }

    platform = input(
        "Enter the platform to scrape (flipkart/amazon): ").strip().lower()
    url = input("Enter the URL to scrape: ").strip()

    if platform in platform_scrapers:
        scraper = platform_scrapers[platform]
        scraped_data = scraper.scrape(url)
        print("Scraped Data:")
        print(scraped_data.to_string())
    else:
        print("Platform not supported.")


if __name__ == "__main__":
    main()
