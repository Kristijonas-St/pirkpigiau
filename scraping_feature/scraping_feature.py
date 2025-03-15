import requests
from bs4 import BeautifulSoup

from scrapers.rimi_scraper import RimiScraper

class ScrapingRequest:
    def __init__(self, shop_name, item):
        self.shop_name = shop_name
        self.item = item
        self.item_url = None
        self.cheapest_item = None
        self.error_message = None

    def scrape_price(self):
        match self.shop_name:
            case "Maxima":
                pass
            case "IKI":
                pass            
            case "Rimi":
                result = RimiScraper()
                result.scrape(self.item)
            case _:
                print("Unknown error")



scrape1 = ScrapingRequest('Rimi', 'Fasuoti sunokę avokadai')
scrape1.scrape_price()

scrape2 = ScrapingRequest('Rimi', 'Bananai')
scrape2.scrape_price()

