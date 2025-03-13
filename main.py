from scraping_feature.scraping_feature import ScrapingRequest

maxima_url = "https://www.maxima.lt/pasiulymai"
item_to_search = "mangas"

request = ScrapingRequest("Maxima", maxima_url, item_to_search)
request.scrape_price()

if request.error_message:
    print(f"{request.error_message}")
elif request.cheapest_item:
    name, price = request.cheapest_item
    print(f"Pigiausias variantas: {name} už {price}")
else:
    print("Nepavyko rasti prekės.")
