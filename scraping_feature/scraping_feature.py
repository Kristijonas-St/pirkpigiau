import requests
from bs4 import BeautifulSoup

class ScrapingRequest:
    def __init__(self, shop_name, shop_url, item):
        self.shop_name = shop_name
        self.shop_url = shop_url
        self.cheapest_item = None
        self.item = item
        self.error_message = None

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
        for i in range(1, 21):
            url = f'https://www.rimi.lt/e-parduotuve/lt/produktai/vaisiai-darzoves-ir-geles/c/SH-15?currentPage={i}&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-15%3AassortmentStatus%3AinAssortment'
            
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to fetch page {i} (Status {response.status_code})")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('li', class_='product-grid__item')

            for product in products:
                if self.item.lower() in product.text.lower():
                    print(f"Found {self.item} on page {i}: {product.text.replace('\n','').strip()}")
                    return

        print(f"{self.item} not found in 20 pages.")

scrape = ScrapingRequest('Rimi', 'https://www.rimi.lt/e-parduotuve/lt/produktai/vaisiai-darzoves-ir-geles/c/SH-15', 'Marinuotos')
scrape.scrape_price()
