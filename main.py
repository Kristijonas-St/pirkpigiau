import streamlit as st

from scraping_feature.scraping_feature import ScrapingRequest
from speech_response_feature.speech_response import say_formatted_response

shop_name = "Rimi"
item_to_search = "itrinos"

st.title(f"{shop_name}.lt pigiausios prekės")

if st.button("Pasakykite prekę"):
    request = ScrapingRequest(shop_name, item_to_search)
    data = request.scrape_price()

    if not data:
        st.write("HORRIBLE ERROR")
    elif request.cheapest_item:
        st.markdown(f"{shop_name.upper()}: Pigiausias variantas: [{data.item_name}]({data.item_url}) už {data.cheapest_item}", unsafe_allow_html=True)
        say_formatted_response(data.item_name, shop_name, data.cheapest_item)        
    else:
        st.write("Nepavyko rasti prekės")





