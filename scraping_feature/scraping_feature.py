import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

class ScrapingRequest:
    def __init__(self, shop_name, shop_url, item):
        self.shop_name = shop_name
        self.shop_url = shop_url
        self.cheapest_item = None
        self.item = item
        self.error_message = None
        # TODO: Add functionality to also return `item_url` from this class

    def scrape_price(self):
        headers = {'User-Agent': 'Mozilla/5.0'}

        match self.shop_name:
            case "Maxima":
                pass
            case "IKI":
                pass            
            case "Rimi":
                self.scrape_rimi(headers)
            case _:
                print("Unknown error")

    def scrape_rimi(self, headers):
        response = requests.get(self.shop_url, headers=headers)
        if response.status_code != 200:
            self.error_message = f"Nepavyko pasiekti {self.shop_name}  pasiūlymų puslapio."
            print(self.error_message)
            return self

        soup = BeautifulSoup(response.text, 'html.parser')

        products = soup.find_all('li', class_='product-grid__item')
        for product in products:
            if self.item in product.text:
                #print(product.text.replace('\n','').strip())
                print(f"Found {self.item}: {product.text.replace('\n','').strip()}")

scrape = ScrapingRequest('Rimi', 'https://www.rimi.lt/e-parduotuve/lt/produktai/vaisiai-darzoves-ir-geles/c/SH-15', 'Bananai')
scrape.scrape_price()




        

        

        





