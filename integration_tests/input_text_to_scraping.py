import pytest
import time
from unittest.mock import patch
import streamlit as st
from main import perform_scraping

@pytest.mark.integration
@patch('scraping_feature.scraping_feature.RimiScraper.scrape')
def test_text_input_and_scraping_response_validation(mock_scrape):
    manual_input = "saldainiai"
    shop = ["Rimi"]
    st.session_state.recognized_text = manual_input

    mock_scrape.return_value = (st.session_state.recognized_text, 1.99, 'url', 'success')

    start_time = time.time()

    result, _ = perform_scraping(st.session_state.recognized_text, shop)

    elapsed_time = time.time() - start_time
    assert elapsed_time <= 10, f"System took too long to process a response: {elapsed_time:.2f}s (above 10s)"

    assert result is not None, f"Scraping returned None"

    message, price = result[0]
    assert isinstance(message, str), "Each result message should be a string"

    if price != float("inf"):
        assert price > 0, "Price should be greater than 0"
        assert manual_input.lower() in message.lower(), "Product name should appear in the message"
    else:
        expected_message = f"{shop[0].upper()}: Prekė {manual_input} nerasta."
        assert message == expected_message, f"Expected message: {expected_message}"
