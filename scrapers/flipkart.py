from .scraper import BaseScraper, ScrapedItem
from bs4 import BeautifulSoup
from typing import List
from config import PLATFORM_CONFIG
from urllib.parse import urlparse
import re
import json
import textwrap

class FlipkartScraper(BaseScraper):
    __config = None
    
    def __init__(self):
        self.__config= PLATFORM_CONFIG['flipkart']
        super().__init__()
    
    def images(self):
        imgs = []
        images = self.soup.find_all("img", class_= "DByuf4 IZexXJ jLEJ7H")
        for image in images:
            src = image.get("src")
            if src != None:
                imgs.append(src)
        return imgs;        
                
    
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
        try:
            self.soup = BeautifulSoup(html, "lxml")

            config = PLATFORM_CONFIG['flipkart']

            title = self.getText( config.title["tag"], config.title["attribute"], config.title["attr_value"])
            if not title:
                return None
            price = self.getText(config.price["tag"], config.price["attribute"], config.price["attr_value"])
            price = re.sub("[^0-9^.]", "", price)
            
            paths = self.soup.find_all("div", class_="r2CdBx")
            category_name = "Others"
            # Safely get the text from the second-to-last element
            if len(paths) >= 2:  # Ensure there are at least two elements
                category_name = paths[-2].get_text(strip=True)  # Access second-to-last and strip text
        

            
            description = self.getText( config.description["tag"], config.description["attribute"], config.description["attr_value"])
            
            spec = self.sepec()
            images = self.images()
            
            

            item =  ScrapedItem(
                name=title,
                discount_price=price, 
                sort_details=description[:100], 
                details=description, 
                is_specification=True,
                specification_name=json.dumps(list(spec.keys())), 
                specification_description=json.dumps(list(spec.values())), 
                images=images,
                category_name=category_name
            )
            
            return item
        except:
            return None
    
    def parseItemLinks(self, htlm: str) -> List[str]:
        soup = BeautifulSoup(htlm, "lxml")
        items = []
        contents = soup.find_all("a", class_="DMMoT0")
        for content in contents:
            items.append(self.__config.domain+content.get("href"))
        
        return items
        
