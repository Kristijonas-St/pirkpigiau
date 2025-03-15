import requests
from bs4 import BeautifulSoup

from .scrapers.rimi_scraper import RimiScraper


class ScrapingRequest:
    def __init__(self, shop_name, item):
        self.shop_name = shop_name
        self.item = item
        self.item_url = None
        self.cheapest_item = None
        self.message = None

    def scrape_price(self):
        match self.shop_name:
            case "Maxima":
                pass
            case "IKI":
                pass            
            case "Rimi":
                result = RimiScraper()
                self.cheapest_item, self.item_url, self.message = result.scrape(self.item)
                if self.cheapest_item and self.item_url and self.message:
                    print(f"{self.item} PRICE: {self.cheapest_item}, URL: {self.item_url}")
                    return self
                
                return None
            case _:
                print("Unknown error")



