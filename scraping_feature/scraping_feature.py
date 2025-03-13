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

        response = requests.get(self.shop_url, headers=headers)
        if response.status_code != 200:
            self.error_message = f"Nepavyko pasiekti {self.shop_name}  pasiūlymų puslapio."
            return self

        soup = BeautifulSoup(response.text, 'html.parser')
        products_containers = soup.find_all('div', class_='card card-small is-pointer h-100')

        products = []
        products_prices = []

        for product_container in products_containers:
            if product_container.find('div', class_='bg-primary text-white h-100 rounded-end-1'):
                products.append(product_container.find('div', class_='w-100 mb-auto'))
                products_prices.append(product_container.find('div', class_='d-flex justify-content-center'))

        mapping = dict(zip(products, products_prices))
        found_items = []

        for product_name in mapping:
            title_element = product_name.find('h4', class_='mt-4 text-truncate text-truncate--2')

            if title_element:
                title = title_element.text.strip().lower()

                if fuzz.partial_ratio(self.item.lower(), title) > 80:
                    price_whole_element = mapping[product_name].find('div', class_='my-auto price-eur text-end')

                    temp_div = mapping[product_name].find('div', class_='d-flex flex-column my-auto')

                    price_decimal_element = temp_div.find('span', class_='price-cents')

                    price_whole = price_whole_element.text.strip()
                    price_decimal = price_decimal_element.text.strip()

                    price = f"{price_whole}.{price_decimal} €"

                    found_items.append((title, price))

        if not found_items:
            self.error_message = f"Prekės \"{self.item}\" Maximos pasiūlymuose nerasta."
            return self

        found_items.sort(key=lambda x: float(x[1].replace(" €", "").replace(",", ".")))
        self.cheapest_item = found_items[0]

        return self




