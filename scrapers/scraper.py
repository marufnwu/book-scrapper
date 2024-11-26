from subprocess import CREATE_NO_WINDOW
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Union
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Dict, Optional
import random
import string

from config.config import CONFIG


class ScrapedItem:
    def __init__(
        self,
        category_id: int = 0,  # Default category ID to 0
        name: str = "",  # Name is required for generating slug and keywords
        slug: Optional[str] = None,  # Generate slug if not provided
        sku: Optional[str] = None,  # Generate random SKU if not provided
        tags: Optional[str] = None,  # Tags can be optional
        sort_details: str = "",
        specification_name: str = "",
        specification_description: str = "",
        is_specification: bool = False,
        details: str = "",
        photo: Optional[str] = None,
        thumbnail: Optional[str] = None,
        discount_price: Optional[float] = None,
        previous_price: Optional[float] = 0,
        stock: int = 1000,  # Default stock to 1000
        meta_keywords: Optional[str] = None,  # Generate keywords if not provided
        meta_description: Optional[str] = None,
        status: bool = True,
        item_type: str = "normal",  # Default item type to "physical"
        images: List[str] = None,
        category_name=None
    ):
        self.category_id = category_id
        self.name = name
        self.slug = slug or self._generate_slug(name)
        self.sku = sku or self._generate_random_sku()
        self.tags = tags
        self.sort_details = sort_details
        self.specification_name = specification_name
        self.specification_description = specification_description
        self.is_specification = is_specification
        self.details = details
        self.photo = photo
        self.thumbnail = thumbnail
        self.discount_price = discount_price
        self.previous_price = previous_price
        self.stock = stock
        self.meta_keywords = meta_keywords or self._generate_keywords(name)
        self.meta_description = meta_description
        self.status = status
        self.item_type = item_type
        self.images = images or []
        self.category_name = category_name,

    @staticmethod
    def _generate_slug(name: str) -> str:
        """Generate a slug from the name."""
        return name.lower().replace(" ", "-")

    @staticmethod
    def _generate_random_sku(length: int = 8) -> str:
        """Generate a random SKU with alphanumeric characters."""
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

    @staticmethod
    def _generate_keywords(name: str) -> str:
        """Generate meta keywords from the name."""
        return ", ".join(name.lower().split())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category_id": self.category_id,
            "name": self.name,
            "slug": self.slug,
            "sku": self.sku,
            "tags": self.tags,
            "sort_details": self.sort_details,
            "specification_name": self.specification_name,
            "specification_description": self.specification_description,
            "is_specification": self.is_specification,
            "details": self.details,
            "photo": self.photo,
            "thumbnail": self.thumbnail,
            "discount_price": self.discount_price,
            "previous_price": self.previous_price,
            "stock": self.stock,
            "meta_keywords": self.meta_keywords,
            "meta_description": self.meta_description,
            "status": self.status,
            "item_type": self.item_type,
            "images": self.images,
            "category_name": self.category_name,
    }
        
    def to_string(self):
        print("Title")    
        print("----------------------")    
        print(self.name)
        
        
        print("Description")    
        print("----------------------")    
        print(self.details)
        
        
        print("Price")    
        print("----------------------")    
        print(self.discount_price)
        
        print("Spec")    
        print("----------------------")    
        print(self.specification_name)    

# Base Scraper Class


class BaseScraper:
    soup = BeautifulSoup

    def __init__(self):
        self.driver = None

    def setup_driver(self):
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("start-maximized")
        options.add_argument("enable-automation")
        options.add_argument("--disable-infobars")
        options.add_argument('log-level=3')
        
        service = Service()
        service.creation_flags = CREATE_NO_WINDOW

        self.driver = webdriver.Chrome(options=options, service=service)

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
    def parseItemLinks(self, htlm:str)->List[str]:    
        raise NotImplementedError(
            "This method should be overridden by subclasses.")
    def sepec(self)-> dict:
        raise NotImplementedError(
            "This method should be overridden by subclasses.")    

    def scrape(self, url: str) -> ScrapedItem:
        if CONFIG['DEBUG']:
            print(f"Fetching html content=> {url}")
            
        html = self.fetch_html(url)
        item = self.parse(html)
        return item
    
    
    def scrapeLinks(self, url: str) -> List[str]:
        html = self.fetch_html(url)
        items = self.parseItemLinks(html)
        return items

    def getRawHtml( self, tag, attr, attr_value):
        title_element = self.soup.find(tag, {attr: attr_value})
        title = title_element if title_element else None
        return title

    def getText(self, tag, attr, attr_value):
        title = self.getRawHtml( tag, attr, attr_value)
        return title.text if title != None else ""
