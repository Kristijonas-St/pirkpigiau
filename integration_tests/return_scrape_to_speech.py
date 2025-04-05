import time
from scraping_feature.scraping_feature import ScrapingRequest
from speech_response_feature.speech_response import say_formatted_response

def test_rimi_scraped_speech_response():
    item_name = "pomidorai"
    shop_name = "Rimi"
    scraper = ScrapingRequest(shop_name, item_name)

    result = scraper.scrape_price()
    assert result is not None, f"{item_name} not found in {shop_name}"

    start_time = time.time()
    say_formatted_response(
        is_found=True,
        item_to_search=result.item_name,
        shop_name=shop_name,
        price=result.cheapest_item
    )
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Speech response time: {elapsed_time:.2f} seconds")
    assert elapsed_time >= 4, f"Response time was {elapsed_time:.2f} - TOO QUICK"

