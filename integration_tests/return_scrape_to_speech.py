
import pytest
from unittest.mock import patch

from scraping_feature.scraping_feature import ScrapingRequest
from speech_response_feature.speech_response import say_formatted_response

@pytest.mark.integration
@patch("speech_response_feature.speech_response.speak")
def test_rimi_scraped_speech_response(mock_speak):

    item_name = "pomidorai"
    shop_name = "Rimi"
    scraper = ScrapingRequest(shop_name, item_name)

    result = scraper.scrape_price()
    
    assert result is not None, f"{item_name} not found in {shop_name}"

    print(f"\nScraped item: {result.item_name}")

    say_formatted_response(
        is_found=True,
        item_to_search=result.item_name,
        shop_name=shop_name,
        price=result.cheapest_item
    )

    assert mock_speak.called, "speak() was not called"
    
    spoken_text = mock_speak.call_args[0][0]
    assert item_name[:-3] in spoken_text.lower(), f"Response does not contain {item_name}"
    assert shop_name in spoken_text, f"Response doesn't contain {shop_name}"
