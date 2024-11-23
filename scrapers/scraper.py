import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Union
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Generic Model for Scraped Data


class ScrapedItem:
    def __init__(self, title: str, price: str, description, rating=None, url: str = None, spec : dict = None):
        self.title = title
        self.price = price
        self.rating = rating
        self.url = url
        self.description = description
        self.spec = spec

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "price": self.price,
            "rating": self.rating,
            "url": self.url,
            "description": self.description,
            "specification": self.spec,
        }
        
    def to_string(self):
        print("Title")    
        print("----------------------")    
        print(self.title)
        
        
        print("Description")    
        print("----------------------")    
        print(self.description)
        
        
        print("Price")    
        print("----------------------")    
        print(self.price)
        
        print("Spec")    
        print("----------------------")    
        print(self.spec)    

# Base Scraper Class


class BaseScraper:
    soup = BeautifulSoup

    def __init__(self):
        self.driver = None

    def setup_driver(self):
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("start-maximized")
        options.add_argument("enable-automation")
        options.add_argument("--disable-infobars")

        self.driver = webdriver.Chrome(options=options)

    def fetch_html(self, url: str) -> str:
        try:
            if not self.driver:
                self.setup_driver()
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            return self.driver.page_source
        except Exception as e:
            print(f"Error fetching URL {url}: {e}")
            return None

    def parse(self, html: str) -> ScrapedItem:
        raise NotImplementedError(
            "This method should be overridden by subclasses.")
    def sepec(self)-> dict:
        raise NotImplementedError(
            "This method should be overridden by subclasses.")    

    def scrape(self, url: str) -> ScrapedItem:
        html = self.fetch_html(url)
        item = self.parse(html)
        return item

    def getRawHtml( self, tag, attr, attr_value):
        title_element = self.soup.find(tag, {attr: attr_value})
        title = title_element if title_element else None
        return title

    def getText(self, tag, attr, attr_value):
        title = self.getRawHtml( tag, attr, attr_value)
        return title.text if title != None else ""
