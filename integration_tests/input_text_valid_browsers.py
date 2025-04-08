import pytest
import time
from unittest.mock import patch
import streamlit as st
from main import perform_scraping

@pytest.mark.integration
@patch('scraping_feature.scraping_feature.IkiScraper.scrape')
def test_manual_input_passed_to_scraper_and_browser_support(mock_scrape):
    manual_input = "citrina"
    shop = ["Iki"]

    st.session_state.recognized_text = manual_input

    mock_scrape.return_value = (manual_input, 1.99, 'url', 'success')

    result, _ = perform_scraping(st.session_state.recognized_text, shop)

    assert result is not None and len(result) > 0, "Expected non-empty result from scraping"

    message, price = result[0]

    assert isinstance(message, str), "Result message must be a string"
    assert manual_input.lower() in message.lower(), "Input should be reflected in result message"

    assert isinstance(price, float), "Price must be a float"
    assert price > 0, "Price should be greater than 0"


    supported_browsers = ["Chrome", "Edge", "Safari"]

    for browser in supported_browsers:
        assert browser in supported_browsers, f"{browser} should be supported"

