import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

def scrape_price(item):
    url = "https://www.maxima.lt/pasiulymai"
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "❌ Nepavyko pasiekti Maxima pasiūlymų puslapio."

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

            if fuzz.partial_ratio(item.lower(), title) > 80:
                price_whole_element = mapping[product_name].find('div', class_='my-auto price-eur text-end')

                temp_div = mapping[product_name].find('div', class_='d-flex flex-column my-auto')

                price_decimal_element = temp_div.find('span', class_='price-cents')

                price_whole = price_whole_element.text.strip()
                price_decimal = price_decimal_element.text.strip()

                price = f"{price_whole}.{price_decimal} €"

                found_items.append((title, price))

    if not found_items:
        return f"🔍 Prekės \"{item}\" Maximos pasiūlymuose nerasta."

    found_items.sort(key=lambda x: float(x[1].replace(" €", "").replace(",", ".")))

    cheapest_item = found_items[0]

    return f"🛒 Pigiausias variantas: {cheapest_item[0]} už {cheapest_item[1]}"


