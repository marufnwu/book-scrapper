from scrapers.generic import Generic
import sys

def main():
    if len(sys.argv) < 2:
        print("Error: No URL provided")
        return
    url = sys.argv[1]
    scraper = Generic()
    html = scraper.fetch_html(url)
    print(html)

if __name__ == "__main__":
    main()
