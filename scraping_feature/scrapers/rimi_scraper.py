import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0'}

urls = [
    'https://www.rimi.lt/e-parduotuve/lt/produktai/vaisiai-darzoves-ir-geles/c/SH-15?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-15%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/augaliniai-produktai/c/SH-77?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-77%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/pieno-produktai-kiausiniai-ir-suris/c/SH-11?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-11%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/duonos-gaminiai-/c/SH-3?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-3%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/mesa-ir-zuvis-/c/SH-9?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-9%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/saldytas-maistas/c/SH-13?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-13%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/bakaleja/c/SH-2?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-2%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/rimi-konditerija-ir-kulinarija/c/SH-34?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-34%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/vaiku-ir-kudikiu-prekes/c/SH-7?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-7%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/saldumynai-ir-uzkandziai/c/SH-23?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-23%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/gerimai/c/SH-4?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-4%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/alkoholiniai-ir-nealkoholiniai-gerimai/c/SH-1?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-1%3AassortmentStatus%3AinAssortment'
]

class RimiScraper:
    def scrape(self, item):
        for url in urls:
            result = self.scrape_based_on_url(item, url)
            if result:
                return result
            else:
                print(f"{item} not found in any category.")
                return None
        

    def scrape_based_on_url(self, item, url):
        base_url = "https://www.rimi.lt"
        
        for i in range(1, 5):  
            paginated_url = url.replace('currentPage=1', f'currentPage={i}')
            response = requests.get(paginated_url, headers=headers)

            if response.status_code != 200:
                print(f"Failed to fetch page {i} (Status {response.status_code})")
                return None

            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('li', class_='product-grid__item')

            for product in products:
                if item.lower() in product.text.lower():
                    
                    if product.find('div', class_='card__price-wrapper -has-discount'):
                        print(f"NUOLAIDA: {product.text.replace('\n', '').strip()}")
                        price_tag = product.find('div', class_='price-tag card__price')
                        
                        euro = price_tag.find('span').text.strip()
                        cents = price_tag.find('sup').text.strip()

                        print(f"NUOLAIDA: {euro} .... {cents}")


                    elif product.find('div', class_='card__price-wrapper'):
                        print(f"{product.text.replace('\n', '').strip()}")  
                        price_tag = product.find('div', class_='price-tag card__price')
                        
                        euro = price_tag.find('span').text.strip()
                        cents = price_tag.find('sup').text.strip()

                        print(f"be nuolaidos: {euro} .... {cents}")


                    
                    link_tag = product.find('a', class_='js-gtm-eec-product-click')
                    
                    if link_tag and 'href' in link_tag.attrs:
                        item_url = base_url + link_tag.attrs['href']                   
                    
                    
                    return product
        return None
