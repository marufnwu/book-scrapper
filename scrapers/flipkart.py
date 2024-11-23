from .scraper import BaseScraper, ScrapedItem
from bs4 import BeautifulSoup
from typing import List
from config import PLATFORM_CONFIG


class FlipkartScraper(BaseScraper):
    def sepec(self)-> dict:
        rows = self.soup.find_all('tr', class_='WJdYP6 row')

        spec = {}

        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:  # Ensure the row has at least two cells
                key = cells[0].get_text(strip=True)  # Extract and clean the text from the first cell
                value = cells[1].get_text(strip=True)  # Extract and clean the text from the second cell
                spec[key] = value
        return spec        
        
    
    def parse(self, html: str) -> ScrapedItem:
        self.soup = BeautifulSoup(html, "lxml")

        config = PLATFORM_CONFIG['flipkart']

        title = self.getText( config.title["tag"], config.title["attribute"], config.title["attr_value"])
        price = self.getText(config.price["tag"], config.price["attribute"], config.price["attr_value"])
        description = self.getText( config.description["tag"], config.description["attribute"], config.description["attr_value"])
        
        spec = self.sepec()

        return ScrapedItem(title=title, price=price, description=description, spec=spec)
