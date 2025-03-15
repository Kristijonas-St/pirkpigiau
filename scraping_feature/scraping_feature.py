import requests
from bs4 import BeautifulSoup

from scrapers.rimi_scraper import RimiScraper

class ScrapingRequest:
    def __init__(self, shop_name, item):
        self.shop_name = shop_name
        self.item = item
        self.shop_url = None
        self.cheapest_item = None
        self.error_message = None

    def scrape_price(self):
        match self.shop_name:
            case "Maxima":
                pass
            case "IKI":
                pass            
            case "Rimi":
                scraper = RimiScraper()
                scraper.scrape(self.item)
            case _:
                print("Unknown error")


scrape = ScrapingRequest('Rimi', 'Nektarinai')
scrape.scrape_price()
