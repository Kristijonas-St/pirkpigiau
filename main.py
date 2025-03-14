import streamlit as st

from scraping_feature.scraping_feature import ScrapingRequest
from speech_response_feature.speech_response import say_formatted_response

shop_name = "Maxima"
shop_url = "https://www.maxima.lt/pasiulymai"
fixed_item_url = "https://barbora.lt/produktai/citrinos-3-4-d-1-kg"
item_to_search = "Citrinos"

st.title("Maxima.lt pigiausios prekės")

if st.button("Pasakykite prekę"):
    request = ScrapingRequest("Maxima", shop_url, item_to_search).scrape_price()

    if request.error_message:
        st.write(request.error_message)
    elif request.cheapest_item:
        name, price = request.cheapest_item
        st.markdown(f"Pigiausias variantas: [{name}]({fixed_item_url}) už {price}", unsafe_allow_html=True)
        say_formatted_response(item_to_search, shop_name, price)        
    else:
        st.write("Nepavyko rasti prekės")



